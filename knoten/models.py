from django.db import models
import uuid

# Create your models here.


class Knoten(models.Model):
    id            = models.UUIDField('ID', primary_key=True, default=uuid.uuid4, db_column='knt_id', editable=False)
    #schluessel    = models.CharField('Schluessel', max_length=4096,  default="<ungesetzt>", blank=True, db_column='knt_key')

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'knoten'
        db_table = 'knoten'
        verbose_name = 'Knoten'
        verbose_name_plural = 'Knoten'
        # unique_together = [['bezeichnung',]]


class Verbindung(models.Model):
    id            = models.AutoField('ID', primary_key=True, db_column='vbd_id')
    adresse       = models.URLField('Adresse (URL)', db_column='vbd_adr')
    port          = models.PositiveIntegerField('Port', db_column='vbd_port')
    remote_id     = models.UUIDField('Remote ID', db_column='knt_id', null=True, blank=True)
    knoten        = models.ForeignKey(Knoten, verbose_name='Knoten', 
                                      db_column='knt_idl', on_delete=models.CASCADE, null=True, default=None, blank=True)
    
    class Meta:
        app_label = 'knoten'
        db_table = 'verbindung'
        verbose_name = 'verbindung'
        verbose_name_plural = 'Verbindungen'

