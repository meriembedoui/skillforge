"""Environment configuration; local secrets never enter the repository."""
import os
import secrets
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


def env_bool(name, default=False):
    value = os.environ.get(name, str(default)).lower().strip()
    if value not in {'true', 'false', '1', '0'}:
        raise ImproperlyConfigured(f'{name} must be true/false or 1/0.')
    return value in {'true', '1'}


def secret_key(base_dir: Path, debug: bool):
    configured = os.environ.get('DJANGO_SECRET_KEY', '').strip()
    if configured:
        return configured
    if not debug:
        raise ImproperlyConfigured('DJANGO_SECRET_KEY is required when DEBUG=False.')
    path = base_dir / '.development-secret'
    try:
        with path.open('x', encoding='utf-8') as stream:
            stream.write(secrets.token_urlsafe(64))
        path.chmod(0o600)
    except FileExistsError:
        pass
    value = path.read_text(encoding='utf-8').strip()
    if len(value) < 50:
        raise ImproperlyConfigured('Local development secret is invalid.')
    return value
