from django.db import models
from django.urls import reverse

# Create your models here.


class Cell(models.Model):
    row = models.PositiveSmallIntegerField(help_text="Number of cell's row on a warehouse scheme")
    column = models.PositiveSmallIntegerField(help_text="Number of cell's column on a warehouse scheme")

    def __str__(self):
        return f'Row {self.row}, Place {self.column}'

    def get_absolute_url(self):
        pass
        # TODO: Define method for representing list of cell's places

    class Meta:
        ordering = ['row', 'column']  # TODO: Choose ordering for table view


class Place(models.Model):
    cell = models.ForeignKey(Cell, on_delete=models.RESTRICT)

    STORAGE_TYPES = [
        ('HRS', 'High Rack Storage'),
        ('PAL', 'Pallet'),
    ]
    storage = models.CharField(
        max_length=3,
        choices=STORAGE_TYPES,
        default='HRS',
        help_text='Type of storage (e.g. High Rack Storage, Pallet)'
    )

    length = models.PositiveSmallIntegerField(help_text="Length of the place (in cm)")
    width = models.PositiveSmallIntegerField(help_text="Width of the place (in cm)")
    height = models.PositiveSmallIntegerField(help_text="Height of the place (in cm)")

    max_weight = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        help_text="Maximum available weight on the place (in kg)"
    )

    def __str__(self):
        return f"{dict(self.STORAGE_TYPES)[self.storage]}\nLength: {self.length / 100}m, \
                Width: {self.width / 100}m, Height: {self.height / 100}m\nCapacity: {self.max_weight}kg"

    def get_absolute_url(self):
        return reverse('place-details', args=[str(self.id)])


class Good(models.Model):
    barcode = models.CharField(max_length=128, null=True, help_text="Product barcode")
    article = models.CharField(max_length=128, blank=True, help_text="Name of goods")
    manufacturer = models.CharField(max_length=128, blank=True, help_text="Manufacturer name (e.g. BOSCH, Samsung")
    model = models.CharField('Model', max_length=128, blank=True, help_text="Model of the product")

    weight = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        help_text="Weight of a good (in kg)"
    )
    price = models.PositiveIntegerField(help_text="Price of a good (in cents)")
    fragile = models.BooleanField(default=False)

    def __str__(self):
        return self.article

    def get_absolute_url(self):
        return reverse('good-detail', args=[str(self.id)])


class GoodInstance(models.Model):
    good = models.ForeignKey(Good, on_delete=models.PROTECT)
    manufactured = models.DateField(null=True)
    best_before = models.DateField('Best before', null=True, blank=True)
    bill = models.ForeignKey('Bill', on_delete=models.SET_NULL, null=True)
    place = models.ForeignKey(Place, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.id} ({self.good.article})"


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
