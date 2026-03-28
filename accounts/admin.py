from django.contrib import admin
from .models import User, Company


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "role", "company")
    search_fields = ("email", "username")
    list_filter = ("role", "company")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")