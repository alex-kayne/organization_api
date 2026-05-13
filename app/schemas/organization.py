from datetime import datetime
from typing import Literal, Sequence

from pydantic import BaseModel, Field, model_validator


class DepartmentCreateRequest(BaseModel):
    name: str
    parent_id: int | None

    @model_validator(mode="after")
    def check_data(self) -> 'DepartmentCreateRequest':
        self.name = self.name.strip()
        if len(self.name) > 200:
            raise ValueError("Department name cannot be longer than 200 characters")
        return self


class DepartmentCreateResponse(BaseModel):
    id: int
    message: str = "Department created"


class EmployeeCreateRequest(BaseModel):
    full_name: str
    position: str
    hired_at: datetime | None

    @model_validator(mode="after")
    def check_data(self) -> 'EmployeeCreateRequest':
        self.full_name = self.full_name.strip()
        if len(self.full_name) > 200:
            raise ValueError("Employee full name cannot be longer than 200 characters")

        self.position = self.position.strip()
        if len(self.position) > 200:
            raise ValueError("Employee position cannot be longer than 200 characters")

        return self


class EmployeeCreateResponse(BaseModel):
    id: int
    message: str = "Employee created"


class DepartmentGetRequest(BaseModel):
    depth: int = Field(default=1, le=5)
    include_employees: bool = True


class DepartmentGetResponse(BaseModel):
    department: dict | None
    employees: Sequence[dict] | None
    children: Sequence[dict]


class DepartmentUpdateRequest(BaseModel):
    name: str | None
    parent_id: int | None


class DepartmentUpdateResponse(BaseModel):
    id: int | None
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
