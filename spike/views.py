from django.shortcuts import render
from .models import DataPoint
from .services import baseline_10_years
from .services import search_by_product
from .services import retreive_drug_names
from django.http import *
from .forms import PostForm
from rest_framework.decorators import api_view


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


@api_view(['GET', 'POST'])
def search(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            drug_name = request.POST.get('drug_name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
    else:
        drug_name = request.query_params.get('drug_name')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

    data_points = search_by_product(drug_name, start_date, end_date)

    if data_points:
        return JsonResponse(data_points)
        # return HttpResponse(data_points, content_type="application/json")
    else:
        return render(request, 'spike/search.html', {'error': True})


@api_view(['GET', 'POST'])
def get_drug_names(request):
    return JsonResponse(retreive_drug_names(request.query_params.get('count')))
