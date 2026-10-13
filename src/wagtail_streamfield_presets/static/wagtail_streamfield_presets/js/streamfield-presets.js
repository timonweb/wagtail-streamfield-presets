(() => {
  const { StreamBlockDefinition } = window.wagtailStreamField.blocks;

  function el(tag, attrs, text) {
    const node = document.createElement(tag);
    Object.entries(attrs).forEach(([name, value]) =>
      node.setAttribute(name, value),
    );
    if (text) node.textContent = text;
    return node;
  }

  class PresetStreamBlockDefinition extends StreamBlockDefinition {
    constructor(
      name,
      groupedChildBlockDefs,
      initialChildStates,
      meta,
      options,
    ) {
      super(name, groupedChildBlockDefs, initialChildStates, meta);
      this.presets = options.presets;
      this.strings = options.strings;
    }

    render(placeholder, prefix, initialState, initialError) {
      // Placed before the placeholder, which the stream replaces with its own markup, so
      // nothing here depends on how the stream builds its DOM.
      const picker = this.presets.length ? this.renderPicker(prefix) : null;
      if (picker) placeholder.before(picker.root);

      const block = super.render(
        placeholder,
        prefix,
        initialState,
        initialError,
      );

      if (picker) {
        picker.button.addEventListener('click', () =>
          this.load(block, picker.select),
        );
      }
      return block;
    }

    renderPicker(prefix) {
      const id = `${prefix}-preset`;
      const root = el('div', { class: 'streamfield-presets' });
      const label = el(
        'label',
        { class: 'w-field__label', for: id },
        this.strings.label,
      );
      const controls = el('div', { class: 'streamfield-presets__controls' });
      // No name, so the choice is never submitted with the page.
      const select = el('select', { id });
      select.append(el('option', { value: '' }, this.strings.placeholder));
      this.presets.forEach((preset) => {
        select.append(el('option', { value: preset.key }, preset.label));
      });
      const button = el(
        'button',
        { type: 'button', class: 'button button-secondary' },
        this.strings.load,
      );

      controls.append(select, button);
      root.append(label, controls);
      return { root, select, button };
    }

    load(block, select) {
      const preset = this.presets.find(
        (candidate) => candidate.key === select.value,
      );
      if (!preset) return;

      const replace =
        block.getState().length === 0 ||
        window.confirm(
          this.strings.confirm.replace('%(preset)s', () => preset.label),
        );
      if (!replace) return;

      block.setState(preset.state);
      select.value = '';
    }
  }

  window.telepath.register(
    'wagtail_streamfield_presets.PresetStreamBlock',
    PresetStreamBlockDefinition,
  );
})();
