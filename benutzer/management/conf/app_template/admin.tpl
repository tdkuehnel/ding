from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django import forms

from .models import {{ klassname }}

# Register your models here.

class {{ klassname }}AdminForm(forms.ModelForm):

    class Meta:
        model = {{ klassname }}
        fields = [
            'bezeichnung',
        ]
        widgets = {
            'bezeichnung'         : forms.Textarea(attrs={'cols': 120, 'rows': 2}),
        }

class {{ klassname }}Inline(admin.TabularInline):
    model = {{ klassname }}
    extra = 0
    show_change_link = True

@admin.register({{ klassname }})
class {{ klassname }}Admin(SimpleHistoryAdmin):
    form = {{ klassname }}AdminForm
    list_filter = ['bezeichnung']
    filter_horizontal = [
        #'quellen',
    ]
