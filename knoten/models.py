from django.db import models

# Create your models here.

class Verbindung(models.Model):
    id            = models.AutoField('ID', primary_key=True, db_column='vbd_id')
    adresse       = models.URLField('Adresse (URL)', db_column='vbd_adr')
    port          = models.PositiveIntegerField('Port', db_column='vbd_port')
    
    class Meta:
        app_label = 'knoten'
        db_table = 'verbindung'
        verbose_name = 'verbindung'
        verbose_name_plural = 'Verbindungen'


class Knoten(models.Model):
    id            = models.UUIDField('ID', primary_key=True, db_column='knt_id')
    #schluessel    = models.CharField('Schluessel', max_length=4096,  default="<ungesetzt>", blank=True, db_column='knt_key')
    knoten_links  = models.ForeignKey(Verbindung, verbose_name='Knoten links', related_name='knoten_links',
                                      db_column='knt_idl', on_delete=models.CASCADE, null=True, default=None, blank=True)
    knoten_rechts = models.ForeignKey(Verbindung, verbose_name='Knoten rechts', related_name='knoten_rechts',
                                      db_column='knt_idr', on_delete=models.CASCADE, null=True, default=None, blank=True)
    knoten_neu    = models.ForeignKey(Verbindung, verbose_name='Knoten neu', related_name='knoten_neu',
                                      db_column='knt_idn', on_delete=models.CASCADE, null=True, default=None, blank=True)

    class Meta:
        app_label = 'knoten'
        db_table = 'knoten'
        verbose_name = 'Knoten'
        verbose_name_plural = 'Knoten'
