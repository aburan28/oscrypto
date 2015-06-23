# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

from ctypes.util import find_library
from ctypes import c_void_p, c_int32, c_char_p, c_size_t, c_byte, c_int
from ctypes import CDLL, POINTER


from .._ffi import LibraryNotFoundError, FFIEngineError



security_path = find_library('Security')
if not security_path:
    raise LibraryNotFoundError('The library Security could not be found')

Security = CDLL(security_path, use_errno=True)

CFData = c_void_p
CFString = c_void_p
CFDictionary = c_void_p
CFError = c_void_p
CFType = c_void_p

CFTypeRef = POINTER(CFType)
CFAllocatorRef = c_void_p

OSStatus = c_int32

CFDataRef = POINTER(CFData)
CFStringRef = POINTER(CFString)
CFDictionaryRef = POINTER(CFDictionary)
CFErrorRef = POINTER(CFError)

SecKeyRef = POINTER(c_void_p)
SecCertificateRef = POINTER(c_void_p)
SecTransformRef = POINTER(c_void_p)
SecRandomRef = c_void_p

try:
    Security.SecRandomCopyBytes.argtypes = [SecRandomRef, c_size_t, c_char_p]
    Security.SecRandomCopyBytes.restype = c_int

    Security.SecKeyCreateFromData.argtypes = [CFDictionaryRef, CFDataRef, POINTER(CFErrorRef)]
    Security.SecKeyCreateFromData.restype = SecKeyRef

    Security.SecEncryptTransformCreate.argtypes = [SecKeyRef, POINTER(CFErrorRef)]
    Security.SecEncryptTransformCreate.restype = SecTransformRef

    Security.SecDecryptTransformCreate.argtypes = [SecKeyRef, POINTER(CFErrorRef)]
    Security.SecDecryptTransformCreate.restype = SecTransformRef

    Security.SecTransformSetAttribute.argtypes = [SecTransformRef, CFStringRef, CFTypeRef, POINTER(CFErrorRef)]
    Security.SecTransformSetAttribute.restype = c_byte

    Security.SecTransformExecute.argtypes = [SecTransformRef, POINTER(CFErrorRef)]
    Security.SecTransformExecute.restype = CFTypeRef

    Security.SecVerifyTransformCreate.argtypes = [SecKeyRef, CFDataRef, POINTER(CFErrorRef)]
    Security.SecVerifyTransformCreate.restype = SecTransformRef

    Security.SecSignTransformCreate.argtypes = [SecKeyRef, POINTER(CFErrorRef)]
    Security.SecSignTransformCreate.restype = SecTransformRef

    Security.SecCertificateCreateWithData.argtypes = [CFAllocatorRef, CFDataRef]
    Security.SecCertificateCreateWithData.restype = SecCertificateRef

    Security.SecCertificateCopyPublicKey.argtypes = [SecCertificateRef, POINTER(SecKeyRef)]
    Security.SecCertificateCopyPublicKey.restype = OSStatus

    Security.SecCopyErrorMessageString.argtypes = [OSStatus, c_void_p]
    Security.SecCopyErrorMessageString.restype = CFStringRef

    setattr(Security, 'kSecRandomDefault', SecRandomRef.in_dll(Security, 'kSecRandomDefault'))

    setattr(Security, 'kSecPaddingKey', CFStringRef.in_dll(Security, 'kSecPaddingKey'))
    setattr(Security, 'kSecPaddingPKCS7Key', CFStringRef.in_dll(Security, 'kSecPaddingPKCS7Key'))
    setattr(Security, 'kSecPaddingPKCS5Key', CFStringRef.in_dll(Security, 'kSecPaddingPKCS5Key'))
    setattr(Security, 'kSecPaddingPKCS1Key', CFStringRef.in_dll(Security, 'kSecPaddingPKCS1Key'))
    setattr(Security, 'kSecPaddingNoneKey', CFStringRef.in_dll(Security, 'kSecPaddingNoneKey'))
    setattr(Security, 'kSecModeCBCKey', CFStringRef.in_dll(Security, 'kSecModeCBCKey'))
    setattr(Security, 'kSecTransformInputAttributeName', CFStringRef.in_dll(Security, 'kSecTransformInputAttributeName'))
    setattr(Security, 'kSecDigestTypeAttribute', CFStringRef.in_dll(Security, 'kSecDigestTypeAttribute'))
    setattr(Security, 'kSecDigestLengthAttribute', CFStringRef.in_dll(Security, 'kSecDigestLengthAttribute'))
    setattr(Security, 'kSecIVKey', CFStringRef.in_dll(Security, 'kSecIVKey'))

    setattr(Security, 'kSecAttrKeyClass', CFStringRef.in_dll(Security, 'kSecAttrKeyClass'))
    setattr(Security, 'kSecAttrKeyClassPublic', CFTypeRef.in_dll(Security, 'kSecAttrKeyClassPublic'))
    setattr(Security, 'kSecAttrKeyClassPrivate', CFTypeRef.in_dll(Security, 'kSecAttrKeyClassPrivate'))

    setattr(Security, 'kSecDigestSHA1', CFStringRef.in_dll(Security, 'kSecDigestSHA1'))
    setattr(Security, 'kSecDigestSHA2', CFStringRef.in_dll(Security, 'kSecDigestSHA2'))
    setattr(Security, 'kSecDigestMD5', CFStringRef.in_dll(Security, 'kSecDigestMD5'))

    setattr(Security, 'kSecAttrKeyType', CFStringRef.in_dll(Security, 'kSecAttrKeyType'))

    setattr(Security, 'kSecAttrKeyTypeRSA', CFTypeRef.in_dll(Security, 'kSecAttrKeyTypeRSA'))
    setattr(Security, 'kSecAttrKeyTypeDSA', CFTypeRef.in_dll(Security, 'kSecAttrKeyTypeDSA'))
    setattr(Security, 'kSecAttrKeyTypeECDSA', CFTypeRef.in_dll(Security, 'kSecAttrKeyTypeECDSA'))

    setattr(Security, 'kSecAttrCanSign', CFTypeRef.in_dll(Security, 'kSecAttrCanSign'))
    setattr(Security, 'kSecAttrCanVerify', CFTypeRef.in_dll(Security, 'kSecAttrCanVerify'))

    setattr(Security, 'kSecAttrKeyTypeAES', CFTypeRef.in_dll(Security, 'kSecAttrKeyTypeAES'))
    setattr(Security, 'kSecAttrKeyTypeRC4', CFTypeRef.in_dll(Security, 'kSecAttrKeyTypeRC4'))
    setattr(Security, 'kSecAttrKeyTypeRC2', CFTypeRef.in_dll(Security, 'kSecAttrKeyTypeRC2'))
    setattr(Security, 'kSecAttrKeyType3DES', CFTypeRef.in_dll(Security, 'kSecAttrKeyType3DES'))
    setattr(Security, 'kSecAttrKeyTypeDES', CFTypeRef.in_dll(Security, 'kSecAttrKeyTypeDES'))

except (AttributeError):
    raise FFIEngineError('Error initializing ctypes')