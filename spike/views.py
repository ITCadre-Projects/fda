from django.shortcuts import render
from .models import DataPoint
from .services import baseline_10_years
from .services import search_by_product
from django.http import *
from .forms import PostForm


def index(request):
    data_points = DataPoint.objects.order_by('filed_date')
    context = {'data_points': data_points}
    return render(request, 'spike/index.html', context)


def fda(request):
    data_points = baseline_10_years()
    context = {'data_points': data_points}
    return render(request, 'spike/index.html', context)


def search_form(request):
    return render(request, 'spike/search.html')


def search(request):
    print('hey man')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            drug_name = request.POST.get('drug_name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
        else:
            print('form is bad')

        # print(drug_name)
        data_points = search_by_product(drug_name, start_date, end_date)
        print("--------------")
        print(data_points)
        if data_points:
            return JsonResponse(data_points)
            # return HttpResponse(data_points, content_type="application/json")
        else:
            return render(request, 'spike/search.html', {'error': True})
    else:
        return render(request, 'spike/search.html', {'error': True})
