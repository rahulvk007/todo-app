from .models import *
from django.contrib import admin
from .search import *

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Work)
admin.site.register(Progress)
