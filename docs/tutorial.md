# Your first preset

This tutorial gives a page type a preset, so editors can fill its body with a ready-made
set of blocks. It assumes a working Wagtail 7.4+ project with a page type that has a
StreamField.

## 1. Install the package

```bash
pip install wagtail-streamfield-presets
```

Add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "wagtail_streamfield_presets",
]
```

## 2. Switch the stream to `PresetStreamBlock`

Say your page has this body:

```python
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.models import Page


class ArticleStream(blocks.StreamBlock):
    heading = blocks.CharBlock()
    paragraph = blocks.RichTextBlock()


class ArticlePage(Page):
    body = StreamField(ArticleStream(), blank=True)
```

Change the base class:

```python
from wagtail_streamfield_presets.blocks import PresetStreamBlock


class ArticleStream(PresetStreamBlock):
    heading = blocks.CharBlock()
    paragraph = blocks.RichTextBlock()
```

Run `python manage.py makemigrations`. It reports no changes: a `PresetStreamBlock` stores
exactly what a `StreamBlock` does, so existing pages are untouched.

## 3. Write a preset

A preset is a function returning blocks as `(block_type, value)` pairs, the same shape you
would use to fill a page's body in code:

```python
from wagtail.rich_text import RichText


def article_outline():
    return [
        ("heading", "[Title]"),
        ("paragraph", RichText("<p>[Opening paragraph]</p>")),
        ("heading", "[Second section]"),
        ("paragraph", RichText("<p>[Its text]</p>")),
    ]
```

The square brackets are a convention, not a requirement: they make an unfinished page
obvious in a preview.

## 4. Offer it on the stream

Declare it in the stream's `Meta`, with a key and the label editors will see:

```python
from wagtail_streamfield_presets.blocks import Preset, PresetStreamBlock


class ArticleStream(PresetStreamBlock):
    heading = blocks.CharBlock()
    paragraph = blocks.RichTextBlock()

    class Meta:
        presets = [Preset("outline", "Article outline", article_outline)]
```

Run `makemigrations` again. Still no changes, which is the point of declaring presets in
`Meta`.

## 5. Try it

Open the editor for a new `ArticlePage`. Above the body there is now **Start from a preset**.
Choose **Article outline** and press **Load**: the four blocks appear, ready to fill in.

Load it again on a page that already has blocks, and the editor asks before replacing them.

## Next steps

- [Start a preset with content from the database](how-to/database-presets.md)
- [Offer several presets on one field](how-to/several-presets.md)
- [Check your presets in tests](how-to/testing-presets.md)
