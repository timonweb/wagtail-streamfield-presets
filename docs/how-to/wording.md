# Word the picker for your editors

Editors meet presets as two pieces of text: the label above the picker, and the name of
each preset in it. Both should tell an editor who has never heard the word "preset" what
**Load** will do.

## Name presets after what they load

A preset's label is read in the list, out of context. Say what the editor gets, not how it
was made:

| Instead of | Prefer |
|---|---|
| Layout 1 | Standard article sections |
| Pillar layout | Standard pillar page sections |
| LP template | Standard landing page sections |

Adding the number of blocks sets expectations before anything is replaced:

```python
presets = [
    Preset("pillar", _("Standard pillar page sections (19)"), pillar_page),
]
```

A count written into a label can fall out of date when the preset changes. Guard it with a
test:

```python
import re


def test_the_label_states_the_preset_size():
    for preset in STREAM.meta.presets:
        count = int(re.search(r"\((\d+)\)", str(preset.label)).group(1))
        assert count == len(STREAM.preset_value(preset))
```

## Name the picker after your site's vocabulary

The default label, "Start from a preset", is deliberately generic. If your editors call
these "sections" or "templates", say so on the stream:

```python
class BodyStream(PresetStreamBlock):
    class Meta:
        presets = [...]
        preset_picker_label = _("Start with a set of sections")
```

The placeholder ("Choose…") and the confirmation never say "preset", so they read correctly
under whatever label you choose.
