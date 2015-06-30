# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import sys
import base64
import datetime
import struct

from .._ffi import buffer_from_bytes, bytes_from_buffer, deref, struct_from_buffer, new, null, unwrap, array_from_pointer
from ._crypt32 import crypt32, crypt32_const, get_error, handle_error

if sys.version_info < (3,):
    str_cls = unicode  #pylint: disable=E0602
    from cStringIO import StringIO as BytesIO  #pylint: disable=F0401
else:
    str_cls = str
    from io import BytesIO



def extract_trusted_roots():
    """
    Returns a byte string of all trusted root certificates stored in the
    Windows certificate store.

    :raises:
        pdfcrypto.errors.CACertsError - when an error occurs exporting certs

    :return:
        A bytestring of OpenSSL-compatiable PEM-encoded certificates
    """

    certificates = {}

    now = datetime.datetime.utcnow()

    for store in ["ROOT", "CA"]:
        store_handle = crypt32.CertOpenSystemStore(None, store)
        handle_error(store_handle)

        cert_pointer = crypt32.CertEnumCertificatesInStore(store_handle, None)
        while bool(cert_pointer):
            context = unwrap(cert_pointer)

            skip = False

            if context.dwCertEncodingType != crypt32_const.X509_ASN_ENCODING:
                skip = True

            if not skip:
                cert_info = unwrap(context.pCertInfo)

                subject_struct = cert_info.Subject
                subject = bytes_from_buffer(subject_struct.pbData, subject_struct.cbData)

                not_before = _convert_filetime_to_datetime(cert_info.NotBefore)
                not_after = _convert_filetime_to_datetime(cert_info.NotAfter)

                if not_before > now:
                    skip = True

                if not_after < now:
                    skip = True

            if not skip:
                has_enhanced_usage = True

                to_read = new(crypt32, 'DWORD *', 0)
                res = crypt32.CertGetEnhancedKeyUsage(context, 0, null(), to_read)
                if res == 0:
                    error_code, _ = get_error()
                    if error_code == crypt32_const.CRYPT_E_NOT_FOUND:
                        has_enhanced_usage = False
                    else:
                        handle_error(res)
                else:
                    usage_buffer = buffer_from_bytes(deref(to_read))
                    res = crypt32.CertGetEnhancedKeyUsage(context, 0, usage_buffer, to_read)
                    handle_error(res)

                    key_usage = struct_from_buffer(crypt32, 'CERT_ENHKEY_USAGE', usage_buffer)
                    if key_usage.cUsageIdentifier > 0:
                        print(array_from_pointer(crypt32, 'LPSTR', key_usage.rgpszUsageIdentifier, int(key_usage.cUsageIdentifier)))

                # Having no enhanced usage properties means a cert is distrusted
                if has_enhanced_usage and key_usage.cUsageIdentifier == 0:
                    skip = True

            if not skip:
                data = bytes_from_buffer(context.pbCertEncoded, int(context.cbCertEncoded))
                certificates[subject] = data

            cert_pointer = crypt32.CertEnumCertificatesInStore(store_handle, cert_pointer)

        result = crypt32.CertCloseStore(store_handle, 0)
        handle_error(result)
        store_handle = None

    output = BytesIO()
    for der_subject in certificates:
        der_cert = certificates[der_subject]
        b64_cert = base64.b64encode(der_cert)
        b64_len = len(b64_cert)
        output.write(b'-----BEGIN CERTIFICATE-----\n')
        i = 0
        while i < b64_len:
            output.write(b64_cert[i:i+64])
            output.write(b'\n')
            i += 64
        output.write(b'-----END CERTIFICATE-----\n')

    return output.getvalue()


def _convert_filetime_to_datetime(filetime):
    """
    Windows returns times as 64-bit unsigned longs that are the number
    of hundreds of nanoseconds since Jan 1 1601. This converts it to
    a datetime object.

    :param filetime:
        A FILETIME struct object

    :return:
        A (UTC) datetime object
    """

    hundreds_nano_seconds = struct.unpack('>Q', struct.pack('>LL', filetime.dwHighDateTime, filetime.dwLowDateTime))[0]
    seconds_since_1601 = hundreds_nano_seconds / 10000000
    epoch_seconds = seconds_since_1601 - 11644473600  # Seconds from Jan 1 1601 to Jan 1 1970

    try:
        return datetime.datetime.fromtimestamp(epoch_seconds)
    except (OSError):
        return datetime.datetime(2037, 1, 1)