def test_health_check(client):
    # checks the / endpoint returns ok
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_shorten_url_returns_short_code(client):
    # checks that shortening a URL gives back a code
    res = client.post("/shorten", json={"original_url": "https://github.com"})
    assert res.status_code == 201
    assert "short_code" in res.json()
    assert "short_url" in res.json()


def test_shorten_url_clicks_start_at_zero(client):
    # a brand new short URL should have 0 clicks
    res = client.post("/shorten", json={"original_url": "https://github.com"})
    assert res.json()["clicks"] == 0


def test_shorten_url_invalid_input(client):
    # "not-a-url" is not a valid URL — Pydantic should reject it
    res = client.post("/shorten", json={"original_url": "not-a-url"})
    assert res.status_code == 422


def test_custom_code_works(client):
    # user can choose their own short code
    res = client.post("/shorten", json={
        "original_url": "https://youtube.com",
        "custom_code": "yt"
    })
    assert res.status_code == 201
    assert res.json()["short_code"] == "yt"


def test_duplicate_custom_code_returns_409(client):
    # using the same custom code twice should fail with conflict
    client.post("/shorten", json={"original_url": "https://a.com", "custom_code": "dup"})
    res = client.post("/shorten", json={"original_url": "https://b.com", "custom_code": "dup"})
    assert res.status_code == 409


def test_redirect_returns_307(client):
    # visiting a short code should redirect, not return JSON
    create = client.post("/shorten", json={"original_url": "https://github.com"})
    code = create.json()["short_code"]
    res = client.get(f"/{code}", follow_redirects=False)
    assert res.status_code == 307


def test_redirect_points_to_original_url(client):
    # the redirect location must be the original URL
    client.post("/shorten", json={"original_url": "https://github.com"})
    create = client.post("/shorten", json={"original_url": "https://github.com"})
    code = create.json()["short_code"]
    res = client.get(f"/{code}", follow_redirects=False)
    assert "github.com" in res.headers["location"]


def test_redirect_nonexistent_code_returns_404(client):
    # a code that was never created should return 404
    res = client.get("/doesnotexist", follow_redirects=False)
    assert res.status_code == 404


def test_stats_returns_click_count(client):
    # stats endpoint should return the short code and clicks
    create = client.post("/shorten", json={"original_url": "https://github.com"})
    code = create.json()["short_code"]
    res = client.get(f"/stats/{code}")
    assert res.status_code == 200
    assert res.json()["short_code"] == code
    assert "clicks" in res.json()


def test_stats_nonexistent_code_returns_404(client):
    # stats for a made-up code should return 404
    res = client.get("/stats/fakecode")
    assert res.status_code == 404