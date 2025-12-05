"""REST API client for testing REST endpoints."""

from typing import Any

import requests
from requests import Response


class RestClient:
    """A REST API client for making HTTP requests."""

    def __init__(self, base_url: str, headers: dict[str, str] | None = None):
        """Initialize the REST client.

        Args:
            base_url: The base URL for the API.
            headers: Optional default headers to include in all requests.
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make a GET request.

        Args:
            endpoint: The API endpoint (will be appended to base_url).
            params: Optional query parameters.
            headers: Optional headers for this specific request.

        Returns:
            The response object.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.get(url, params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make a POST request.

        Args:
            endpoint: The API endpoint (will be appended to base_url).
            json: Optional JSON body.
            data: Optional form data.
            headers: Optional headers for this specific request.

        Returns:
            The response object.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.post(url, json=json, data=data, headers=headers)

    def put(
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make a PUT request.

        Args:
            endpoint: The API endpoint (will be appended to base_url).
            json: Optional JSON body.
            data: Optional form data.
            headers: Optional headers for this specific request.

        Returns:
            The response object.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.put(url, json=json, data=data, headers=headers)

    def patch(
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make a PATCH request.

        Args:
            endpoint: The API endpoint (will be appended to base_url).
            json: Optional JSON body.
            data: Optional form data.
            headers: Optional headers for this specific request.

        Returns:
            The response object.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.patch(url, json=json, data=data, headers=headers)

    def delete(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make a DELETE request.

        Args:
            endpoint: The API endpoint (will be appended to base_url).
            headers: Optional headers for this specific request.

        Returns:
            The response object.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.delete(url, headers=headers)

    def close(self) -> None:
        """Close the session."""
        self.session.close()
