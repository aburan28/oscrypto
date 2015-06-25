# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import sys


if sys.platform == 'darwin':
    from ._osx.symmetric import (  #pylint: disable=W0611
        aes_cbc_pkcs7_encrypt,
        aes_cbc_pkcs7_decrypt,
        rc4_encrypt,
        rc4_decrypt,
        rc2_cbc_pkcs5_encrypt,
        rc2_cbc_pkcs5_decrypt,
        des_cbc_pkcs5_encrypt,
        des_cbc_pkcs5_decrypt,
        tripledes_cbc_pkcs5_encrypt,
        tripledes_cbc_pkcs5_decrypt,
    )

elif sys.platform == 'win32':
    from ._win.symmetric import (  #pylint: disable=W0611
        aes_cbc_pkcs7_encrypt,
        aes_cbc_pkcs7_decrypt,
        rc4_encrypt,
        rc4_decrypt,
        rc2_cbc_pkcs5_encrypt,
        rc2_cbc_pkcs5_decrypt,
        des_cbc_pkcs5_encrypt,
        des_cbc_pkcs5_decrypt,
        tripledes_cbc_pkcs5_encrypt,
        tripledes_cbc_pkcs5_decrypt,
    )

else:
    from ._linux.symmetric import (  #pylint: disable=W0611
        aes_cbc_pkcs7_encrypt,
        aes_cbc_pkcs7_decrypt,
        rc4_encrypt,
        rc4_decrypt,
        rc2_cbc_pkcs5_encrypt,
        rc2_cbc_pkcs5_decrypt,
        des_cbc_pkcs5_encrypt,
        des_cbc_pkcs5_decrypt,
        tripledes_cbc_pkcs5_encrypt,
        tripledes_cbc_pkcs5_decrypt,
    )
