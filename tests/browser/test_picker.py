import re

import pytest

from playwright.sync_api import Page, expect

from wagtail_streamfield_presets.test.models import PresetPage


pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]


def load(editor: Page, label="Introduction"):
    editor.get_by_label("Start from a preset").select_option(label=label)
    editor.get_by_role("button", name="Load", exact=True).click()


def expect_introduction(editor: Page):
    expect(editor.locator('[name="body-0-value"]')).to_have_value("Preset heading")
    expect(editor.locator('[name="body-1-value"]')).to_have_value("Preset paragraph")
    expect(editor.locator('[name="body-2-value-0-value-label"]')).to_have_value(
        "First link"
    )
    expect(editor.locator('[name="body-count"]')).to_have_value("3")


def test_a_preset_fills_an_empty_stream(editor):
    """
    GIVEN: The create view of a page whose body offers the "Introduction" preset
    WHEN: The editor chooses it and presses Load
    THEN: The body holds the preset's heading, paragraph and list, with no confirmation
          asked, and the picker is reset
    """
    editor.on("dialog", lambda dialog: pytest.fail(f"Unexpected {dialog.type}"))

    load(editor)

    expect_introduction(editor)
    expect(editor.get_by_label("Start from a preset")).to_have_value("")


def test_loading_over_existing_blocks_asks_first(editor):
    """
    GIVEN: A body already filled from the preset, then edited
    WHEN: The preset is loaded again, the confirmation dismissed and then accepted
    THEN: Dismissing keeps the edit; accepting replaces the blocks rather than adding to
          them
    """
    heading = editor.locator('[name="body-0-value"]')
    load(editor)
    heading.fill("Edited heading")

    editor.once("dialog", lambda dialog: dialog.dismiss())
    load(editor)
    expect(heading).to_have_value("Edited heading")

    editor.once("dialog", lambda dialog: dialog.accept())
    load(editor)
    expect_introduction(editor)


def test_a_page_saved_from_a_preset_stores_its_blocks(editor):
    """
    GIVEN: A new page whose body was loaded from a preset
    WHEN: It is saved as a draft
    THEN: The stored body holds the preset's blocks and values
    """
    title = editor.locator("#id_title")
    title.fill("From a preset")
    # Wagtail copies the title into the slug on blur, which `fill` alone doesn't cause, and
    # after a short delay, so saving straight away can find the slug still empty.
    title.blur()
    expect(editor.locator("#id_slug")).to_have_value("from-a-preset")
    load(editor)

    editor.get_by_role("button", name="Save draft").click()
    expect(editor).to_have_url(re.compile(r"/admin/pages/\d+/edit/"))

    body = PresetPage.objects.get().get_latest_revision_as_object().body
    assert [(child.block_type, child.value) for child in body][:2] == [
        ("heading", "Preset heading"),
        ("paragraph", "Preset paragraph"),
    ]
    assert body[2].value[0]["label"] == "First link"


def test_a_stream_can_name_its_picker(labelled_editor):
    """
    GIVEN: The create view of a page whose stream sets `preset_picker_label`
    WHEN: The editor finds the picker by that label, chooses a preset and presses Load
    THEN: The preset loads, and the placeholder reads "Choose…"
    """
    picker = labelled_editor.get_by_label("Start with a set of sections")
    expect(picker.locator("option").first).to_have_text("Choose…")

    picker.select_option(label="Introduction")
    labelled_editor.get_by_role("button", name="Load", exact=True).click()

    expect_introduction(labelled_editor)
