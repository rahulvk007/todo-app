from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'role', 'team')
    search_fields = ['user', 'role','team']
