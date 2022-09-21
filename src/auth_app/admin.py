from django.contrib import admin

from src.auth_app.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "image",
        "email",
        "is_staff",
        "is_active",
    )


admin.site.register(User, UserAdmin)
