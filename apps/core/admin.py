from django.contrib import admin

from .models import GenericSource


class BaseModelAdmin(admin.ModelAdmin):
    """
    This is the base `ModelAdmin` for this project
    """
    ...


class AuditBaseModelAdmin(BaseModelAdmin):
    """
    This is the base `ModelAdmin` for all `AuditBaseModel` models in this
    project.
    """
    date_hierarchy = "updated_at"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fieldsets = (
        #     self.audit_details_fieldset,
        # )
        self.readonly_fields = (
            "created_at", "created_by", "updated_at", "updated_by"
        )

    @property
    def audit_details_fieldset(self):
        """
        Returns a field set containing the necessary fields needed to audit a
        model instance.

        :return: a field set of fields that define/hold audit data.
        """
        return (
            "Audit Details", {
                "classes": ("collapse",),
                "fields": (
                    "created_at", "created_by", "updated_at", "updated_by"
                )
            }
        )

    def save_model(self, request, obj, form, change):
        """
        Persist a model instance to the database.
        """
        # Get the logged on user
        user = request.user

        # If we are changing the object, call obj.update and pass the logged
        # on user
        # if change:
        #     obj.update(user)
        # Otherwise, call obj.save and pass the user
        obj.save(user)


@admin.register(GenericSource)
class GenericSourceAdmin(AuditBaseModelAdmin):
    list_display = ("name", "description")
