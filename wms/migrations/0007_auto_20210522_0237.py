# Generated by Django 3.2.3 on 2021-05-21 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0006_auto_20210519_1518'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='good',
            options={'ordering': ['article']},
        ),
        migrations.AlterField(
            model_name='bill',
            name='date',
            field=models.DateField(blank=True, help_text='DD.MM.YYYY', null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='operation',
            field=models.CharField(choices=[('arr', 'Arrival'), ('dep', 'Departure'), ('ord', 'Order')], default='dep', help_text='Type of operation', max_length=3),
        ),
        migrations.AlterField(
            model_name='goodinstance',
            name='manufactured',
            field=models.DateField(blank=True, help_text='DD.MM.YYYY', null=True),
        ),
        migrations.AlterField(
            model_name='row',
            name='storage',
            field=models.CharField(choices=[('HRS', 'Стеллаж'), ('PAL', 'Паллета')], default='HRS', help_text='Type of storage (e.g. High Rack Storage, Pallet)', max_length=3),
        ),
    ]
