from django.contrib import admin
from django.http import HttpRequest
from .models import TransferModel, UserProfile

class ProfileInline(admin.StackedInline):
    model = UserProfile.transition.through
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    
class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        ProfileInline,
        ]   
    fields = ['profile', 'money', 'avatar',]
    readonly_fields = ('profile',)
    list_display = ['profile', 'money']
    
class TransferInline(admin.StackedInline):
    model = UserProfile.transition.through
    extra = 0
    def has_view_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        False
    def has_add_permission(self, request, obj=None):
        return False
    
class TransferAdmin(admin.ModelAdmin):
    inlines = [
        TransferInline,
        ]
    readonly_fields = ('date', 'translation_money', 'user', 'other_user', 'read_status_sender', 'read_status_recipient')
    list_display = ['date', 'translation_money', 'user', 'other_user', 'commentary']

admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(TransferModel, TransferAdmin)
# Register your models here.
