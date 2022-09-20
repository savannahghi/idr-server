from django.http.request import HttpRequest
from django.http.response import HttpResponse


def trigger_error(request: HttpRequest) -> HttpResponse:  # pragma: no cover
    assert False, "This is an expected error."
    return HttpResponse(  # noqa
        content=b"<p>This should not be visible.</p>", status=200
    )
