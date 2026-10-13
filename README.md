# Wagtail StreamField presets

Give your editors a head start: ready-made sets of blocks they can load into a StreamField
and fill in.

Most pages on a site follow a pattern. A landing page is a hero, a few sections and a call
to action. A recipe is an introduction, a photo, the ingredients and the method. Without
presets, editors rebuild that pattern block by block on every new page.

With presets, an editor picks one from the list above the field and presses **Load**. The
blocks appear, ready to fill in, so the editor's time goes on the words instead of the
layout.

![An editor opens the preset list above a StreamField, chooses Recipe, presses Load, and the recipe's blocks fill the field](https://raw.githubusercontent.com/timonweb/wagtail-streamfield-presets/main/docs/images/editor-picker.gif)

- **Fills the field in the browser.** Nothing reloads, so the title and every other field
  keep what the editor typed.
- **Asks before replacing.** If the field already has blocks, the editor confirms first;
  nothing is saved until the page is.
- **Declared in code, next to the blocks.** A preset is a function that returns blocks, so
  it can start with real content from your database, such as an image from the library.
- **A plain StreamBlock everywhere but the editor.** Rendering, storage, validation and
  migrations are unchanged, so an existing stream can adopt it without touching its data.

## Links

- [Documentation](https://github.com/timonweb/wagtail-streamfield-presets/blob/main/docs/README.md)
- [Changelog](https://github.com/timonweb/wagtail-streamfield-presets/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/timonweb/wagtail-streamfield-presets/blob/main/CONTRIBUTING.md)
- [Security](https://github.com/timonweb/wagtail-streamfield-presets/security)

## Supported versions

Wagtail 7.4 and up, and all
[compatible versions of Python and Django](https://docs.wagtail.org/en/stable/releases/upgrading.html#compatible-django-python-versions):
Python 3.11+ and Django 5.2+.

## Installation

Pick the command for your preferred package installer:

```bash
uv add wagtail-streamfield-presets
poetry add wagtail-streamfield-presets
pip install wagtail-streamfield-presets
```

Then add the app to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "wagtail_streamfield_presets",
]
```

No template or URL wiring is needed. The picker's script and stylesheet travel with the
field's own editor media.

## Usage

Subclass `PresetStreamBlock` instead of `StreamBlock`, and declare presets in its `Meta`:

```python
from wagtail import blocks
from wagtail.rich_text import RichText
from wagtail_streamfield_presets.blocks import Preset, PresetStreamBlock


def article_outline():
    return [
        ("heading", "[Title]"),
        ("paragraph", RichText("<p>[Opening paragraph]</p>")),
    ]


class ArticleStream(PresetStreamBlock):
    heading = blocks.CharBlock()
    paragraph = blocks.RichTextBlock()

    class Meta:
        presets = [Preset("outline", "Article outline", article_outline)]
```

Use it like any StreamBlock: `body = StreamField(ArticleStream())`. Editors now see
**Start from a preset** above the field. Set `preset_picker_label` in the same `Meta` to say
it in your editors' words, such as "Start with a set of sections".

Presets belong in `Meta`, not in the block's constructor arguments: Wagtail writes those into
migrations, and a preset holds a function. Kept in `Meta`, editing a preset never needs a
migration.

The [documentation](https://github.com/timonweb/wagtail-streamfield-presets/blob/main/docs/README.md)
has a tutorial, how-to guides and the full reference.

## License

[BSD-3-Clause](https://github.com/timonweb/wagtail-streamfield-presets/blob/main/LICENSE).
