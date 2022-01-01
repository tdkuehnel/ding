from django.db import models

# Create your models here.

class {{ klassname }}(models.Model):
    id                      = models.AutoField('ID', primary_key=True, db_column='{{ kuerzel }}_id')
    bezeichnung             = models.CharField('Bezeichnung', max_length=512, default='<unbenannt>', db_column='{{ kuerzel }}_txt')

    def __str__(self):
        return self.bezeichnung

    class Meta:
        app_label            = '{{ app_name }}'
        db_table             = '{{ klassname }}'
        verbose_name         = '{{ klassname }}'
        verbose_name_plural  = '{{ klassname }} (viele)'
        # unique_together = [['bezeichnung',]]
        ordering             = ['bezeichnung']
