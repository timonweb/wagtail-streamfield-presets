# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `PresetStreamBlock`: a StreamBlock that offers editors a picker of predefined block sets
  above the field, loading the chosen one into the stream in the browser.
- `Preset(key, label, build)`: a preset declared in the stream's `Meta.presets`, built on
  every editor render so it can start with content from the database.
- Confirmation before a preset replaces blocks already in the field.
- Translatable picker text. No translations ship yet; the interface falls back to English.
- Support for Wagtail 7.4+, Django 5.2+ and Python 3.11+.

<!-- TEMPLATE - keep below to copy for new releases -->
<!--


## [x.y.z] - YYYY-MM-DD

### Added

- ...

### Changed

- ...

### Removed

- ...

-->
