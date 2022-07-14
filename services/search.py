from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user', 'role','team']
