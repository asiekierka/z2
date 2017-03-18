from django.template import Library
from django.utils.safestring import mark_safe

register = Library()


@register.simple_tag()
def content_warning(*args, **kwargs):
    output = """
        <div class="content-warning">
        <div class="text">
            <b class="heading">CONTENT WARNING</b>
            <p>The following content contains material which may be offensive to
            some audiences. It was most likely originally created by a teenager
            who has since grown up. This material does not necessarily reflect
            its creator's current opinions nor behaviors.</p>

            <p>Specifically, this page contains depictions of or references to:
            <br><b>{}</b></p>

            <div class="controls r">
                <span class="jsLink" name="cw-hide-all">Hide all future content warnings</span> |
                <span class="jsLink" name="cw-hide-this">Hide this</span>
            </div>
        </div>
    </div>
    """

    output = output.format(", ".join(args).title())

    return mark_safe(output + "\n")