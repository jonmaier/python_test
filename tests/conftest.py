"""Test configuration and fixtures for API tests."""

import pytest

from python_test.clients.graphql_client import AsyncGraphQLClient, GraphQLClient
from python_test.clients.rest_client import RestClient


@pytest.fixture
def rest_client():
    """Create a REST client for testing with JSONPlaceholder API."""
    client = RestClient("https://jsonplaceholder.typicode.com")
    yield client
    client.close()


@pytest.fixture
def graphql_client():
    """Create a GraphQL client for testing with Countries API."""
    client = GraphQLClient("https://countries.trevorblades.com/graphql")
    yield client
    client.close()


@pytest.fixture
async def async_graphql_client():
    """Create an async GraphQL client for testing with Countries API."""
    client = AsyncGraphQLClient("https://countries.trevorblades.com/graphql")
    yield client
    await client.close()
