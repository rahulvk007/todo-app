from .models import *
from django.contrib import admin
from .search import *

admin.site.register(Profile)
admin.site.register(Work)
admin.site.register(Progress)
