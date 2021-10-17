from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class CustomUserAdmin(UserAdmin):
    # list_display = UserAdmin.list_display + ('is_patient', 'national_number',)
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional',
            {
                'fields': (
                    'type', 'national_number', 'verified', 'profile_picture'
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Medicine)
admin.site.register(Result)
admin.site.register(Appointment)
admin.site.register(Department)
