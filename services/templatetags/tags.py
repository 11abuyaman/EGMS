import os
import re

from django import template
from django.template.defaultfilters import safe
from django.templatetags.static import static
from django.urls import NoReverseMatch, reverse

from EGMS import settings

register = template.Library()


@register.simple_tag
def no_results(flag, title='', message=''):
    return safe("""
        <div class="no-results">
             <img src="{}">
             <div>
                <h3>{}</h3>
                <p>{}</p>
             </div>
        </div>
        """.format(
        static('services/assets/media/svg/no-results.svg'),
        title if title else "No appointments",
        message if message else "We couldn't find any available appointments at this time range..",
    )) if not flag else ""


@register.simple_tag()
def absolute_static(path):
    return os.path.join(settings.BASE_DIR, static(path))


@register.filter()
def dash_if_none(value):
    return value if value else "-"


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''
