import pytest
from pydantic import ValidationError

from app.schemas.organization import DepartmentCreateRequest, EmployeeCreateRequest


def test_department_name_is_trimmed():
    payload = DepartmentCreateRequest(name="  Backend  ", parent_id=None)
    assert payload.name == "Backend"


def test_department_name_can_not_be_empty_after_trim():
    with pytest.raises(ValidationError):
        DepartmentCreateRequest(name=" ", parent_id=1)


def test_employee_fields_are_trimmed():
    payload = EmployeeCreateRequest(full_name="  Backend  ", position=" Engineer ", hired_at=None)
    assert payload.full_name == "Backend"
    assert payload.position == "Engineer"
    assert payload.hired_at is None
