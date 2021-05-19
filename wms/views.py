from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from django.views import generic
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Row, Cell, Place, Good, GoodInstance, Bill

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

    context = {'rows': rows, 'rows_count': rows_count,
               'section_cells': section_cells, 'section_range': range(1, max_section + 1), }

    return render(request, 'map.html', context=context)


class CellDetailView(generic.DetailView):
    model = Cell


class PlaceDetailView(generic.DetailView):
    model = Place


class GoodDetailView(generic.DetailView):
    model = Good


class GoodListView(generic.ListView):
    model = Good
    paginate_by = 10

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', 'price')
        new_context = Good.objects.filter(
            manufacturer__icontains=filter_val,
        ).order_by(order)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', )
        context['orderby'] = self.request.GET.get('orderby', 'price')
        return context


class GoodInstanceDetailView(generic.DetailView):
    model = GoodInstance


class FavoriteGoodsByUserListView(LoginRequiredMixin, generic.ListView):
    model = Good
    template_name = 'wms/favorite_good_list_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Good.objects.filter(favorites=self.request.user).order_by('article')


@login_required()
def add_to_favorites(request, pk):
    good = get_object_or_404(Good, good_id=pk)
    user = request.user

    if good and user:
        good.favorites.add(user.pk)
        return HttpResponseRedirect(reverse('good-detail', args=[str(pk)]))
    else:
        HttpResponseBadRequest(f'Wrong credentials!')


@login_required()
def remove_from_favorites(request, pk):
    good = get_object_or_404(Good, good_id=pk)
    user = request.user

    if good and user and good in user.good_set.filter(good_id__exact=pk):
        for good in user.good_set.filter(good_id__exact=pk):
            good.favorites.remove(user.pk)
        return HttpResponseRedirect(reverse('good-detail', args=[str(pk)]))

    return HttpResponseBadRequest(f'Wrong credentials!<a href="/">Return to main page</a>')


class BillListView(PermissionRequiredMixin, generic.ListView):
    model = Bill
    paginate_by = 10
    permission_required = 'wms.view_bill'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('index'))


class BillDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Bill
    permission_required = 'wms.view_bill'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('index'))


class BillCreate(PermissionRequiredMixin, CreateView):
    model = Bill
    fields = '__all__'
    permission_required = 'wms.can_view_bill'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('index'))


class BillEdit(PermissionRequiredMixin, UpdateView):
    model = Bill
    fields = '__all__'
    permission_required = 'wms.change_bill'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('index'))


def delete_good_from_bill(request, goodinstance_id, bill_id):
    context = {}

    good_instance = get_object_or_404(GoodInstance, goodinstance_id=goodinstance_id)
    bill = get_object_or_404(Bill, number=bill_id)

    if request.method == 'POST':
        set_to_del = bill.goodinstance_set.filter(goodinstance_id__exact=goodinstance_id)

        for entry in set_to_del:
            bill.goodinstance_set.remove(entry)

        return HttpResponseRedirect(reverse('bill-detail', args=[str(bill_id)]))

    return render(request, "wms/goodinstance_confirm_delete.html", context)


class GoodInstanceCreate(PermissionRequiredMixin, CreateView):
    model = GoodInstance
    fields = '__all__'
    permission_required = 'wms.change_good_instance'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('index'))


class GoodInstanceUpdate(PermissionRequiredMixin, UpdateView):
    model = GoodInstance
    fields = ['good', 'manufactured', 'best_before', 'bill', 'place']
    permission_required = 'wms.change_good_instance'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('index'))
