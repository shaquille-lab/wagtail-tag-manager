import datetime

from django.conf import settings

from .models import Tag


def set_cookie(response, key, value, days_expire=None):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60

    delta = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
    expires = datetime.datetime.strftime(delta, "%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie(
        key, value, max_age=max_age, expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None)


def get_cookie_state(request):
    cookies = request.COOKIES
    return {
        tag_type: cookies.get(f'wtm_{tag_type}', 'false') != 'false'
        for tag_type in Tag.get_types()
    }