from django.db import models
from django.urls import reverse

# Create your models here.


class Row(models.Model):
    number = models.PositiveSmallIntegerField(help_text="Number of cell's row on a warehouse scheme", primary_key=True)
    STORAGE_TYPES = [
        ('HRS', 'Стеллаж'),
        ('PAL', 'Палета'),
    ]
    storage = models.CharField(
        max_length=3,
        choices=STORAGE_TYPES,
        default='HRS',
        help_text='Type of storage (e.g. High Rack Storage, Pallet)'
    )

    def __str__(self):
        return f"{dict(self.STORAGE_TYPES)[self.storage]} Ряд {self.number}"



    class Meta:
        ordering = ['number']


class Cell(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE)
    section = models.PositiveSmallIntegerField('Section', help_text="Vertical section number on a warehouse scheme")

    def __str__(self):
        return f'{self.row}, Секция {self.section}'

    def get_absolute_url(self):
        return reverse('cell-detail', args=[str(self.id)])

    class Meta:
        ordering = ['row', 'section']  # TODO: Choose ordering for table view


class Place(models.Model):
    cell = models.ForeignKey(Cell, on_delete=models.RESTRICT)
    level = models.PositiveSmallIntegerField(help_text="Level of the place", default=0)

    length = models.PositiveSmallIntegerField(help_text="Length of the place (in cm)")
    width = models.PositiveSmallIntegerField(help_text="Width of the place (in cm)")
    height = models.PositiveSmallIntegerField(help_text="Height of the place (in cm)", blank=True, default=0)

    max_weight = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        help_text="Maximum available weight on the place (in kg)"
    )

    def __str__(self):
        if self.cell.row.storage == 'HRS':
            return f"{self.cell}, Уровень {self.level}"
        else:
            return f"{self.cell}"

    def get_absolute_url(self):
        return reverse('place-detail', args=[str(self.id)])

    class Meta:
        ordering = ['level']


class Good(models.Model):
    barcode = models.CharField(max_length=128, null=True, help_text="Product barcode")
    article = models.CharField(max_length=128, blank=True, help_text="Name of product")
    description = models.TextField(max_length=1000, help_text="Description of product")
    manufacturer = models.CharField(max_length=128, blank=True, help_text="Manufacturer name (e.g. BOSCH, Samsung)")
    model = models.CharField('Model', max_length=128, blank=True, help_text="Model of the product")

    length = models.PositiveSmallIntegerField(help_text="Length of the product (in cm)", default=0)
    width = models.PositiveSmallIntegerField(help_text="Width of the product (in cm)", default=0)
    height = models.PositiveSmallIntegerField(help_text="Height of the product (in cm)", default=0, blank=True)

    weight = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        help_text="Weight of a good (in kg)"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of a good (in rubles)")
    fragile = models.BooleanField(default=False)

    def __str__(self):
        return self.article

    def get_absolute_url(self):
        return reverse('good-detail', args=[str(self.id)])


class GoodInstance(models.Model):
    good = models.ForeignKey(Good, on_delete=models.PROTECT)
    manufactured = models.DateField(null=True)
    best_before = models.DateField('Best before', null=True, blank=True)
    bill = models.ForeignKey('Bill', on_delete=models.SET_NULL, null=True, blank=True)
    place = models.ForeignKey('Place', on_delete=models.RESTRICT, blank=True)

    def __str__(self):
        return f"{self.id}: {self.good.article} ({self.place})"


class Bill(models.Model):
    number = models.PositiveSmallIntegerField(help_text='Number of the bill', primary_key=True)

    OPERATION_TYPES = [
        ('arr', 'Arrival'),
        ('dep', 'Departure'),
    ]
    operation = models.CharField(
        max_length=3,
        choices=OPERATION_TYPES,
        default='dep',
        help_text='Type of operation'
    )

    date = models.DateField()

    def __str__(self):
        return f"{self.number} ({self.date})"

    def get_absolute_url(self):
        return reverse('bill-detail', args=[str(self.number)])
