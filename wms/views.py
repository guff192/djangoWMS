from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from django.views import generic
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms
from django.core.exceptions import ValidationError
import time

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
               'section_cells': section_cells, 'section_range': range(1, max_section + 1),}

    return render(request, 'map.html', context=context)


class CellDetailView(generic.DetailView):
    model = Cell


class PlaceDetailView(generic.DetailView):
    model = Place


class GoodDetailView(generic.DetailView):
    model = Good

    # def get_context_data(self, **kwargs):
    #     context = super(GoodDetailView, self).


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

        user_cart = self.request.session.get('cart_number', False)
        if not user_cart:
            number = int(''.join(str(time.time()).split('.')))
            bill = Bill(number=number, operation='ord')
            bill.save()
            user_cart = bill
            self.request.session['cart_number'] = user_cart.number
        else:
            bill = Bill.objects.get(number__exact=user_cart)

        context['bill'] = bill
        return context


class GoodInstanceDetailView(generic.DetailView):
    model = GoodInstance


class FavoriteGoodsByUserListView(LoginRequiredMixin, generic.ListView):
    model = Good
    template_name = 'wms/favorite_good_list_user.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FavoriteGoodsByUserListView, self).get_context_data()
        user_cart = self.request.session.get('cart_number', False)
        if not user_cart:
            number = int(''.join(str(time.time()).split('.')))
            bill = Bill(number=number, operation='ord')
            bill.save()
            user_cart = bill
            self.request.session['cart_number'] = user_cart.number
        else:
            bill = Bill.objects.get(number__exact=user_cart)
        context['bill'] = bill

        return context


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


class BillEditForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ('number', 'operation', 'date')

    number = forms.NumberInput()
    operation = forms.ChoiceField(choices=Bill.OPERATION_TYPES)
    date = forms.DateField(widget=forms.SelectDateWidget)


class BillEdit(PermissionRequiredMixin, UpdateView):
    model = Bill
    form_class = BillEditForm
    permission_required = 'wms.change_bill'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('index'))


def delete_good_from_bill(request, goodinstance_id, bill_id):
    good_instance = get_object_or_404(GoodInstance, goodinstance_id=goodinstance_id)
    bill = get_object_or_404(Bill, number=bill_id)

    if request.method == 'POST':
        set_to_del = bill.goodinstance_set.filter(goodinstance_id__exact=goodinstance_id)

        for entry in set_to_del:
            bill.goodinstance_set.remove(entry)

        if request.user.groups.filter(name__exact='Клиенты'):
            return HttpResponseRedirect(reverse('cart'))
        return HttpResponseRedirect(reverse('bill-detail', args=[str(bill_id)]))

    return render(request, "wms/goodinstance_confirm_delete.html")


class AddGoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ('good_id',)

    good_set = Good.objects.all()

    good = forms.ModelChoiceField(
        queryset=good_set,
        empty_label=None,
        to_field_name='good_id',
        label='Товар:',
    )

    def clean_good(self):
        data = self.cleaned_data['good']
        for goodinstance in data.goodinstance_set.all():
            print(f"{goodinstance}:")
            if goodinstance.bill.all().filter(operation__in=('dep', 'ord')):
                continue
            return data

        raise ValidationError('Этого товара нет в наличии')


@login_required()
def add_good_to_bill(request, bill_id):
    bill = get_object_or_404(Bill, number=bill_id)

    if request.method == 'POST':
        form = AddGoodForm(request.POST)
        if form.is_valid():
            good = form.cleaned_data['good']
            goodinstance_set = GoodInstance.objects \
                .filter(good__exact=good)
            for goodinstance in goodinstance_set:
                if not goodinstance.bill.filter(operation__in=('dep', 'ord')):
                    bill.goodinstance_set.add(goodinstance)
                    print(goodinstance)
                    break
            if request.user.groups.filter(name__exact='Клиенты'):
                return HttpResponseRedirect(reverse('cart'))
            return HttpResponseRedirect(reverse('bill-detail', args=[str(bill.number)]))

    form = AddGoodForm(request.POST)
    context = {
        'bill_id': bill_id,
        'form': form,
        'bill': bill,
    }

    return render(request, 'wms/goodinstance_add_form.html', context)


@login_required()
def add_to_cart(request, bill_id, good_id):
    bill = get_object_or_404(Bill, number=bill_id)
    good = get_object_or_404(Good, good_id=good_id)

    goodinstance_set = GoodInstance.objects \
        .filter(good__exact=good)
    for goodinstance in goodinstance_set:
        if not goodinstance.bill.filter(operation__in=('dep', 'ord')):
            bill.goodinstance_set.add(goodinstance)
            if request.user.groups.filter(name__exact='Клиенты'):
                return HttpResponseRedirect(reverse('cart'))
            return HttpResponseRedirect(reverse('bill-detail', args=[str(bill.number)]))

    return HttpResponseRedirect(reverse('goods'))




@login_required()
def cart(request):
    if request.user.groups.filter(name__exact='Клиенты'):
        user_cart = request.session.get('cart_number', False)
        if not user_cart:
            number = int(''.join(str(time.time()).split('.')))
            bill = Bill(number=number, operation='ord')
            bill.save()
            user_cart = bill
            request.session['cart_number'] = user_cart.number
        else:
            bill = Bill.objects.get(number__exact=user_cart)

        context = {'bill': bill}
        return render(request, 'wms/bill_detail.html', context)

    return HttpResponseRedirect(reverse('bills'))


class GoodInstanceCreate(PermissionRequiredMixin, CreateView):
    model = GoodInstance
    template_name = 'wms/goodinstance_create_form.html'
    fields = '__all__'
    permission_required = 'wms.change_good_instance'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('index'))


class GoodInstanceUpdate(PermissionRequiredMixin, UpdateView):
    model = GoodInstance
    template_name = 'wms/goodinstance_create_form.html'
    fields = ['good', 'manufactured', 'best_before', 'bill', 'place']
    permission_required = 'wms.change_good_instance'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('index'))
