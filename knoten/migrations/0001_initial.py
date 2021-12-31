# Generated by Django 3.2.5 on 2021-12-31 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Verbindung',
            fields=[
                ('id', models.AutoField(db_column='vbd_id', primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.URLField(db_column='vbd_adr', verbose_name='Adresse (URL)')),
                ('port', models.PositiveIntegerField(db_column='vbd_port', verbose_name='Port')),
            ],
            options={
                'verbose_name': 'verbindung',
                'verbose_name_plural': 'Verbindungen',
                'db_table': 'verbindung',
            },
        ),
        migrations.CreateModel(
            name='Knoten',
            fields=[
                ('id', models.UUIDField(db_column='knt_id', primary_key=True, serialize=False, verbose_name='ID')),
                ('knoten_links', models.ForeignKey(blank=True, db_column='knt_idl', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='knoten_links', to='knoten.verbindung', verbose_name='Knoten links')),
                ('knoten_neu', models.ForeignKey(blank=True, db_column='knt_idn', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='knoten_neu', to='knoten.verbindung', verbose_name='Knoten neu')),
                ('knoten_rechts', models.ForeignKey(blank=True, db_column='knt_idr', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='knoten_rechts', to='knoten.verbindung', verbose_name='Knoten rechts')),
            ],
            options={
                'verbose_name': 'Knoten',
                'verbose_name_plural': 'Knoten',
                'db_table': 'knoten',
            },
        ),
    ]