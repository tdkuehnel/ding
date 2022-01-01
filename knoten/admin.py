from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django import forms

from .models import Knoten
from .models import Verbindung

# Register your models here.

class VerbindungInline(admin.TabularInline):
    model = Verbindung
    extra = 0
    show_change_link = True

@admin.register(Verbindung)
class VerbindungAdmin(SimpleHistoryAdmin):
    #form = KnotenAdminForm
    #list_filter = ['bezeichnung']
    filter_horizontal = [
        #'quellen',
    ]

class KnotenAdminForm(forms.ModelForm):

    class Meta:
        model = Knoten
        fields = [
            #'id',
        ]
        widgets = {
            #'id'         : forms.Textarea(attrs={'cols': 120, 'rows': 2}),
        }

class KnotenInline(admin.TabularInline):
    model = Knoten
    extra = 0
    show_change_link = True

@admin.register(Knoten)
class KnotenAdmin(SimpleHistoryAdmin):
    form = KnotenAdminForm
    readonly_fields = ('id',)
    #list_filter = ['bezeichnung']
    filter_horizontal = [
        #'quellen',
    ]
    inlines = [
        VerbindungInline,
    ]

