from django.contrib import admin
from .models import Ebook, ViewedEbook, Review, EbookInsertDate

#Register your models here

class EbookAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Ebook)
admin.site.register(Review)
# Configurar el titulo del panel admin
title = "Administration Scribd"
admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = "Management Panel"