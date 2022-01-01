from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django import forms

from .models import 

# Register your models here.

class AdminForm(forms.ModelForm):

    class Meta:
        model = 
        fields = [
            'bezeichnung',
        ]
        widgets = {
            'bezeichnung'         : forms.Textarea(attrs={'cols': 120, 'rows': 2}),
        }

class Inline(admin.TabularInline):
    model = 
    extra = 0
    show_change_link = True

@admin.register()
class Admin(SimpleHistoryAdmin):
    form = AdminForm
    list_filter = ['bezeichnung']
    filter_horizontal = [
        #'quellen',
    ]
