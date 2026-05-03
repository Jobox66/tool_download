import pytest
from fastapi.testclient import TestClient
from api.index import app
from api.trending import calculate_hot_score, get_trending_feed

client = TestClient(app)

def test_calculate_hot_score():
    score = calculate_hot_score(likes=100, comments=50, shares=10, views=1000)
    assert score == 23.0
    
    score_zero = calculate_hot_score(likes=100, comments=50, shares=10, views=0)
    assert score_zero == 0

def test_get_trending_feed():
    result = get_trending_feed("VN")
    
    assert "success" in result
    assert result["success"] is True
    assert "data" in result
    assert isinstance(result["data"], list)
    
    videos = result["data"]
    if len(videos) >= 2:
        assert videos[0]["hot_score"] >= videos[1]["hot_score"]

def test_api_trending_endpoint():
    response = client.get("/api/trending?region=VN")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) > 0
