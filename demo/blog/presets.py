from wagtail.images import get_image_model
from wagtail.rich_text import RichText


def heading(text):
    return ("heading_block", {"heading_text": text, "size": "h2"})


def paragraph(html):
    return ("paragraph_block", RichText(html))


def recipe():
    """Reads the image library each time the editor opens, so the preset starts with
    whatever photo is there now rather than one fixed at import."""
    photo = get_image_model().objects.order_by("pk").first()

    return [
        paragraph("<p>[A sentence or two on why this bake is worth the effort]</p>"),
        ("image_block", {"image": photo, "caption": "", "attribution": ""}),
        heading("Ingredients"),
        paragraph("<ul><li>[Ingredient]</li><li>[Ingredient]</li></ul>"),
        heading("Method"),
        paragraph("<ol><li>[First step]</li><li>[Second step]</li></ol>"),
    ]


def news():
    return [
        heading("[Headline]"),
        paragraph("<p>[What happened, and why it matters to our customers]</p>"),
        (
            "block_quote",
            {
                "text": "[A line from someone involved]",
                "attribute_name": "[Their name]",
                "settings": {"theme": "default", "text_size": "default"},
            },
        ),
    ]
