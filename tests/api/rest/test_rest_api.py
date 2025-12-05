"""Tests for REST API endpoints using JSONPlaceholder API.

These are integration tests that require network access.
Run with: pytest -m integration
"""

import pytest

pytestmark = pytest.mark.integration


class TestRestApiGet:
    """Tests for REST API GET requests."""

    def test_get_single_post(self, rest_client):
        """Test retrieving a single post."""
        response = rest_client.get("/posts/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "title" in data
        assert "body" in data
        assert "userId" in data

    def test_get_all_posts(self, rest_client):
        """Test retrieving all posts."""
        response = rest_client.get("/posts")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_posts_with_query_params(self, rest_client):
        """Test retrieving posts with query parameters."""
        response = rest_client.get("/posts", params={"userId": 1})

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(post["userId"] == 1 for post in data)

    def test_get_nonexistent_resource(self, rest_client):
        """Test retrieving a nonexistent resource."""
        response = rest_client.get("/posts/9999")

        assert response.status_code == 404


class TestRestApiPost:
    """Tests for REST API POST requests."""

    def test_create_post(self, rest_client):
        """Test creating a new post."""
        new_post = {
            "title": "Test Post",
            "body": "This is a test post body",
            "userId": 1,
        }

        response = rest_client.post("/posts", json=new_post)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == new_post["title"]
        assert data["body"] == new_post["body"]
        assert data["userId"] == new_post["userId"]
        assert "id" in data


class TestRestApiPut:
    """Tests for REST API PUT requests."""

    def test_update_post(self, rest_client):
        """Test updating an existing post."""
        updated_post = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated body content",
            "userId": 1,
        }

        response = rest_client.put("/posts/1", json=updated_post)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == updated_post["title"]
        assert data["body"] == updated_post["body"]


class TestRestApiPatch:
    """Tests for REST API PATCH requests."""

    def test_partial_update_post(self, rest_client):
        """Test partially updating an existing post."""
        partial_update = {"title": "Patched Title"}

        response = rest_client.patch("/posts/1", json=partial_update)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == partial_update["title"]


class TestRestApiDelete:
    """Tests for REST API DELETE requests."""

    def test_delete_post(self, rest_client):
        """Test deleting a post."""
        response = rest_client.delete("/posts/1")

        assert response.status_code == 200
