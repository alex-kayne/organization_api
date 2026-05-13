from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.api.dependencies import get_organization_service
from app.main import app
from app.schemas.organization import DepartmentCreateRequest


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


class FakeOrganizationService:
    async def create_department(self, payload: DepartmentCreateRequest) -> int | None:
        return 1


@pytest.mark.asyncio
async def test_create_department_success(async_client: AsyncClient):
    app.dependency_overrides[get_organization_service] = lambda: FakeOrganizationService()
    try:
        response = await async_client.post("/departments/", json={"name": "Test Department", "parent_id": None, })
        assert response.status_code == 200
        assert response.json() == {"id": 1, "message": "Department created",}
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_department_empty_name_returns_422(async_client: AsyncClient):
    response = await async_client.post("/departments/", json={"name": "   ", "parent_id": None})
    assert response.status_code == 422
