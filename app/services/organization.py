from app.db.session import async_session_maker
from app.repositories.organization import OrganizationRepository
from app.schemas.organization import DepartmentCreateRequest, EmployeeCreateRequest, \
    DepartmentGetRequest, DepartmentGetResponse, DepartmentUpdateRequest, \
    DepartmentDeleteRequest


class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository) -> None:
        self.organization_repository = organization_repository

    async def create_department(self, payload: DepartmentCreateRequest) -> int | None:
        async with async_session_maker().begin() as session:
            if payload.parent_id is not None and await (self.organization_repository.get_departmen_by(session, payload.parent_id, payload.name)):
                return None
            return await self.organization_repository.create_department(session, payload)

    async def create_employee(self, department_id: int, payload: EmployeeCreateRequest) -> int | None:
        async with async_session_maker().begin() as session:
            if (await self.organization_repository.get_department(session, department_id)) is None:
                return None
            return await self.organization_repository.create_employee(session, department_id, payload)

    async def get_department(self, department_id: int, payload: DepartmentGetRequest) -> DepartmentGetResponse:
        employees = None
        department = None
        async with async_session_maker().begin() as session:
            department = await self.organization_repository.get_department(session, department_id)

            if payload.include_employees:
                employees = await self.organization_repository.get_employee(session, department_id)

            department_tree = await self.organization_repository.get_department_tree_recursive(session, department_id,
                                                                                               payload.depth)
        return DepartmentGetResponse(department=department, employees=employees, children=department_tree)

    async def update_department(self, department_id: int, payload: DepartmentUpdateRequest) -> int | None:
        async with async_session_maker().begin() as session:
            if payload.parent_id is not None and (await self.organization_repository.check_department_tree_conflicts(session, department_id, payload.parent_id)):
                return None
            return await self.organization_repository.update_department(session, department_id, payload)

    async def delete_department(self, department_id: int, payload: DepartmentDeleteRequest) -> None:
        async with async_session_maker().begin() as session:
            if payload.mode == "cascade":
                await self.organization_repository.delete_department_cascade(session, department_id)
            else:
                await self.organization_repository.delete_department_reassign(session,
                                                                              payload.reassign_to_department_id,
                                                                              department_id)
