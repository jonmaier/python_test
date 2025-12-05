"""Tests for GraphQL API endpoints using Countries API.

These are integration tests that require network access.
Run with: pytest -m integration
"""

import pytest

pytestmark = pytest.mark.integration


class TestGraphQLQuery:
    """Tests for GraphQL queries."""

    def test_query_single_country(self, graphql_client):
        """Test querying a single country by code."""
        query = """
            query GetCountry($code: ID!) {
                country(code: $code) {
                    name
                    code
                    capital
                    currency
                }
            }
        """
        variables = {"code": "US"}

        result = graphql_client.query(query, variables=variables)

        assert "data" in result
        assert result["data"]["country"]["name"] == "United States"
        assert result["data"]["country"]["code"] == "US"
        assert result["data"]["country"]["capital"] == "Washington D.C."

    def test_query_multiple_countries(self, graphql_client):
        """Test querying multiple countries."""
        query = """
            query {
                countries {
                    code
                    name
                }
            }
        """

        result = graphql_client.query(query)

        assert "data" in result
        assert isinstance(result["data"]["countries"], list)
        assert len(result["data"]["countries"]) > 0

    def test_query_country_with_continent(self, graphql_client):
        """Test querying a country with its continent information."""
        query = """
            query GetCountryWithContinent($code: ID!) {
                country(code: $code) {
                    name
                    continent {
                        name
                        code
                    }
                }
            }
        """
        variables = {"code": "FR"}

        result = graphql_client.query(query, variables=variables)

        assert "data" in result
        assert result["data"]["country"]["name"] == "France"
        assert result["data"]["country"]["continent"]["name"] == "Europe"

    def test_query_continent(self, graphql_client):
        """Test querying a continent."""
        query = """
            query GetContinent($code: ID!) {
                continent(code: $code) {
                    name
                    code
                    countries {
                        name
                    }
                }
            }
        """
        variables = {"code": "EU"}

        result = graphql_client.query(query, variables=variables)

        assert "data" in result
        assert result["data"]["continent"]["name"] == "Europe"
        assert result["data"]["continent"]["code"] == "EU"
        assert isinstance(result["data"]["continent"]["countries"], list)


class TestAsyncGraphQLQuery:
    """Tests for async GraphQL queries."""

    @pytest.mark.asyncio
    async def test_async_query_country(self, async_graphql_client):
        """Test async querying a single country."""
        query = """
            query GetCountry($code: ID!) {
                country(code: $code) {
                    name
                    code
                    capital
                }
            }
        """
        variables = {"code": "GB"}

        result = await async_graphql_client.query(query, variables=variables)

        assert "data" in result
        assert result["data"]["country"]["name"] == "United Kingdom"
        assert result["data"]["country"]["code"] == "GB"

    @pytest.mark.asyncio
    async def test_async_query_languages(self, async_graphql_client):
        """Test async querying languages."""
        query = """
            query {
                languages {
                    code
                    name
                }
            }
        """

        result = await async_graphql_client.query(query)

        assert "data" in result
        assert isinstance(result["data"]["languages"], list)
        assert len(result["data"]["languages"]) > 0
