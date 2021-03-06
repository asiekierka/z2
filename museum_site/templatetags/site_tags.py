from datetime import datetime

from django import template
from django.template import Template, Context, Library
from django.template import defaultfilters as filters
from django.utils.safestring import mark_safe

from museum_site.models import File

register = Library()


@register.filter
def as_template(raw):
    raw = "{% load staticfiles %}\n{% load site_tags %}\n{% load zzt_tags %}" + raw
    return Template(raw).render(Context())


@register.simple_tag()
def content_warning(*args, **kwargs):
    output = """
        <div class="content-warning">
        <div class="text">
            <b class="heading">CONTENT WARNING</b>
            <p>The following content contains material which may be offensive
            to some audiences. It was most likely originally created by a
            teenager who has since grown up. This material does not necessarily
            reflect its creator's current opinions nor behaviors.</p>

            <p>Specifically, this page contains depictions of or references to:
            <br><b>{}</b></p>

            <div class="controls r">
                <span class="jsLink" name="cw-hide-all">Hide all future content
                warnings</span> |
                <span class="jsLink" name="cw-hide-this"
                data-content-warning-key="{}">Hide this</span>
                {}

            </div>
        </div>
    </div>
    """
    content_warning_key = kwargs.get("key", "")

    if not kwargs.get("noskip"):
        skip_text = ' | <a href="#end-cw">Jump past warned content</a>'
    else:
        skip_text= ""

    output = output.format(", ".join(args).title(), content_warning_key, skip_text)

    return mark_safe(output + "\n")


@register.simple_tag()
def patreon_plug(*args, **kwargs):
    output = """
        <div class="patreon-plug">
        <div class="text">
            <div class="heading"><span>======</span> A Worlds of ZZT Production <span>======</span></div>
            <p>
               The Worlds of ZZT project is
               committed to the preservation
               of ZZT and its history.</p>

               <p> This article was produced
               thanks to supporters on Patreon.</p>

            <a href="https://patreon.com/worldsofzzt" target="_blank">Support Worlds of ZZT on
            Patreon!</a>
        </div>
    </div>
    """

    return mark_safe(output + "\n")

@register.simple_tag()
def cl_info(id):
    file = File.objects.get(pk=id)

    if file.company:
        company = "Published Under: {}<br>".format(file.company)
    else:
        company = ""

    if file.release_date is not None:
        release = file.release_date.strftime("%B %m, %Y")
    else:
        release = "Unknown"


    output = """
        <div class="c">
            <h2>{title}</h2>
            By: {author}<br>
            {company}
            Released: {release}<br>
            <a href="{download}" target="_blank">Download</a> | <a href="{play}" target="_blank">Play Online</a> | <a href="{view}" target="_blank">View Files</a><br>
        </div>

    """.format(title=file.title, author=file.author, company=company, release=release, download=file.download_url(), play=file.play_url(), view=file.file_url())

    return mark_safe(output + "\n")


@register.tag(name="commentary")
def scroll(parser, token):
    nodelist = parser.parse(('endcommentary',))
    parser.delete_first_token()
    return Commentary(nodelist)

class Commentary(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        material_nodes = self.nodelist[:-1]
        commentary_node = self.nodelist[-1]

        material = ""
        commentary = ""

        for n in material_nodes:
            material += n.render(context)

        #commentary = filters.linebreaks(commentary_node.render(context).strip())
        commentary = commentary_node.render(context).strip()
        if (commentary and commentary[0] != "<") or commentary.startswith("<!"):
            commentary = "<p>" + commentary.replace("\n\n", "</p><p>") + "</p>"

        output = """
<div class="side-commentary">
    <div class="material">
    {material}
    </div>
    <div class="commentary">
        {commentary}
    </div>
</div>
"""
        return output.format(material=material, commentary=commentary)


@register.tag(name="il")
def register_il(parser, token):
    nodelist = parser.parse(('endil',))
    parser.delete_first_token()
    # Strip the leading "il " before splitting args
    raw_args = token.contents[3:] if len(token.contents.split()) >= 2 else ""
    return IL(nodelist, raw_args)

class IL(template.Node):
    def __init__(self, nodelist, raw_args=""):
        self.args = raw_args.split("|") + ["", "", "", ""]
        self.nodelist = nodelist

    def render(self, context):
        text = self.nodelist[0].render(context)
        q = text if self.args[0] == "" else self.args[0]
        filename = "&file=" + self.args[1] if self.args[1] != "" else ""
        board = "&board=" + self.args[2] if self.args[2] != "" else ""
        coords = "#" + self.args[3] if self.args[3] != "" else ""
        url = "/search?q={}&auto=1".format(q) + filename + board + coords
        output = "<a class='il' target='_blank' href='{url}'>{text}</a>".format(url=url, text=text)
        return output
