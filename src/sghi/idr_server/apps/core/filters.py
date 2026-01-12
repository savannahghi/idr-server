from django_filters.rest_framework import FilterSet


class BaseFilterSet(FilterSet):
    """
    The base `FilterSet` from which all other filter sets are derived from.
    """

    ...


class AuditBaseFilterSet(BaseFilterSet):
    """
    The base `FilterSet` from which all other `AuditBase` model filter sets are
    derived from.
    """

    ...
