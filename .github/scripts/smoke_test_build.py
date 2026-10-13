"""Checks a built wheel or sdist on its own: the package imports from the installed copy, not
from the source tree, and Django finds its static files. The test app is left out of the
build on purpose, so the test suite cannot run against it."""

from pathlib import Path

import django

from django.conf import settings


def main():
    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django.contrib.staticfiles",
            "wagtail",
            "wagtail.admin",
            "wagtail_streamfield_presets",
        ],
        STATIC_URL="/static/",
    )
    django.setup()

    from django.contrib.staticfiles import finders

    import wagtail_streamfield_presets.blocks as blocks

    source = Path(__file__).resolve().parents[2] / "src"
    if source in Path(blocks.__file__).resolve().parents:
        raise SystemExit(
            f"Imported from the source tree, not the build: {blocks.__file__}"
        )

    for path in (
        "wagtail_streamfield_presets/js/streamfield-presets.js",
        "wagtail_streamfield_presets/css/streamfield-presets.css",
    ):
        if not finders.find(path):
            raise SystemExit(f"{path} is missing from the build")

    print(f"OK: {blocks.__file__}")


if __name__ == "__main__":
    main()
