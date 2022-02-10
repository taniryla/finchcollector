from django.shortcuts import render
from .models import Finch, House
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import WatchingForm
from django.shortcuts import render, redirect


# Create your views here.


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {'finches': finches})


def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    # get the houses that the finch doesn't have
    houses_finch_doesnt_have = House.objects.exclude(
        id__in=finch.houses.all().values_list('id'))
    watching_form = WatchingForm()
    return render(request, 'finches/detail.html', {
        'finch': finch,
        'watching_form': watching_form,
        'houses': houses_finch_doesnt_have
    })


class FinchCreate(CreateView):
    model = Finch
    fields = ['name', 'type', 'description', 'age']


class FinchUpdate(UpdateView):
    model = Finch
    fields = ['breed', 'description', 'age']


class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches/'


def add_watching(request, finch_id):

    # create a ModelForm instance using the data in request.POST
    form = WatchingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_watching = form.save(commit=False)
        new_watching.cat_id = finch_id
        new_watching.save()
    return redirect('detail', finch_id=finch_id)


def houses_index(request):
    houses = House.objects.all()
    return render(request, 'houses/index.html', {'houses': houses})


class HouseCreate(CreateView):
    model = House
    fields = "__all__"


def houses_detail(request, house_id):
    house = House.objects.get(id=house_id)
    return render(request, 'houses/detail.html', {
        'house': house
    })


class HouseUpdate(UpdateView):
    model = House
    fields = ['name', 'color']


class HouseDelete(DeleteView):
    model = House
    success_url = '/houses/'


def assoc_house(request, finch_id, house_id):
    # Note that you can pass a house's id instead of the whole house object
    Finch.objects.get(id=finch_id).houses.add(house_id)
    return redirect('detail', finch_id=finch_id)


def un_assoc_house(request, finch_id, house_id):
    # Note that you can pass a house's id instead of the whole house object
    Finch.objects.get(id=finch_id).houses.add(house_id)
    return redirect('detail', finch_id=finch_id)
