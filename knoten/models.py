from django.db import models

# Create your models here.

class Knoten(models.Model):
    id            = models.AutoField('ID', primary_key=True, db_column='knt_id')
    schluessel    = models.CharField('Schluessel', max_length=4096,  default="<ungesetzt>", blank=True, db_column='knt_key')
    knoten_links  = models.ForeignKey('Knoten', verbose_name='Knoten links',  db_column='knt_idl', on_delete=models.CASCADE, null=True, default=None, blank=True)
    knoten_rechts = models.ForeignKey('Knoten', verbose_name='Knoten rechts', db_column='knt_idr', on_delete=models.CASCADE, null=True, default=None, blank=True)
    knoten_neu    = models.ForeignKey('Knoten', verbose_name='Knoten neu',    db_column='knt_idn', on_delete=models.CASCADE, null=True, default=None, blank=True)


    class Meta:
        app_label = 'knoten'
        db_table = "knoten"
        verbose_name_plural = "Knoten"
        verbose_name = "Knoten"
