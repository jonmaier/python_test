"""Unit tests for the REST client using mocking."""

from unittest.mock import MagicMock, patch

from python_test.clients.rest_client import RestClient


class TestRestClientInit:
    """Tests for RestClient initialization."""

    def test_init_with_base_url(self):
        """Test that RestClient initializes with correct base_url."""
        client = RestClient("https://api.example.com")
        assert client.base_url == "https://api.example.com"
        client.close()

    def test_init_strips_trailing_slash(self):
        """Test that trailing slashes are stripped from base_url."""
        client = RestClient("https://api.example.com/")
        assert client.base_url == "https://api.example.com"
        client.close()

    def test_init_with_headers(self):
        """Test that headers are set correctly."""
        headers = {"Authorization": "Bearer token123"}
        client = RestClient("https://api.example.com", headers=headers)
        assert client.session.headers.get("Authorization") == "Bearer token123"
        client.close()


class TestRestClientGet:
    """Tests for RestClient GET method with mocking."""

    @patch("python_test.clients.rest_client.requests.Session")
    def test_get_basic(self, mock_session_class):
        """Test basic GET request."""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "title": "Test Post"}
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = RestClient("https://api.example.com")
        response = client.get("/posts/1")

        assert response.status_code == 200
        assert response.json() == {"id": 1, "title": "Test Post"}
        mock_session.get.assert_called_once_with(
            "https://api.example.com/posts/1", params=None, headers=None
        )

    @patch("python_test.clients.rest_client.requests.Session")
    def test_get_with_params(self, mock_session_class):
        """Test GET request with query parameters."""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = RestClient("https://api.example.com")
        client.get("/posts", params={"userId": 1})

        mock_session.get.assert_called_once_with(
            "https://api.example.com/posts", params={"userId": 1}, headers=None
        )


class TestRestClientPost:
    """Tests for RestClient POST method with mocking."""

    @patch("python_test.clients.rest_client.requests.Session")
    def test_post_with_json(self, mock_session_class):
        """Test POST request with JSON body."""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 101, "title": "New Post"}
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = RestClient("https://api.example.com")
        response = client.post("/posts", json={"title": "New Post", "body": "Content"})

        assert response.status_code == 201
        mock_session.post.assert_called_once()


class TestRestClientPut:
    """Tests for RestClient PUT method with mocking."""

    @patch("python_test.clients.rest_client.requests.Session")
    def test_put_with_json(self, mock_session_class):
        """Test PUT request with JSON body."""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.put.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = RestClient("https://api.example.com")
        response = client.put("/posts/1", json={"title": "Updated"})

        assert response.status_code == 200
        mock_session.put.assert_called_once()


class TestRestClientPatch:
    """Tests for RestClient PATCH method with mocking."""

    @patch("python_test.clients.rest_client.requests.Session")
    def test_patch_with_json(self, mock_session_class):
        """Test PATCH request with JSON body."""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.patch.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = RestClient("https://api.example.com")
        response = client.patch("/posts/1", json={"title": "Patched"})

        assert response.status_code == 200
        mock_session.patch.assert_called_once()


class TestRestClientDelete:
    """Tests for RestClient DELETE method with mocking."""

    @patch("python_test.clients.rest_client.requests.Session")
    def test_delete(self, mock_session_class):
        """Test DELETE request."""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.delete.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = RestClient("https://api.example.com")
        response = client.delete("/posts/1")

        assert response.status_code == 200
        mock_session.delete.assert_called_once_with(
            "https://api.example.com/posts/1", headers=None
        )
