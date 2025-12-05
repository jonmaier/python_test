"""GraphQL client for testing GraphQL endpoints."""

from typing import Any

import httpx


class GraphQLClient:
    """A GraphQL client for making GraphQL queries and mutations."""

    def __init__(self, endpoint: str, headers: dict[str, str] | None = None):
        """Initialize the GraphQL client.

        Args:
            endpoint: The GraphQL endpoint URL.
            headers: Optional default headers to include in all requests.
        """
        self.endpoint = endpoint
        self.headers = headers or {}
        self._client = httpx.Client(headers=self.headers)

    def execute(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Execute a GraphQL query or mutation.

        Args:
            query: The GraphQL query or mutation string.
            variables: Optional variables for the query.
            operation_name: Optional operation name.
            headers: Optional headers for this specific request.

        Returns:
            The response data as a dictionary.
        """
        payload: dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = variables
        if operation_name:
            payload["operationName"] = operation_name

        request_headers = {**self.headers}
        if headers:
            request_headers.update(headers)

        response = self._client.post(
            self.endpoint,
            json=payload,
            headers=request_headers,
        )
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        return result

    def query(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Execute a GraphQL query.

        This is an alias for execute() for better readability when making queries.

        Args:
            query: The GraphQL query string.
            variables: Optional variables for the query.
            operation_name: Optional operation name.
            headers: Optional headers for this specific request.

        Returns:
            The response data as a dictionary.
        """
        return self.execute(query, variables, operation_name, headers)

    def mutate(
        self,
        mutation: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Execute a GraphQL mutation.

        This is an alias for execute() for better readability when making mutations.

        Args:
            mutation: The GraphQL mutation string.
            variables: Optional variables for the mutation.
            operation_name: Optional operation name.
            headers: Optional headers for this specific request.

        Returns:
            The response data as a dictionary.
        """
        return self.execute(mutation, variables, operation_name, headers)

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()


class AsyncGraphQLClient:
    """An async GraphQL client for making GraphQL queries and mutations."""

    def __init__(self, endpoint: str, headers: dict[str, str] | None = None):
        """Initialize the async GraphQL client.

        Args:
            endpoint: The GraphQL endpoint URL.
            headers: Optional default headers to include in all requests.
        """
        self.endpoint = endpoint
        self.headers = headers or {}
        self._client = httpx.AsyncClient(headers=self.headers)

    async def execute(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Execute a GraphQL query or mutation asynchronously.

        Args:
            query: The GraphQL query or mutation string.
            variables: Optional variables for the query.
            operation_name: Optional operation name.
            headers: Optional headers for this specific request.

        Returns:
            The response data as a dictionary.
        """
        payload: dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = variables
        if operation_name:
            payload["operationName"] = operation_name

        request_headers = {**self.headers}
        if headers:
            request_headers.update(headers)

        response = await self._client.post(
            self.endpoint,
            json=payload,
            headers=request_headers,
        )
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        return result

    async def query(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Execute a GraphQL query asynchronously.

        This is an alias for execute() for better readability when making queries.

        Args:
            query: The GraphQL query string.
            variables: Optional variables for the query.
            operation_name: Optional operation name.
            headers: Optional headers for this specific request.

        Returns:
            The response data as a dictionary.
        """
        return await self.execute(query, variables, operation_name, headers)

    async def mutate(
        self,
        mutation: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Execute a GraphQL mutation asynchronously.

        This is an alias for execute() for better readability when making mutations.

        Args:
            mutation: The GraphQL mutation string.
            variables: Optional variables for the mutation.
            operation_name: Optional operation name.
            headers: Optional headers for this specific request.

        Returns:
            The response data as a dictionary.
        """
        return await self.execute(mutation, variables, operation_name, headers)

    async def close(self) -> None:
        """Close the async HTTP client."""
        await self._client.aclose()
