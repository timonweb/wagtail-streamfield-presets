# Start a preset with content from the database

A preset's function runs each time the editor opens a page that offers it, not once at
import. It can therefore query the database, and the editor starts with content that
exists now.

## Use an image from the library

Return the image instance itself as the chooser's value:

```python
from wagtail.images import get_image_model
from wagtail.rich_text import RichText


def recipe():
    photo = get_image_model().objects.filter(title__startswith="Recipe: ").first()

    return [
        ("paragraph", RichText("<p>[Why this bake is worth the effort]</p>")),
        ("image", {"image": photo, "caption": "", "attribution": ""}),
    ]
```

If no image matches, `photo` is `None` and the editor sees an empty chooser, the same as
a block added by hand. A preset does not have to be complete; it has to be a good start.

## Use snippets, pages or documents

Chooser blocks take model instances in the same way: a snippet for a
`SnippetChooserBlock`, a page for a `PageChooserBlock`, a document for a
`DocumentChooserBlock`.

```python
from myapp.models import Testimonial


def landing_page():
    return [
        ("hero", {"heading": "[Headline]", "testimonial": Testimonial.objects.first()}),
    ]
```

## Keep it cheap

The function runs on every editor load for every preset the field offers. A handful of
indexed queries is fine; anything slow belongs in a cache or behind a simpler default.
