# Python Test Automation Framework

A Python test automation framework for API testing, supporting both REST and GraphQL APIs. Built with Python 3.12 and PyTest.

## Features

- **REST API Testing**: Full support for GET, POST, PUT, PATCH, DELETE operations using the `requests` library
- **GraphQL API Testing**: Synchronous and asynchronous GraphQL clients using `httpx`
- **PyTest Integration**: Organized test structure with fixtures and markers
- **Type Safety**: Full type hints with mypy validation
- **Code Quality**: Linting with ruff

## Requirements

- Python 3.12 or higher

## Installation

```bash
# Clone the repository
git clone https://github.com/jonmaier/python_test.git
cd python_test

# Install in development mode
pip install -e ".[dev]"
```

## Project Structure

```
python_test/
├── src/
│   └── python_test/
│       └── clients/
│           ├── rest_client.py      # REST API client
│           └── graphql_client.py   # GraphQL clients (sync and async)
├── tests/
│   ├── api/
│   │   ├── rest/                   # REST API integration tests
│   │   └── graphql/                # GraphQL integration tests
│   ├── unit/                       # Unit tests with mocking
│   └── conftest.py                 # Shared fixtures
├── pyproject.toml                  # Project configuration
└── README.md
```

## Usage

### REST API Client

```python
from python_test.clients.rest_client import RestClient

# Create a client
client = RestClient("https://api.example.com", headers={"Authorization": "Bearer token"})

# Make requests
response = client.get("/users")
response = client.post("/users", json={"name": "John"})
response = client.put("/users/1", json={"name": "Jane"})
response = client.patch("/users/1", json={"name": "Jane Doe"})
response = client.delete("/users/1")

# Always close when done
client.close()
```

### GraphQL Client

```python
from python_test.clients.graphql_client import GraphQLClient

# Create a client
client = GraphQLClient("https://api.example.com/graphql")

# Execute a query
result = client.query("""
    query GetUser($id: ID!) {
        user(id: $id) {
            name
            email
        }
    }
""", variables={"id": "1"})

# Execute a mutation
result = client.mutate("""
    mutation CreateUser($input: UserInput!) {
        createUser(input: $input) {
            id
            name
        }
    }
""", variables={"input": {"name": "John"}})

client.close()
```

### Async GraphQL Client

```python
import asyncio
from python_test.clients.graphql_client import AsyncGraphQLClient

async def main():
    client = AsyncGraphQLClient("https://api.example.com/graphql")
    
    result = await client.query("""
        query {
            users {
                id
                name
            }
        }
    """)
    
    await client.close()

asyncio.run(main())
```

## Running Tests

```bash
# Run all unit tests (no network required)
pytest -v -m "not integration"

# Run integration tests (requires network access)
pytest -v -m integration

# Run all tests
pytest -v

# Run with coverage
pytest --cov=python_test
```

## Development

### Code Quality

```bash
# Run linter
ruff check .

# Fix linting issues
ruff check . --fix

# Run type checker
mypy src/
```

## Future Roadmap

- [ ] Web UI testing (Selenium/Playwright)
- [ ] Database testing utilities
- [ ] Performance testing integration
- [ ] Test reporting and dashboards
- [ ] CI/CD integration examples