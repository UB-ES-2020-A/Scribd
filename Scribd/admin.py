from django.contrib import admin

from .models import Ebook, ViewedEbooks, Review, EbookInsertDate, UserTickets
# Register your models here
from .user_model import SubscribedUsers, User, Provider


class EbookAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Ebook)
admin.site.register(Review)
admin.site.register(ViewedEbooks)
admin.site.register(EbookInsertDate)
admin.site.register(User)
admin.site.register(Provider)
admin.site.register(SubscribedUsers)
admin.site.register(UserTickets)

# Configurar el titulo del panel admin
title = "Administration Scribd"
admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = "Management Panel"
