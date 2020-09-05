from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from . import models
from tablib import formats

from import_export.admin import ImportExportMixin
from import_export.formats import base_formats
from import_export import resources
from import_export.fields import Field


# use for all admins that are admin.ModelAdmin and use ExportMixin
class ImportExportMixinAdmin(ImportExportMixin, admin.ModelAdmin):

    def get_export_formats(self):
        formats = (
          base_formats.JSON,
          base_formats.XLSX,
          base_formats.CSV,
          )

        return [f for f in formats if f().can_export()]

        def get_import_formats(self):
            formats = (
              base_formats.JSON,
              base_formats.XLSX,
              base_formats.CSV,
              )

            return [f for f in formats if f().can_import()]

    class Meta:
        abstract = True


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
            }),
    )


class OrgUnitResource(resources.ModelResource):
    class Meta:
        model = models.OrgUnit
        skip_unchanged = True
        report_skipped = True



class OrgUnitAdmin(ImportExportMixinAdmin):
    resource_class = OrgUnitResource


class ProcessResource(resources.ModelResource):
    class Meta:
        model = models.Process
        skip_unchanged = True
        report_skipped = True



class ProcessAdmin(ImportExportMixinAdmin):
    resource_class = ProcessResource
    inlines = [
        models.ProcedureInline,
    ]


class ProcedureResource(resources.ModelResource):
    class Meta:
        model = models.Procedure
        skip_unchanged = True
        report_skipped = True


class ProcedureAdmin(ImportExportMixinAdmin):
    resource_class = ProcedureResource
    inlines = [
        models.ActionInline,
    ]


class ActionResource(resources.ModelResource):
    class Meta:
        model = models.Action
#        import_id_fields = ('id', 'procedure', 'in_process_step')
        skip_unchanged = True
        report_skipped = True


class ActionAdmin(ImportExportMixinAdmin):
    resource_class = ActionResource
    inlines = [
        models.WorkTaskInline,
    ]


class WorkTaskResource(resources.ModelResource):
    class Meta:
        model = models.WorkTask
        skip_unchanged = True
        report_skipped = True


class WorkTaskAdmin(ImportExportMixinAdmin):
    resource_class = WorkTaskResource


class BCMActivityResource(resources.ModelResource):
    class Meta:
        model = models.BCMActivity
        skip_unchanged = True
        report_skipped = True


class BCMActivityAdmin(ImportExportMixinAdmin):
    resource_class = BCMActivityResource


class BusinessAppResource(resources.ModelResource):
    class Meta:
        model = models.BusinessApp
        skip_unchanged = True
        report_skipped = True


class BusinessAppAdmin(ImportExportMixinAdmin):
    resource_class = BusinessAppResource


class StakeholderResource(resources.ModelResource):
    class Meta:
        model = models.Stakeholder
        skip_unchanged = True
        report_skipped = True


class StakeholderAdmin(ImportExportMixinAdmin):
    resource_class = StakeholderResource
    fields = (
        ('name', 'type'),
        'description',
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.OrgUnit, OrgUnitAdmin)
admin.site.register(models.Process, ProcessAdmin)
admin.site.register(models.Procedure, ProcedureAdmin)
admin.site.register(models.Action, ActionAdmin)
admin.site.register(models.WorkTask, WorkTaskAdmin)
admin.site.register(models.BCMActivity, BCMActivityAdmin)
admin.site.register(models.BusinessApp, BusinessAppAdmin)
admin.site.register(models.Stakeholder, StakeholderAdmin)
