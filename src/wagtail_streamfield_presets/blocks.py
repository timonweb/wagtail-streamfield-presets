from collections.abc import Callable
from dataclasses import dataclass

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property
from django.utils.translation import gettext
from wagtail.admin.staticfiles import versioned_static
from wagtail.admin.telepath import register
from wagtail.blocks import StreamBlock, StreamValue
from wagtail.blocks.stream_block import StreamBlockAdapter


@dataclass(frozen=True)
class Preset:
    """`build` returns stream data as a page would be written, a list of
    `(block_type, value)`. It runs each time the editor renders, so it may read the
    database."""

    key: str
    label: str
    build: Callable[[], list]


class PresetStreamBlock(StreamBlock):
    """A StreamBlock everywhere but the editor, where it offers its presets. They are a
    `Meta` option rather than a constructor argument because Wagtail writes constructor
    arguments into migrations, which a callable cannot survive."""

    class Meta:
        presets = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        keys = [preset.key for preset in self.meta.presets]
        if len(keys) != len(set(keys)):
            raise ImproperlyConfigured(
                f"{type(self).__name__} declares a preset key more than once: {keys}"
            )

    def preset_value(self, preset):
        """Round-tripped through the stored form, so the editor receives exactly what a
        saved page would give it, ids and all."""
        return self.to_python(self.get_prep_value(StreamValue(self, preset.build())))

    def preset_states(self):
        return [
            {
                "key": preset.key,
                "label": str(preset.label),
                "state": self.get_form_state(self.preset_value(preset)),
            }
            for preset in self.meta.presets
        ]


def picker_strings():
    """Translated here rather than in the script, so the package needs no JavaScript
    catalog. The confirmation names no count: plural rules differ by language, and the
    count is only known in the browser."""
    return {
        "label": gettext("Start from a preset"),
        "placeholder": gettext("Choose a preset…"),
        "load": gettext("Load"),
        "confirm": gettext(
            "Replace the blocks in this field with the “%(preset)s” preset? Your "
            "changes to them will be lost."
        ),
    }


class PresetStreamBlockAdapter(StreamBlockAdapter):
    js_constructor = "wagtail_streamfield_presets.PresetStreamBlock"

    def js_args(self, block):
        return [
            *super().js_args(block),
            {"presets": block.preset_states(), "strings": picker_strings()},
        ]

    @cached_property
    def media(self):
        return super().media + forms.Media(
            js=[
                versioned_static(
                    "wagtail_streamfield_presets/js/streamfield-presets.js"
                )
            ],
            css={
                "all": [
                    versioned_static(
                        "wagtail_streamfield_presets/css/streamfield-presets.css"
                    )
                ]
            },
        )


register(PresetStreamBlockAdapter(), PresetStreamBlock)
