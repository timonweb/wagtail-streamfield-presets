# API reference

Everything public lives in `wagtail_streamfield_presets.blocks`.

## `Preset`

```python
Preset(key: str, label: str, build: Callable[[], list])
```

A frozen dataclass describing one preset.

| Field | Meaning |
|---|---|
| `key` | Identifies the preset in the picker. Unique within a stream. |
| `label` | The text editors see in the picker. Plain or lazily translated text. |
| `build` | A function taking no arguments and returning the preset's blocks. |

`build` returns a list of `(block_type, value)` pairs, the same shape you would assign to a
page's StreamField in code. Values are what each child block accepts in Python: strings,
`RichText` for rich text, dicts for StructBlocks, lists for ListBlocks, and model instances
for chooser blocks.

`build` runs every time the editor renders a field offering the preset.

## `PresetStreamBlock`

```python
class PresetStreamBlock(wagtail.blocks.StreamBlock)
```

A StreamBlock that offers presets in the editor. Declare child blocks on it exactly as on
a StreamBlock.

### `Meta.presets`

A sequence of `Preset`. Defaults to an empty tuple, which shows no picker.

Declare it in `Meta`, never as a constructor argument. Wagtail serialises a block's
constructor arguments into migrations, and a `Preset` holds a function, which a migration
cannot represent. `Meta` options are not serialised, so adding, removing or editing a preset
needs no migration.

Raises `ImproperlyConfigured` on instantiation if two presets share a key.

### `preset_value(preset) -> StreamValue`

The value the editor receives for `preset`. The result of `preset.build()` goes through the
stream's stored form and back, so every block and list item has an id, as on a saved page.
Use it in tests and anywhere a preset's content is needed outside the editor.

### `preset_states() -> list[dict]`

The packed form the editor receives: `[{"key": ..., "label": ..., "state": ...}]`, where
`state` is the stream's form state for `preset_value(preset)`. Called by the block's
adapter; rarely needed directly.

## The editor

The picker is rendered above the field for every `PresetStreamBlock` that declares at least
one preset.

- **Load** replaces the whole stream with the chosen preset. It never appends.
- If the stream already has blocks, the editor is asked to confirm first.
- Nothing is saved until the page is saved.
- Blocks loaded from a preset start expanded, even when the stream is configured
  `collapsed=True`; Wagtail collapses only the blocks present when the field first renders.

## Translations

The picker's text ("Start from a preset", "Choose a preset…", "Load" and the confirmation)
is translated with Django's `gettext` on the server, in the editor's language. Preset
labels are yours to translate, with `gettext_lazy`.

## Static files

The adapter adds `wagtail_streamfield_presets/js/streamfield-presets.js` and
`wagtail_streamfield_presets/css/streamfield-presets.css` to the field's media, after
Wagtail's own `telepath/blocks.js`. No template changes are needed.

The stylesheet reads two custom properties, with defaults. Set them on any ancestor of the
field, `:root` included, to retune the spacing:

| Property | Default | Controls |
|---|---|---|
| `--streamfield-presets-spacing` | `1rem` | Space below the picker. |
| `--streamfield-presets-gap` | `0.5rem` | Space between the select and the button. |
