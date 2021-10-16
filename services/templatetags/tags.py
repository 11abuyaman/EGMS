import os

from django import template
from django.template.defaultfilters import safe
from django.templatetags.static import static

from EGMS import settings

register = template.Library()


@register.simple_tag
def no_appointments(flag):
    return safe("""
        <div class="no-results">
             <img src="{}">
             <div>
                <h3>No appointments</h3>
                <p>We couldn't find any available appointments at this time range..</p>
             </div>
        </div>
        """.format(static('services/assets/media/svg/no-results.svg'))) if not flag else ""


@register.simple_tag()
def absolute_static(path):
    return os.path.join(settings.BASE_DIR, static(path))

