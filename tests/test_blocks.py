import html

from io import StringIO

import pytest

from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.utils.translation import gettext_lazy
from wagtail import blocks
from wagtail.admin.telepath import JSContext
from wagtail.blocks.stream_block import StreamBlockAdapter
from wagtail.models import Page

from wagtail_streamfield_presets.blocks import Preset, PresetStreamBlock
from wagtail_streamfield_presets.test.models import PresetPage, SectionStream


def packed(block):
    return JSContext().pack(block)


def options(block):
    """The argument this package adds after Wagtail's own four."""
    return packed(block)["_args"][4]


class BareStream(PresetStreamBlock):
    heading = blocks.CharBlock()


class TestPacking:
    def test_each_preset_is_packed_with_its_key_label_and_form_state(self):
        """
        GIVEN: A stream declaring one preset of a heading, a paragraph and a list
        WHEN: The block is packed for the editor
        THEN: A fifth argument carries the preset's key, label and the form state of
              its blocks, in order
        """
        [preset] = options(SectionStream())["presets"]

        assert preset["key"] == "introduction"
        assert preset["label"] == "Introduction"
        assert [child["type"] for child in preset["state"]] == [
            "heading",
            "paragraph",
            "links",
        ]
        assert preset["state"][0]["value"] == "Preset heading"

    def test_the_state_carries_ids_as_a_saved_page_would(self):
        """
        GIVEN: A preset built from bare (type, value) pairs and a list of plain dicts
        WHEN: It is packed
        THEN: Every block and list item has an id, because the value went through the
              stored form first
        """
        [preset] = options(SectionStream())["presets"]
        links = preset["state"][2]["value"]

        assert all(child["id"] for child in preset["state"])
        assert links[0]["id"]
        assert links[0]["value"] == {"label": "First link"}

    def test_the_first_four_arguments_are_wagtails_own(self):
        """
        GIVEN: A preset stream
        WHEN: It is packed
        THEN: Its name, child definitions and meta are exactly what Wagtail's StreamBlock
              adapter produces, so the JS parent class receives what it expects
        """
        block = SectionStream()

        ours = packed(block)["_args"]
        wagtails = JSContext().pack(StreamBlockAdapter().js_args(block))

        assert [ours[0], ours[1], ours[3]] == [wagtails[0], wagtails[1], wagtails[3]]
        # Default list items get a fresh id on every pack, so only the shape compares.
        assert ours[2].keys() == wagtails[2].keys()

    def test_a_stream_without_presets_packs_an_empty_list(self):
        """
        GIVEN: A preset stream that declares no presets
        WHEN: It is packed
        THEN: Its preset list is empty, which renders no picker
        """
        assert options(BareStream())["presets"] == []

    def test_a_preset_is_built_each_time_the_editor_renders(self, monkeypatch):
        """
        GIVEN: A preset whose builder counts its calls
        WHEN: The block is packed twice
        THEN: The builder ran twice, so a preset can read the database as it is now
        """
        calls = []

        def build():
            calls.append(1)
            return [("heading", "Counted")]

        block = SectionStream()
        monkeypatch.setattr(
            block.meta, "presets", [Preset("counted", "Counted", build)]
        )

        packed(block)
        packed(block)

        assert len(calls) == 2

    def test_the_picker_assets_follow_wagtails_block_script(self):
        """
        GIVEN: A preset stream
        WHEN: Its editor media is collected
        THEN: The picker's script loads after Wagtail's blocks.js, which it extends, and
              its stylesheet is included
        """
        context = JSContext()
        context.pack(SectionStream())
        scripts = [str(path) for path in context.media._js]

        blocks_js = next(i for i, s in enumerate(scripts) if "telepath/blocks.js" in s)
        presets_js = next(
            i for i, s in enumerate(scripts) if "streamfield-presets.js" in s
        )
        assert blocks_js < presets_js
        assert any(
            "streamfield-presets.css" in str(path)
            for paths in context.media._css.values()
            for path in paths
        )

    def test_the_picker_text_is_packed_alongside_the_presets(self):
        """
        GIVEN: A preset stream
        WHEN: It is packed
        THEN: The picker's label, placeholder, button and confirmation travel with it, the
              confirmation carrying a placeholder for the preset's name
        """
        strings = options(SectionStream())["strings"]

        assert strings["label"] == "Start from a preset"
        assert strings["load"] == "Load"
        assert "%(preset)s" in strings["confirm"]

    def test_a_lazily_translated_label_is_packed_as_text(self, monkeypatch):
        """
        GIVEN: A preset whose label is a lazy translation, as a project's would be
        WHEN: The block is packed
        THEN: The label arrives as a plain string the browser can show
        """
        block = SectionStream()
        lazy = Preset("lazy", gettext_lazy("Lazy label"), lambda: [])
        monkeypatch.setattr(block.meta, "presets", [lazy])

        [preset] = options(block)["presets"]

        assert preset["label"] == "Lazy label"
        assert type(preset["label"]) is str


class TestDefinition:
    def test_presets_stay_out_of_the_constructor_arguments(self):
        """
        GIVEN: A preset stream declaring a preset with a callable builder
        WHEN: It is deconstructed, as makemigrations does
        THEN: No preset appears, so a migration never has to serialise a callable
        """
        _, args, kwargs = SectionStream().deconstruct()

        assert "presets" not in kwargs
        assert "introduction" not in repr(args)

    @pytest.mark.django_db
    def test_editing_a_preset_needs_no_migration(self):
        """
        GIVEN: The test app's migrations, which were generated with its preset in place
        WHEN: makemigrations checks for changes
        THEN: It finds none
        """
        out = StringIO()

        call_command(
            "makemigrations",
            "wagtail_streamfield_presets_test",
            "--check",
            "--dry-run",
            stdout=out,
        )

        assert "No changes detected" in out.getvalue()

    def test_a_repeated_preset_key_is_refused(self):
        """
        GIVEN: A stream declaring two presets under one key
        WHEN: It is instantiated
        THEN: It fails loudly, because the picker could only ever load one of them
        """

        class Clashing(PresetStreamBlock):
            heading = blocks.CharBlock()

            class Meta:
                presets = [
                    Preset("same", "First", list),
                    Preset("same", "Second", list),
                ]

        with pytest.raises(ImproperlyConfigured, match="same"):
            Clashing()


@pytest.mark.django_db
class TestEditor:
    def test_the_create_view_offers_the_presets(self, admin_client):
        """
        GIVEN: A page type whose body is a preset stream
        WHEN: Its create view is opened in the admin
        THEN: The picker's script is on the page and the body's definition carries the
              preset's label
        """
        root = Page.objects.get(depth=1)
        url = f"/admin/pages/add/wagtail_streamfield_presets_test/presetpage/{root.pk}/"

        response = admin_client.get(url)
        body = response.content.decode()

        assert response.status_code == 200
        assert "wagtail_streamfield_presets/js/streamfield-presets.js" in body
        assert "Introduction" in html.unescape(body)

    def test_a_page_saved_from_a_preset_stores_its_blocks(self):
        """
        GIVEN: A page whose body holds a preset's value, as the editor would submit it
        WHEN: It is saved and read back
        THEN: The blocks are all there, so a preset is a plain stream value once saved
        """
        block = SectionStream()
        value = block.preset_value(block.meta.presets[0])
        page = PresetPage(title="From a preset", slug="from-a-preset", body=value)
        Page.objects.get(depth=1).add_child(instance=page)

        stored = list(PresetPage.objects.get(pk=page.pk).body.raw_data)

        assert [child["type"] for child in stored] == ["heading", "paragraph", "links"]
