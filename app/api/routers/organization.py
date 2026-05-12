from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_organization_service
from app.schemas.organization import DepartmentCreateRequest, DepartmentCreateResponse, EmployeeCreateRequest, \
    EmployeeCreateResponse, DepartamentGetRequest, DepartmentGetResponse, DepartmentUpdateRequest, \
    DepartmentUpdateResponse, DepartmentDeleteRequest, DepartmentDeleteResponse
from app.services.organization import OrganizationService

router = APIRouter()


@router.post("/departments/", tags=["Organization"], response_model=DepartmentCreateResponse)
async def create_department(payload: DepartmentCreateRequest,
                            organization_service: OrganizationService = Depends(
                                get_organization_service)) -> DepartmentCreateResponse:
    """
    Department creation
    """
    return DepartmentCreateResponse()


@router.post("/departments/{department_id}/employees/", tags=["Organization"], response_model=EmployeeCreateResponse)
async def create_employee_in_department(department_id: int,
                                        payload: EmployeeCreateRequest,
                                        organization_service: OrganizationService = Depends(
                                            get_organization_service)) -> EmployeeCreateResponse:
    """
    Employee creation
    """
    return EmployeeCreateResponse()


@router.get("/departments/{department_id}", tags=["Organization"], response_model=DepartmentGetResponse)
async def get_department(department_id: int,
                         payload: Annotated[DepartamentGetRequest, Query()],
                         organization_service: OrganizationService = Depends(
                             get_organization_service)) -> DepartmentGetResponse:
    """
    Department retrieval
    """

    return DepartmentGetResponse()


@router.patch("/departments/{department_id}", tags=["Organization"], response_model=DepartmentUpdateResponse)
async def update_department(department_id: int,
                            payload: DepartmentUpdateRequest) -> DepartmentUpdateResponse:
    """
    Department updating
    """
    return DepartmentUpdateResponse()


@router.delete("/departments/{department_id}", tags=["Organization"], response_model=DepartmentDeleteResponse)
async def delete_department(department_id: int,
                            payload: DepartmentDeleteRequest) -> DepartmentDeleteResponse:
    """
    Department deleting
    """
    return DepartmentDeleteResponse()
