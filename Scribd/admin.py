from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Ebook, Review, ViewedEbooks, EbookInsertDate, UserTickets, Forum, Discussion
# Register your models here
from .user_models import User, providerProfile, supportProfile, userProfile


class EbookAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


class CustomUserAdmin(UserAdmin):
    # add_form = RegisterForm, Subscription
    # form = RegisterForm
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Information", {'fields': ('is_provider', 'is_support', 'is_suscribed')}),)


admin.site.register(User, CustomUserAdmin)
admin.site.register(providerProfile)
admin.site.register(supportProfile)
admin.site.register(userProfile)
admin.site.register(Ebook)
admin.site.register(Review)
admin.site.register(ViewedEbooks)
admin.site.register(EbookInsertDate)
admin.site.register(UserTickets)
admin.site.register(Forum)
admin.site.register(Discussion)
# Configurar el titulo del panel admin
title = "Administration Scribd"
admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = "Management Panel"
