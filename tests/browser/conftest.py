import os

import pytest

from wagtail.models import Locale, Page


# Playwright's sync API keeps an event loop running in the main thread for the rest of
# the session, which Django takes for async code and refuses database access from.
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def root():
    """Wagtail's migrations make the locale and root page, but a live server's test
    flushes the database after it, so the next one may have to make them again. A
    serialised rollback can't: once Playwright is running, Django hands out a fresh
    connection that never received the serialised data."""
    Locale.objects.get_or_create(language_code="en")
    return Page.get_first_root_node() or Page.add_root(
        instance=Page(title="Root", slug="root")
    )


def open_create_view(page, live_server, admin_client, root, model):
    session = admin_client.cookies["sessionid"]
    page.context.add_cookies(
        [{"name": "sessionid", "value": session.value, "url": live_server.url}]
    )

    page.goto(
        f"{live_server.url}/admin/pages/add/"
        f"wagtail_streamfield_presets_test/{model}/{root.pk}/"
    )
    return page


@pytest.fixture
def editor(page, live_server, admin_client, root):
    """The admin's create view for a page with a preset stream, logged in as a
    superuser."""
    return open_create_view(page, live_server, admin_client, root, "presetpage")


@pytest.fixture
def labelled_editor(page, live_server, admin_client, root):
    """The same, for a page whose stream names its picker "Start with a set of
    sections"."""
    return open_create_view(page, live_server, admin_client, root, "labelledpresetpage")
