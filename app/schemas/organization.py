from datetime import datetime
from typing import Literal, Sequence, Annotated

from pydantic import BaseModel, Field, model_validator, StringConstraints

NameStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]


class DepartmentCreateRequest(BaseModel):
    name: str = NameStr
    parent_id: int | None


class DepartmentCreateResponse(BaseModel):
    id: int
    message: str = "Department created"


class EmployeeCreateRequest(BaseModel):
    full_name: NameStr
    position: NameStr
    hired_at: datetime | None


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
