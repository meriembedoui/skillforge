"""Shared infrastructure tests only: no business apps, fixtures or models."""
import os
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.staticfiles import finders
from django.contrib.messages.storage.base import Message
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.urls import resolve
from django.views.defaults import permission_denied, server_error

from config.environment import env_bool, secret_key
from core.templatetags.skillforge_ui import page_query


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings, self.ids, self.links, self.styles = 0, set(), [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.headings += tag == 'h1'
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            self.styles.append(attrs['href'])


@override_settings(ALLOWED_HOSTS=['testserver'])
class PresentationTests(SimpleTestCase):
    def test_home_routes_assets_and_anchors(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        markup = Markup()
        markup.feed(response.content.decode('utf-8-sig'))
        self.assertEqual(markup.headings, 1)
        self.assertIn('contenu-principal', markup.ids)
        self.assertIn('lang="fr"', response.content.decode())
        for url in markup.links:
            if url.startswith('#'):
                self.assertIn(url[1:], markup.ids)
            else:
                self.assertEqual(url.split('#')[0], '/')
                if '#' in url:
                    self.assertIn(url.split('#')[1], markup.ids)
        for asset in markup.styles:
            self.assertTrue(finders.find(asset.removeprefix('/static/')))
        self.assertTrue(finders.find('js/main.js'))
        self.assertEqual(resolve('/admin/').namespace, 'admin')

    @override_settings(DEBUG=False, SECURE_SSL_REDIRECT=False)
    def test_real_404_and_error_handlers(self):
        self.assertContains(self.client.get('/does-not-exist/'), 'Page introuvable', status_code=404)
        request = RequestFactory().get('/')
        self.assertContains(permission_denied(request, Exception()), 'Accès refusé', status_code=403)
        self.assertContains(server_error(request), 'Une erreur est survenue', status_code=500)

    def test_layouts_render_without_business_context(self):
        request = RequestFactory().get('/')
        for layout in ['learner', 'mentor', 'admin']:
            with self.subTest(layout=layout):
                html = render_to_string(f'layouts/{layout}.html', request=request)
                markup = Markup()
                markup.feed(html)
                self.assertEqual(markup.headings, 1)
                self.assertIn('Modules à venir', html)
                for stylesheet in markup.styles:
                    self.assertTrue(finders.find(stylesheet.removeprefix('/static/')))

    def test_pagination_preserves_filters_and_escapes_query(self):
        request = RequestFactory().get('/?tag=a&tag=b&q=%22%3E&page=1')
        url = page_query({'request': request}, 2)
        self.assertIn('tag=a&tag=b', url)
        self.assertIn('page=2', url)
        html = render_to_string('components/pagination.html', {
            'page_obj': Paginator(range(5), 2).page(2),
        }, request=request)
        self.assertIn('Page précédente', html)
        self.assertIn('Page suivante', html)
        self.assertIn('&amp;', html)

    def test_shared_components_escape_untrusted_content(self):
        html = render_to_string('components/breadcrumbs.html', {
            'breadcrumbs': [{'label': '<script>bad()</script>', 'url': '/'}],
        })
        self.assertNotIn('<script>', html)
        self.assertIn('aria-current="page"', html)

    def test_messages_name_their_state_in_french_and_escape_content(self):
        html = render_to_string('components/messages.html', {
            'messages': [Message(40, '<script>bad()</script>'), Message(25, 'OK')],
        })
        self.assertIn('Erreur', html)
        self.assertIn('Succès', html)
        self.assertIn('role="alert"', html)
        self.assertIn('role="status"', html)
        self.assertNotIn('<script>', html)


class EnvironmentTests(SimpleTestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_local_secret_persists_and_production_requires_environment(self):
        with TemporaryDirectory() as directory:
            path = Path(directory)
            first = secret_key(path, True)
            self.assertGreaterEqual(len(first), 50)
            self.assertEqual(first, secret_key(path, True))
            with self.assertRaises(ImproperlyConfigured):
                secret_key(path, False)

    @patch.dict(os.environ, {'DEBUG': 'typo'}, clear=True)
    def test_invalid_boolean_fails_closed(self):
        with self.assertRaises(ImproperlyConfigured):
            env_bool('DEBUG')
