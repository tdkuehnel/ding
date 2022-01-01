from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import SimpleListFilter

from .models import Benutzer

admin.site.site_header = 'ding'

# Register your models here.

# admin.site.register(Benutzer, UserAdmin)


class UserCreateForm(UserCreationForm):

    class Meta:
        model = Benutzer
        fields = ('username', 'password1', 'password2')

class BeispielFilter(SimpleListFilter):
    """ Beispielfilter """
    title= 'beispiel'
    parameter_name = 'beispiel'

    def lookups(self, request, model_admin):
        return (
            ('01','beispiel'),
        )
    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset.all()
        return queryset.filter(username__startswith=self.value())
    
class BenutzerAdmin(UserAdmin):
    add_form = UserCreateForm
    list_display = ('get_name', 'is_staff', 'is_active',)
    list_filter = (BeispielFilter, 'is_staff', 'is_active',)
    filter_horizontal = ('groups', 'user_permissions')
    search_fields = ['username']
    ordering = ['username']
    fieldsets = (
        ('Standardinformationen', {
            'fields': ('username', 'email',)
        }),
        ('Systeminformationen', {
            'classes': ('collapse',),
            'fields': ( 'password', ('is_active', 'is_staff', 'is_superuser'), 'groups', 'user_permissions', ('last_login', 'date_joined'))
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }
        ),
    )
    def get_name(self, obj):
        return obj.get_name()
    get_name.short_description = 'Name'
    
admin.site.register(Benutzer, BenutzerAdmin)
