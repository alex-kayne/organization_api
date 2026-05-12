from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.models.organization import Departament, Employee


class DepartmentCreateRequest(BaseModel):
    name: str
    parent_id: int | None


class DepartmentCreateResponse(BaseModel):
    id: int
    message: str = "Department created"


class EmployeeCreateRequest(BaseModel):
    full_name: str
    position: str
    hired_at: datetime | None


class EmployeeCreateResponse(BaseModel):
    id: int
    message: str = "Employee created"


class DepartamentGetRequest(BaseModel):
    depth: int = Field(default=1, le=5)
    include_employees: bool = True


class DepartmentGetResponse(BaseModel):
    department: Departament
    employees: list[Employee] | None
    children: list[Departament]


class DepartmentUpdateRequest(BaseModel):
    name: str | None
    parent_id: int | None


class DepartmentUpdateResponse(BaseModel):
    id: int
    message: str = "Department updated"


class DepartmentDeleteRequest(BaseModel):
    mode: Literal["cascade", "reassign"]
    reassign_to_department_id: int | None

    @model_validator(mode="after")
    def check_data(self) -> 'DepartmentDeleteRequest':
        if self.mode == "reassign" and not self.reassign_to_department_id:
            raise ValueError("Department id cannot be reassigned")
        return self


class DepartmentDeleteResponse(BaseModel):
    message: str = "Department deleted"

