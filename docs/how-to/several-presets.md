# Offer several presets on one field

List them in `Meta.presets`, in the order editors should see them:

```python
class BodyStream(PresetStreamBlock):
    heading = blocks.CharBlock()
    paragraph = blocks.RichTextBlock()
    quote = blocks.BlockQuoteBlock()

    class Meta:
        presets = [
            Preset("news", "News story", news),
            Preset("interview", "Interview", interview),
            Preset("outline", "Blank outline", outline),
        ]
```

## Keys and labels

- **The key** identifies the preset in the picker. It must be unique on the stream:
  repeating one raises `ImproperlyConfigured` when the block is created.
- **The label** is what editors read. Translate it with `gettext_lazy`, as you would any
  other admin text:

```python
from django.utils.translation import gettext_lazy as _

presets = [Preset("news", _("News story"), news)]
```

## Share presets between page types

Two page types that use the same stream class share its presets. To give them different
presets, subclass the stream and override `Meta`:

```python
class NewsBodyStream(BodyStream):
    class Meta:
        presets = [Preset("news", "News story", news)]
```

The subclass stores the same blocks, so moving a page type from one to the other needs no
data migration.
