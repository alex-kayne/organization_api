from sqlalchemy import insert, select, Integer, update, delete, func
from typing import Sequence
from app.models.organization import Department, Employee
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.organization import DepartmentCreateRequest, DepartmentCreateResponse, EmployeeCreateRequest, \
    EmployeeCreateResponse, DepartmentGetRequest, DepartmentGetResponse, DepartmentUpdateRequest, \
    DepartmentUpdateResponse, DepartmentDeleteRequest, DepartmentDeleteResponse


class OrganizationRepository:
    async def create_department(self, async_session: AsyncSession, payload: DepartmentCreateRequest) -> int:
        dt_now = datetime.now()
        department = insert(Department).values(name=payload.name,
                                               parent_id=payload.parent_id,
                                               created_at=dt_now).returning(Department.id)
        result = await async_session.execute(department)
        return result.fetchone()[0]

    async def create_employee(self, async_session: AsyncSession, department_id: int,
                              payload: EmployeeCreateRequest) -> int:
        dt_now = datetime.now()
        employee = insert(Employee).values(department_id=department_id,
                                           full_name=payload.full_name,
                                           position=payload.position,
                                           hired_at=payload.hired_at,
                                           created_at=dt_now).returning(Department.id)
        result = await async_session.execute(employee)
        return result.fetchone()[0]

    async def get_employee(self, async_session: AsyncSession, department_id: int) -> Sequence[Employee]:
        state = select(Employee).where(Employee.department_id == department_id).order_by(Employee.created_at)
        result = await async_session.scalars(state)
        return result.all()

    async def get_department(self, async_session: AsyncSession, department_id: int) -> Department | None:
        state = select(Department).where(Department.id == department_id)
        result = await async_session.execute(state)
        return result.scalar_one_or_none()

    async def get_departmen_by(self, async_session: AsyncSession, parent_department_id: int,
                               name: str) -> Department | None:
        state = select(Department).where(Department.parent_id == parent_department_id, Department.name == name)
        result = await async_session.execute(state)
        return result.scalar_one_or_none()

    async def get_department_tree_recursive(self, async_session: AsyncSession, department_id: int, max_depth: int) -> \
            Sequence[
                Department]:
        hierarchy_cte = (
            select(Department, Integer.with_variant(Integer, "postgresql").label("level")).filter(
                Department.parent_id == department_id).cte(name="hierarchy", recursive=True)
        )

        hierarchy_cte = hierarchy_cte.union_all(
            select(Department, (hierarchy_cte.c.level + 1).label("level")).join(hierarchy_cte,
                                                                                Department.parent_id == hierarchy_cte.c.id).where(
                hierarchy_cte.c.level < max_depth)
        )

        stmt = select(hierarchy_cte)

        result = await async_session.scalars(stmt)
        return result.all()

    async def check_department_tree_conflicts(self, async_session: AsyncSession, department_id: int,
                                              parent_department_id: int) -> bool | None:
        hierarchy_cte = (
            select(Department).filter(
                Department.parent_id == department_id).cte(name="hierarchy", recursive=True)
        )

        hierarchy_cte = hierarchy_cte.union_all(
            select(Department).join(hierarchy_cte,
                                    Department.parent_id == hierarchy_cte.c.id).where(
            )
        )

        final_query = (
            func.exists(select(hierarchy_cte.c.id).where(hierarchy_cte.c.id == parent_department_id))
        )

        return await async_session.scalar(final_query)

    async def update_department(self, async_session: AsyncSession, department_id: int,
                                payload: DepartmentUpdateRequest) -> int | None:
        stmt = (
            update(Department)
            .where(Department.id == department_id)
            .values(name=payload.name, parent_id=payload.parent_id)
            .returning(Department.id)
        )

        result = await async_session.execute(stmt)

        updated_id = result.scalar()

        return updated_id

    async def delete_department_cascade(self, async_session: AsyncSession, department_id: int) -> None:
        stmt = delete(Department).where(Department.id == department_id)
        await async_session.execute(stmt)
        return None

    async def delete_department_reassign(self, async_session: AsyncSession, reassign_to_department_id: int,
                                         department_id: int) -> None:
        stmt = update(Department).where(Department.parent_id == department_id).values(
            parent_id=reassign_to_department_id)
        await async_session.execute(stmt)

        stmt = update(Employee).where(Employee.department_id == department_id).values(
            department_id=reassign_to_department_id)
        await async_session.execute(stmt)

        stmt = delete(Department).where(Department.id == department_id)
        await async_session.execute(stmt)

        return None
