# Agents

Important context for AI coding agents working on this project.

## Project overview

Wagtail streamfield presets is a Django/Wagtail package. The source code is in `src/wagtail_streamfield_presets/`, with tests in `tests/` and a demo Wagtail site in `demo/`.

This project was created from the [cookiecutter-wagtail-package](https://github.com/wagtail/cookiecutter-wagtail-package) template and follows the [Wagtail package maintenance guidelines](https://wagtail.org/package-guidelines/).

## Key commands

```sh
just help            # View all commands
just install         # Install Python and Node.js dependencies
just demo            # Run the demo Wagtail site (migrate + load data + runserver)
just test            # Run tests with pytest
just lint            # Run all linters (Ruff, prek, Prettier, Stylelint, ESLint)
just format          # Run all formatters (Ruff, Prettier)
just coverage        # Run tests with coverage report
just makemessages    # Extract messages for translation
just compilemessages # Compile translation message catalogs for use
```

## Quality assurance

- Python: Ruff for linting and formatting (`ruff.toml`), prek hooks (`prek.toml`).
- JavaScript/CSS/JSON/YAML: Prettier for formatting (`prettier.config.js`).
- CSS: Stylelint with `@wagtail/stylelint-config-wagtail` (`stylelint.config.mjs`).
- JavaScript: ESLint with `@wagtail/eslint-config-wagtail` (`eslint.config.mjs`).
- Tests: pytest with pytest-django. Test settings are in `src/wagtail_streamfield_presets/test/settings.py`.
- CI: GitHub Actions in `.github/workflows/`.

Always run `just lint` and `just test` before considering work complete.

## Project layout

```
src/wagtail_streamfield_presets/       # Package source code
src/wagtail_streamfield_presets/test/  # Django test app with settings, URLs
tests/                     # Test modules (pytest)
demo/                      # Demo Wagtail site for development
.github/workflows/         # CI: linting, tests, nightly builds, publishing
```

## Guidelines

- Follow [Semantic Versioning](https://semver.org/) for releases.
- Use [Keep a Changelog](https://keepachangelog.com/) format for CHANGELOG.md.
- CSS should follow the Wagtail stylelint config conventions.
- Refer to [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution workflow.

## Architecture

- `src/wagtail_streamfield_presets/blocks.py` holds the whole Python side: `Preset`,
  `PresetStreamBlock`, and the telepath adapter that adds the presets to the stream's
  editor definition.
- The picker's JavaScript and CSS under `static/` are hand-written and served as-is; there is
  no build step. The script subclasses Wagtail's `StreamBlockDefinition` and uses only its
  constructor, `render()`, `getState()` and `setState()`.
- Presets are declared in a stream's `Meta`, never in constructor arguments, so they stay out
  of migrations. Keep it that way.
- The picker is covered by Playwright smoke tests in `tests/browser/`, marked `browser`, which
  drive the real page editor in Chromium. `just install` fetches Chromium; `just test` runs
  them with the rest. They check loading, the replace confirmation and saving, not layout, so
  after a visual change still look at the picker in the demo (`just demo`).
- `.github/workflows/nightly.yml` runs daily but only tests a Wagtail release from PyPI that
  hasn't passed yet; a cache entry per version records the pass.
