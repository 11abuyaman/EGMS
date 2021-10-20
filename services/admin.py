from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional',
            {
                'fields': (
                    'type', 'national_number', 'verified', 'profile_picture', 'gender','country'
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Medicine)
admin.site.register(PeriodicMedication)
admin.site.register(Result)
admin.site.register(Appointment)
admin.site.register(Department)
