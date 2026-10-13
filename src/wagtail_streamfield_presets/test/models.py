from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtail_streamfield_presets.blocks import Preset, PresetStreamBlock


def introduction():
    return [
        ("heading", "Preset heading"),
        ("paragraph", "Preset paragraph"),
        ("links", [{"label": "First link"}]),
    ]


class LinkBlock(blocks.StructBlock):
    label = blocks.CharBlock()


class SectionStream(PresetStreamBlock):
    heading = blocks.CharBlock()
    paragraph = blocks.TextBlock()
    links = blocks.ListBlock(LinkBlock())

    class Meta:
        presets = [Preset("introduction", "Introduction", introduction)]


class PresetPage(Page):
    body = StreamField(SectionStream(), blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]
