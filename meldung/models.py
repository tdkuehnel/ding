from django.db import models

from knoten.models import Knoten

# Create your models here.

class Meldung(models.Model):
    """
    Meldung, welche innerhalb der Anwendung im rechten Fenster erscheint.  Eine Meldung ist eine
    Kommunikationseinheit, welche herumgeschickt und zur Anzeige gebracht wird. Anfangs wird das nur
    Text sein, spÃ¤ter auch Grafiken ud Dateien.
    """
    
    id            = models.AutoField('ID', primary_key=True, db_column='mdng_id')
    text          = models.CharField('Meldungstext', max_length=4096,  default="<ungesetzt>", blank=True, db_column='mdng_txt')
    knoten        = models.ForeignKey('Knoten', verbose_name='zugehörigerKnoten', db_column='knt_id', on_delete=models.CASCADE, null=True, default=None, blank=True)
    
    class Meta:
        app_label = 'meldung'
        db_table = "meldung"
        verbose_name_plural = "Meldungen"
        verbose_name = "Meldung"
