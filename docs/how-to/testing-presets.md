# Check your presets in tests

A preset is code, and the blocks it returns can drift from the stream's definition: a
block renamed, a required field added, a `block_counts` rule tightened. Nothing fails
until an editor loads it. A test catches it first.

## Validate every preset against the stream

`preset_value()` builds a preset exactly as the editor receives it. Run it through the
stream's own `clean()`, which applies the rules a publish applies:

```python
import pytest

from myapp.models import ArticlePage

STREAM = ArticlePage._meta.get_field("body").stream_block


@pytest.mark.django_db
@pytest.mark.parametrize("preset", STREAM.meta.presets, ids=lambda p: p.key)
def test_every_preset_passes_the_publish_rules(preset):
    STREAM.clean(STREAM.preset_value(preset))
```

Parametrising over `meta.presets` means a preset added later is tested without anyone
remembering to add a case.

`clean()` raises for required fields left empty, so a preset that deliberately leaves an
image chooser blank fails here. Either give it a value in tests, or test the parts that
must hold, such as block order and counts, instead:

```python
def test_the_outline_has_its_sections_in_order():
    value = STREAM.preset_value(STREAM.meta.presets[0])

    assert [child.block_type for child in value] == ["heading", "paragraph"]
```

## Render it

To prove a preset renders, save its value on a page and fetch it:

```python
from wagtail.models import Site


@pytest.mark.django_db
def test_the_outline_renders(client):
    root = Site.objects.get(is_default_site=True).root_page
    page = ArticlePage(
        title="Outline", body=STREAM.preset_value(STREAM.meta.presets[0])
    )
    root.add_child(instance=page)

    assert client.get(page.url).status_code == 200
```
