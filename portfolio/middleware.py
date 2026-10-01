from urllib.parse import urlsplit

from django.conf import settings
from django.http import HttpResponsePermanentRedirect

from .canonical import canonical_url


class CanonicalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            settings.PUBLIC_SITE_URL
            and request.method in ("GET", "HEAD")
            and request.path != "/health/"
            and request.get_host().lower()
            != urlsplit(settings.PUBLIC_SITE_URL).netloc.lower()
        ):
            return HttpResponsePermanentRedirect(
                canonical_url(request, include_query=True)
            )
        return self.get_response(request)
