import os
import pytest
import requests

STAGING_BASE_URL = os.getenv('STAGING_BASE_URL')

pytestmark = pytest.mark.skipif(not STAGING_BASE_URL, reason="STAGING_BASE_URL not set")

# Helper utilities

def create_auth_headers(token=None):
    if not token:
        token = os.getenv('TEST_USER_TOKEN')
    return {'Authorization': f'Bearer {token}'}

# Functional tests: upload, edit, share

def test_upload_image_ok():
    """Upload a small PNG image and expect 201 with meme id and accessible URL"""
    url = f"{STAGING_BASE_URL}/api/v1/memes"
    files = {'image': ('test.png', b'\x89PNG\r\n\x1a\n', 'image/png')}
    data = {'text': 'Test meme', 'visibility': 'public'}
    resp = requests.post(url, headers=create_auth_headers(), files=files, data=data)
    assert resp.status_code == 201, f"Expected 201, got {resp.status_code}, body={resp.text}"
    body = resp.json()
    assert 'id' in body and 'url' in body


def test_upload_large_image_rejected_or_processed():
    """Upload a large image (>10MB). Expect either 413 or 201 with server-side processing."""
    url = f"{STAGING_BASE_URL}/api/v1/memes"
    large_bytes = b'a' * (11 * 1024 * 1024)
    files = {'image': ('large.jpg', large_bytes, 'image/jpeg')}
    data = {'text': 'Large', 'visibility': 'public'}
    resp = requests.post(url, headers=create_auth_headers(), files=files, data=data)
    assert resp.status_code in (201, 413, 400), f"Unexpected status: {resp.status_code}"


def test_edit_meme_ok():
    """Edit an existing meme's text and expect 200 and updated fields"""
    # create first
    url = f"{STAGING_BASE_URL}/api/v1/memes"
    files = {'image': ('test.png', b'\x89PNG\r\n\x1a\n', 'image/png')}
    data = {'text': 'Original', 'visibility': 'public'}
    resp = requests.post(url, headers=create_auth_headers(), files=files, data=data)
    assert resp.status_code == 201
    meme_id = resp.json()['id']

    edit_url = f"{STAGING_BASE_URL}/api/v1/memes/{meme_id}"
    resp2 = requests.put(edit_url, headers=create_auth_headers(), json={'text': 'Edited'})
    assert resp2.status_code == 200
    assert resp2.json().get('text') == 'Edited'


def test_share_link_accessible_without_auth():
    """Share link should be accessible without auth when visibility=public"""
    # create public meme
    url = f"{STAGING_BASE_URL}/api/v1/memes"
    files = {'image': ('test.png', b'\x89PNG\r\n\x1a\n', 'image/png')}
    data = {'text': 'ShareMe', 'visibility': 'public'}
    resp = requests.post(url, headers=create_auth_headers(), files=files, data=data)
    assert resp.status_code == 201
    meme = resp.json()
    public_url = meme['url']

    resp2 = requests.get(public_url)
    assert resp2.status_code == 200


def test_permissions_owner_only_edit():
    """Only the owner may edit/delete; others get 403"""
    url = f"{STAGING_BASE_URL}/api/v1/memes"
    files = {'image': ('test.png', b'\x89PNG\r\n\x1a\n', 'image/png')}
    data = {'text': 'OwnerTest', 'visibility': 'private'}
    resp = requests.post(url, headers=create_auth_headers(), files=files, data=data)
    assert resp.status_code == 201
    meme_id = resp.json()['id']

    edit_url = f"{STAGING_BASE_URL}/api/v1/memes/{meme_id}"
    # attempt edit with another user's token
    other_headers = {'Authorization': f"Bearer {os.getenv('TEST_OTHER_TOKEN')}"}
    resp2 = requests.put(edit_url, headers=other_headers, json={'text': 'Hacked'})
    assert resp2.status_code == 403


if __name__ == '__main__':
    pytest.main([__file__])
