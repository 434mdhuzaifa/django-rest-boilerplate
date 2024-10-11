from django.contrib import admin
from userAuth.models import *
# Register your models here.

class ResetAdmin(admin.ModelAdmin):
    list_display=["id","user","token","created_at","is_expired"]
admin.site.register(ResetToken,ResetAdmin)
