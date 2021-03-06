# Generated by Django 3.2.5 on 2022-01-01 00:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('knoten', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='verbindung',
            name='remote_id',
            field=models.UUIDField(blank=True, db_column='knt_id', null=True, verbose_name='Remote ID'),
        ),
        migrations.AlterField(
            model_name='knoten',
            name='id',
            field=models.UUIDField(db_column='knt_id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='verbindung',
            name='knoten',
            field=models.ForeignKey(blank=True, db_column='knt_idl', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='knoten.knoten', verbose_name='Knoten'),
        ),
    ]
