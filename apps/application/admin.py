from django.contrib import admin
from .models import (
    Speciality, Specialist, Equipment, Branch,
    Application, ApplicationBranch
)


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "speciality", "created_at")
    search_fields = ("full_name",)
    list_filter = ("speciality",)
    autocomplete_fields = ("speciality",)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "speciality", "created_at")
    search_fields = ("name",)
    list_filter = ("speciality",)
    autocomplete_fields = ("speciality",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "created_at")
    search_fields = ("name", "address")
    ordering = ("name",)


# Inline ko‘rinish uchun
class ApplicationBranchInline(admin.TabularInline):
    model = ApplicationBranch
    extra = 1
    autocomplete_fields = ("branch", "specialities", "specialists", "equipments")
    filter_horizontal = ("specialities", "specialists", "equipments")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id", "app_id", "full_name", "phone", "email",
        "status", "created_at"
    )
    search_fields = ("app_id", "full_name", "phone", "email")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
    inlines = [ApplicationBranchInline]


@admin.register(ApplicationBranch)
class ApplicationBranchAdmin(admin.ModelAdmin):
    list_display = ("id", "application", "branch", "created_at")
    list_filter = ("branch", "application__status")
    search_fields = ("application__app_id", "branch__name")
    autocomplete_fields = ("application", "branch", "specialities", "specialists", "equipments")
    filter_horizontal = ("specialities", "specialists", "equipments")
