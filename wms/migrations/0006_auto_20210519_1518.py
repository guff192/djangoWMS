# Generated by Django 3.2.3 on 2021-05-19 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0005_auto_20210519_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='date',
            field=models.DateField(help_text='DD.MM.YYYY'),
        ),
        migrations.AlterField(
            model_name='goodinstance',
            name='best_before',
            field=models.DateField(blank=True, help_text='DD.MM.YYYY', null=True, verbose_name='Best before'),
        ),
        migrations.AlterField(
            model_name='goodinstance',
            name='manufactured',
            field=models.DateField(help_text='DD.MM.YYYY', null=True),
        ),
    ]
