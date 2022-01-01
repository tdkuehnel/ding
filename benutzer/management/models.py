from django.db import models

# Create your models here.

class (models.Model):
    id                      = models.AutoField('ID', primary_key=True, db_column='_id')
    bezeichnung             = models.CharField('Bezeichnung', max_length=512, default='<unbenannt>', db_column='_txt')

    def __str__(self):
        return self.bezeichnung

    class Meta:
        app_label            = ''
        db_table             = ''
        verbose_name         = ''
        verbose_name_plural  = ' (viele)'
        # unique_together = [['bezeichnung',]]
        ordering             = ['bezeichnung']
