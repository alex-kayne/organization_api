from app.repositories.organization import OrganizationRepository
from app.services.organization import OrganizationService


def get_organization_repository() -> OrganizationRepository:
    return OrganizationRepository()


def get_organization_service() -> OrganizationService:
    return OrganizationService(get_organization_repository())
