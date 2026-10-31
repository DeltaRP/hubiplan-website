"""Sicherheitskopfzeilen für alle Antworten."""

from __future__ import annotations

from urllib.parse import urlparse

from django.conf import settings


def _origin(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}" if p.scheme and p.netloc else ""


class SecurityHeaders:
    def __init__(self, get_response):
        self.get_response = get_response
        hubiplan = _origin(settings.HUBIPLAN_PUBLIC_URL)
        connect = " ".join(x for x in ("'self'", hubiplan) if x)
        form = " ".join(x for x in ("'self'", hubiplan) if x)
        self.csp = (
            "default-src 'self'; img-src 'self' data:; script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            f"connect-src {connect}; form-action {form}; frame-ancestors 'none'; "
            "base-uri 'self'; object-src 'none'"
        )

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault("Content-Security-Policy", self.csp)
        response.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        response.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        return response
