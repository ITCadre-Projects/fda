from django.shortcuts import render
from .models import DataPoint
from .services import baseline_10_years

def index(request):
	data_points = DataPoint.objects.order_by('filed_date')
	context = {'data_points': data_points}
	return render(request, 'spike/index.html', context)
	
def fda(request):
	data_points = baseline_10_years()
	context = {'data_points': data_points}
	return render(request, 'spike/index.html', context)
