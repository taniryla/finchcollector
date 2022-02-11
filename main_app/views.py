from .forms import WatchingForm
from .models import Finch, House
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render

# Create your views here.


# Define the home view
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {'finches': finches})


def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    # instantiate FeedingForm to be rendered in the template
    id_list = finch.houses.all().values_list('id')
    houses_finch_doesnt_have = House.objects.exclude(id__in=id_list)
    watching_form = WatchingForm()
    return render(request, 'finches/detail.html', {
        'finch': finch,
        'watching_form': watching_form,
        'houses': houses_finch_doesnt_have,
    })


def add_viewing(request, finch_id):
    form = WatchingForm(request.POST)
    # validate the form
    if form.is_valid():
        # dont save the form to the db until it
        # has the finch_id assigned
        new_viewing = form.save(commit=False)
        new_viewing.finch_id = finch_id
        new_viewing.save()
    return redirect('detail', finch_id=finch_id)


def houses_index(request):
    houses = House.objects.all()
    return render(request, 'houses/index.html', {'houses': houses})


def houses_detail(request, house_id):
    house = House.objects.get(id=house_id)
    return render(request, 'houses/detail.html', {
        'house': house,
    })


def assoc_house(request, finch_id, house_id):
    # Note that you can pass a toy's id instead of the whole toy object
    Finch.objects.get(id=finch_id).houses.add(house_id)
    return redirect('detail', finch_id=finch_id)


def unassoc_house(request, finch_id, house_id):
    finch = Finch.objects.get(id=finch_id)
    finch.houses.remove(house_id)
    return redirect('detail', finch_id=finch_id)


# class based view
class FinchCreate(CreateView):
    model = Finch
    fields = ['name', 'type', 'description', 'age']


class FinchUpdate(UpdateView):
    model = Finch
    fields = ['type', 'description', 'age']


class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches/'


class HouseCreate(CreateView):
    model = House
    fields = '__all__'


class HouseUpdate(UpdateView):
    model = House
    fields = ['Name', 'Color']


class HouseDelete(DeleteView):
    model = House
    success_url = '/houses/'
