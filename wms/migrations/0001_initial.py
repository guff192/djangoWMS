# Generated by Django 3.2.3 on 2021-05-15 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('number', models.PositiveSmallIntegerField(help_text='Number of the bill', primary_key=True, serialize=False)),
                ('operation', models.CharField(choices=[('arr', 'Arrival'), ('dep', 'Departure')], default='dep', help_text='Type of operation', max_length=3)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.PositiveSmallIntegerField(help_text="Number of cell's row on a warehouse scheme")),
                ('column', models.PositiveSmallIntegerField(help_text="Number of cell's column on a warehouse scheme")),
            ],
            options={
                'ordering': ['row', 'column'],
            },
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode', models.CharField(help_text='Product barcode', max_length=128, null=True)),
                ('article', models.CharField(blank=True, help_text='Name of goods', max_length=128)),
                ('weight', models.DecimalField(decimal_places=3, help_text='Weight of a good (in kg)', max_digits=8)),
                ('price', models.PositiveIntegerField(help_text='Price of a good (in cents)')),
                ('fragile', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage', models.CharField(choices=[('HRS', 'High Rack Storage'), ('PAL', 'Pallet')], default='HRS', help_text='Type of storage (e.g. High Rack Storage, Pallet)', max_length=3)),
                ('length', models.PositiveSmallIntegerField(help_text='Length of the place (in cm)')),
                ('width', models.PositiveSmallIntegerField(help_text='Width of the place (in cm)')),
                ('height', models.PositiveSmallIntegerField(help_text='Height of the place (in cm)')),
                ('max_weight', models.DecimalField(decimal_places=3, help_text='Maximum available weight on the place (in kg)', max_digits=8)),
                ('cell', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wms.cell')),
            ],
        ),
        migrations.CreateModel(
            name='GoodInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufactured', models.DateField(null=True)),
                ('best_before', models.DateField(blank=True, null=True, verbose_name='Best before')),
                ('bill', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wms.bill')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wms.good')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='wms.place')),
            ],
        ),
    ]
