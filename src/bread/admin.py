from django.contrib import admin
from .models import Bread,Bread_Attr


# Register your models here.
class Bread_Attr_Inline(admin.TabularInline):
    model=Bread_Attr
    can_delete=True


class BreadAdmin(admin.ModelAdmin):
    inlines = [
        Bread_Attr_Inline,
    ]

admin.site.register(Bread,BreadAdmin)