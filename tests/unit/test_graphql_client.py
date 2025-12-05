"""Unit tests for the GraphQL client using mocking."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from python_test.clients.graphql_client import AsyncGraphQLClient, GraphQLClient


class TestGraphQLClientInit:
    """Tests for GraphQLClient initialization."""

    def test_init_with_endpoint(self):
        """Test that GraphQLClient initializes with correct endpoint."""
        client = GraphQLClient("https://api.example.com/graphql")
        assert client.endpoint == "https://api.example.com/graphql"
        client.close()

    def test_init_with_headers(self):
        """Test that headers are set correctly."""
        headers = {"Authorization": "Bearer token123"}
        client = GraphQLClient("https://api.example.com/graphql", headers=headers)
        assert client.headers.get("Authorization") == "Bearer token123"
        client.close()


class TestGraphQLClientExecute:
    """Tests for GraphQLClient execute method with mocking."""

    @patch("python_test.clients.graphql_client.httpx.Client")
    def test_execute_basic_query(self, mock_client_class):
        """Test executing a basic GraphQL query."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {"user": {"id": "1", "name": "Test User"}}
        }
        mock_response.raise_for_status.return_value = None
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = GraphQLClient("https://api.example.com/graphql")
        result = client.execute("query { user { id name } }")

        assert result["data"]["user"]["name"] == "Test User"
        mock_client.post.assert_called_once()

    @patch("python_test.clients.graphql_client.httpx.Client")
    def test_execute_with_variables(self, mock_client_class):
        """Test executing a GraphQL query with variables."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"user": {"id": "1"}}}
        mock_response.raise_for_status.return_value = None
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = GraphQLClient("https://api.example.com/graphql")
        client.execute(
            "query GetUser($id: ID!) { user(id: $id) { id } }",
            variables={"id": "1"},
        )

        # Verify the payload includes variables
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert payload["variables"] == {"id": "1"}

    @patch("python_test.clients.graphql_client.httpx.Client")
    def test_execute_with_operation_name(self, mock_client_class):
        """Test executing a GraphQL query with operation name."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {}}
        mock_response.raise_for_status.return_value = None
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = GraphQLClient("https://api.example.com/graphql")
        client.execute("query GetUsers { users { id } }", operation_name="GetUsers")

        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert payload["operationName"] == "GetUsers"


class TestGraphQLClientQueryAndMutate:
    """Tests for GraphQLClient query and mutate aliases."""

    @patch("python_test.clients.graphql_client.httpx.Client")
    def test_query_is_alias_for_execute(self, mock_client_class):
        """Test that query() is an alias for execute()."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"items": []}}
        mock_response.raise_for_status.return_value = None
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = GraphQLClient("https://api.example.com/graphql")
        result = client.query("query { items { id } }")

        assert "data" in result
        mock_client.post.assert_called_once()

    @patch("python_test.clients.graphql_client.httpx.Client")
    def test_mutate_is_alias_for_execute(self, mock_client_class):
        """Test that mutate() is an alias for execute()."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"createItem": {"id": "new"}}}
        mock_response.raise_for_status.return_value = None
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = GraphQLClient("https://api.example.com/graphql")
        result = client.mutate("mutation { createItem { id } }")

        assert result["data"]["createItem"]["id"] == "new"
        mock_client.post.assert_called_once()


class TestAsyncGraphQLClientInit:
    """Tests for AsyncGraphQLClient initialization."""

    def test_init_with_endpoint(self):
        """Test that AsyncGraphQLClient initializes with correct endpoint."""
        client = AsyncGraphQLClient("https://api.example.com/graphql")
        assert client.endpoint == "https://api.example.com/graphql"


class TestAsyncGraphQLClientExecute:
    """Tests for AsyncGraphQLClient execute method with mocking."""

    @pytest.mark.asyncio
    @patch("python_test.clients.graphql_client.httpx.AsyncClient")
    async def test_async_execute_basic_query(self, mock_client_class):
        """Test executing a basic GraphQL query asynchronously."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {"user": {"id": "1", "name": "Test User"}}
        }
        mock_response.raise_for_status.return_value = None
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.aclose = AsyncMock()
        mock_client_class.return_value = mock_client

        client = AsyncGraphQLClient("https://api.example.com/graphql")
        result = await client.execute("query { user { id name } }")

        assert result["data"]["user"]["name"] == "Test User"
        mock_client.post.assert_called_once()

    @pytest.mark.asyncio
    @patch("python_test.clients.graphql_client.httpx.AsyncClient")
    async def test_async_execute_with_variables(self, mock_client_class):
        """Test executing an async GraphQL query with variables."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"user": {"id": "1"}}}
        mock_response.raise_for_status.return_value = None
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.aclose = AsyncMock()
        mock_client_class.return_value = mock_client

        client = AsyncGraphQLClient("https://api.example.com/graphql")
        await client.execute(
            "query GetUser($id: ID!) { user(id: $id) { id } }",
            variables={"id": "1"},
        )

        # Verify the payload includes variables
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert payload["variables"] == {"id": "1"}

    @pytest.mark.asyncio
    @patch("python_test.clients.graphql_client.httpx.AsyncClient")
    async def test_async_query_is_alias_for_execute(self, mock_client_class):
        """Test that async query() is an alias for execute()."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"items": []}}
        mock_response.raise_for_status.return_value = None
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.aclose = AsyncMock()
        mock_client_class.return_value = mock_client

        client = AsyncGraphQLClient("https://api.example.com/graphql")
        result = await client.query("query { items { id } }")

        assert "data" in result
        mock_client.post.assert_called_once()

    @pytest.mark.asyncio
    @patch("python_test.clients.graphql_client.httpx.AsyncClient")
    async def test_async_mutate_is_alias_for_execute(self, mock_client_class):
        """Test that async mutate() is an alias for execute()."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"createItem": {"id": "new"}}}
        mock_response.raise_for_status.return_value = None
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.aclose = AsyncMock()
        mock_client_class.return_value = mock_client

        client = AsyncGraphQLClient("https://api.example.com/graphql")
        result = await client.mutate("mutation { createItem { id } }")

        assert result["data"]["createItem"]["id"] == "new"
        mock_client.post.assert_called_once()
