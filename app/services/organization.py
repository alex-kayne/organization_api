from app.repositories.organization import OrganizationRepository


class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository) -> None:
        self.organization_repository = organization_repository
