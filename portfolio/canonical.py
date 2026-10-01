from django.conf import settings


def canonical_url(request, *, include_query=False):
    """Return the configured public URL, or the current request URL locally."""
    path = request.get_full_path() if include_query else request.path
    if settings.PUBLIC_SITE_URL:
        return f"{settings.PUBLIC_SITE_URL}{path}"
    return request.build_absolute_uri(path)
