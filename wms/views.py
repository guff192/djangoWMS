from django.shortcuts import render
from django.db.models import Max
from django.views import generic
from wms.models import Row, Cell, Place, Good

# Create your views here.


def index(request):
    rows = Row.objects.all()
    rows_count = rows.count()

    cells = Cell.objects.all()

    max_section = Cell.objects.all().aggregate(Max('section'))['section__max']
    section_cells = {}
    for section in range(1, max_section+1):
        cells_list = []
        row = 1
        for cell in cells.filter(section__exact=section):
            if cell.row.number != row:
                for i in range(cell.row.number - row):
                    cells_list.append('')
                    row += 1

            cells_list.append(cell)
            row += 1

        section_cells[section] = cells_list

    # TODO: Generate table

    context = {'rows': rows, 'rows_count': rows_count,
               'section_cells': section_cells, 'section_range': range(1, max_section + 1), }

    return render(request, 'index.html', context=context)


class CellDetailView(generic.DetailView):
    model = Cell


class PlaceDetailView(generic.DetailView):
    model = Place


class GoodDetailView(generic.DetailView):
    model = Good
