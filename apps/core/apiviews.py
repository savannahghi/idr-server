from rest_framework.viewsets import ModelViewSet


class BaseViewSet(ModelViewSet):
    """
    This is the base `ViewSet` from which all other view sets are derived from.
    """
    ...


class AuditBaseViewSet(BaseViewSet):
    """
    This is the base `ViewSet` for all `AuditBase` models in this project.
    """
    ...
