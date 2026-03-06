import os
import pytest
import requests

STAGING_BASE_URL = os.getenv('STAGING_BASE_URL')
MOD_SERVICE_URL = os.getenv('MOD_SERVICE_URL')

pytestmark = pytest.mark.skipif(not STAGING_BASE_URL or not MOD_SERVICE_URL, reason="Environment not configured")

# Moderation: test that flagged images are caught by moderation service

def test_moderation_block_flagged_image():
    # upload an image known to be flagged (test corpus) and expect moderation status
    url = f"{STAGING_BASE_URL}/api/v1/memes"
    files = {'image': ('nsfw.jpg', b'FAKE_NSFW_BYTES', 'image/jpeg')}
    data = {'text': 'This should be blocked', 'visibility': 'public'}
    resp = requests.post(url, headers={'Authorization': f"Bearer {os.getenv('TEST_USER_TOKEN')}"}, files=files, data=data)
    assert resp.status_code in (200,201,202)
    meme = resp.json()
    # Poll moderation status
    mod_url = f"{MOD_SERVICE_URL}/api/v1/moderation/{meme['id']}"
    r2 = requests.get(mod_url)
    assert r2.status_code == 200
    status = r2.json().get('status')
    assert status in ('blocked','review'), f"Unexpected moderation status: {status}"


def test_moderation_false_positive_rate():
    """Run a small curated safe set through moderation and ensure false positive rate < 5%"""
    # This is a placeholder that requires MOD_SERVICE_URL and corpus
    safe_images = [b'SAFE1', b'SAFE2', b'SAFE3', b'SAFE4', b'SAFE5', b'SAFE6', b'SAFE7', b'SAFE8', b'SAFE9', b'SAFE10']
    blocked = 0
    for i, img in enumerate(safe_images):
        files = {'image': (f'safe{i}.jpg', img, 'image/jpeg')}
        resp = requests.post(f"{STAGING_BASE_URL}/api/v1/memes", headers={'Authorization': f"Bearer {os.getenv('TEST_USER_TOKEN')}"}, files=files, data={'text': 'safe','visibility':'private'})
        assert resp.status_code in (200,201,202)
        meme = resp.json()
        r2 = requests.get(f"{MOD_SERVICE_URL}/api/v1/moderation/{meme['id']}")
        assert r2.status_code == 200
        if r2.json().get('status') == 'blocked':
            blocked += 1
    false_positive_rate = blocked / len(safe_images)
    assert false_positive_rate < 0.05, f"False positive rate too high: {false_positive_rate}"


if __name__ == '__main__':
    pytest.main([__file__])
