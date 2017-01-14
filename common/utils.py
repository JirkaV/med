# https://code.djangoproject.com/ticket/24967
#
# needed because Apache mod_proxy + gunicorn + Django
# somehow duplicate SCRIPT_NAME in URL on redirects and I could not
# find a better solution
#
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.conf import settings

def absolute_redirect(url, args=None):
    """
    This is a function that I needed to make because
    Django's default redirect function doesn't work properly when
    FORCE_SCRIPT_NAME is set. It returns a full URL for redirection
    """

    reverse_url = reverse(url, args=args)
    try:
        url_root = settings.URL_ROOT
    except AttributeError:
        url_root = ''

    if url_root:
        reverse_url = reverse(url, args=args)
        return redirect('%s%s' % (url_root, reverse_url))
    else:
        return redirect(reverse_url)
