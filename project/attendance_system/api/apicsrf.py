from django.middleware import csrf

class apicsrf(csrf):
    def __init__(self):
        self.super()
        
    def get_token(request):
    """
    Return the CSRF token required for a POST form. The token is an
    alphanumeric value. A new token is created if one is not already set.
    A side effect of calling this function is to make the csrf_protect
    decorator and the CsrfViewMiddleware add a CSRF cookie and a 'Vary: Cookie'
    header to the outgoing response.  For this reason, you may need to use this
    function lazily, as is done by the csrf context processor.
    """
    if "CSRF_COOKIE" not in request.META:
        csrf_secret = _get_new_csrf_string()
        request.META["CSRF_COOKIE"] = _salt_cipher_secret(csrf_secret)
    else:
        csrf_secret = _unsalt_cipher_token(request.META["CSRF_COOKIE"])
    request.META["CSRF_COOKIE_USED"] = True
    return _salt_cipher_secret(csrf_secret)