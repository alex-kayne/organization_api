from typing import Annotated
from urllib import response

from fastapi import APIRouter, Depends, Query, Response, status

from app.api.dependencies import get_organization_service
from app.schemas.organization import DepartmentCreateRequest, DepartmentCreateResponse, EmployeeCreateRequest, \
    EmployeeCreateResponse, DepartmentGetRequest, DepartmentGetResponse, DepartmentUpdateRequest, \
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
    if not (department_id := await organization_service.create_department(payload)):
        response.status_code = status.HTTP_404_NOT_FOUND
        return DepartmentCreateResponse(id=payload.parent_id, message="Department name can not be duplicated")
    return DepartmentCreateResponse(id=department_id)


@router.post("/departments/{department_id}/employees/", tags=["Organization"], response_model=EmployeeCreateResponse)
async def create_employee(department_id: int,
                          payload: EmployeeCreateRequest,
                          response: Response,
                          organization_service: OrganizationService = Depends(
                              get_organization_service)) -> EmployeeCreateResponse:
    """
    Employee creation
    """
    if not (employee_id := await organization_service.create_employee(department_id, payload)):
        response.status_code = status.HTTP_404_NOT_FOUND
        return EmployeeCreateResponse(id=department_id, message="Department id not found")

    return EmployeeCreateResponse(id=employee_id)


@router.get("/departments/{department_id}", tags=["Organization"], response_model=DepartmentGetResponse)
async def get_department(department_id: int,
                         payload: Annotated[DepartmentGetRequest, Query()],
                         organization_service: OrganizationService = Depends(
                             get_organization_service)) -> DepartmentGetResponse:
    """
    Department retrieval
    """
    return await organization_service.get_department(department_id, payload)


@router.patch("/departments/{department_id}", tags=["Organization"], response_model=DepartmentUpdateResponse)
async def update_department(department_id: int,
                            payload: DepartmentUpdateRequest,
                            organization_service: OrganizationService = Depends(
                                get_organization_service)
                            ) -> DepartmentUpdateResponse:
    """
    Department updating
    """
    if not (updated_id := await organization_service.update_department(department_id, payload)):
        return DepartmentUpdateResponse(id=payload.parent_id, message="Wrong department parent id")
    return DepartmentUpdateResponse(id=updated_id)


@router.delete("/departments/{department_id}", tags=["Organization"], response_model=DepartmentDeleteResponse)
async def delete_department(department_id: int,
                            payload: DepartmentDeleteRequest,
                            organization_service: OrganizationService = Depends(
                                get_organization_service)) -> DepartmentDeleteResponse:
    """
    Department deleting
    """
    await organization_service.delete_department(department_id, payload)
    return DepartmentDeleteResponse()
