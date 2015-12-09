import urllib.request
import urllib.error
from urllib.parse import urlparse
from .classes import DataPoint
from .models import DataRecord
import json
import datetime

def get_json(url, username=None, password=None):
    try:
        if username and password:
            url_parts = urlparse(url)
            url_base = "{}://{}/".format(url_parts.scheme, url_parts.netloc)
            password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            password_manager.add_password(None, url_base, username, password)
            auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
            opener = urllib.request.build_opener(auth_handler)
            urllib.request.install_opener(opener)
        with urllib.request.urlopen(url) as response:
            raw = response.read().decode('utf-8')
            data = json.loads(raw)
        return data
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.msg)


def baseline_10_years(search_type=None):
    print(search_type)
    base = "https://api.fda.gov/drug/event.json"

    if not search_type or search_type == 'All':
        search = "receivedate:[20050101+TO+20150101]"
    else:
        search = 'patient.drug.openfda.pharm_class_epc:"' + search_type + '"'

    print(search)
    count = "receivedate"
    url = "{}?search={}&count={}".format(base, search, count)
    data = get_json(url)
    points = []
    for result in data["results"]:
        # print(result)
        point = DataPoint(filed_date=result["time"], drug_name="All", count=result["count"])
        points.append(point)
    return points


def search_by_product(products, start_date, end_date):
    my_products = products.split(',')

    base = "https://api.fda.gov/drug/event.json"

    my_data_dict = {'final': []}
    for product in my_products:
        search = 'patient.drug.medicinalproduct:{}+AND+receivedate:[{}+TO+{}]+AND+primarysourcecountry:ca'.format(
            product,
            start_date,
            end_date)
        count = "receivedate"
        url = "{}?search={}&count={}".format(base, search, count)
        data = get_json(url)
        my_data_dict['final'].append(data)

    return my_data_dict


def retreive_drug_names(count=None):
    if count:
        my_count = count
    else:
        my_count = 20

    base = "https://api.fda.gov/drug/event.json"
    search = ""
    pcount = "medicinalproduct"

    url = "{}?search={}&count={}&limit={}".format(base, search, pcount, my_count)

    print(url)
    data = get_json(url)
    return data

def retrieve_mentioned_event_twitter(drug_name, start_date = None, end_date = None, count = None):

    events = DataRecord.objects.filter(data_src__iexact="twitter")
    if drug_name:
        events = events.filter(raw_data__icontains=drug_name)
    if start_date:
        sdate = datetime.datetime.strptime(start_date,'%Y%m%d')
        events = events.filter(captured_date__gte=sdate)
    if end_date:
        edate = datetime.datetime.strptime(end_date,'%Y%m%d')
        events = events.filter(captured_date__lte=edate)
    if count:
        mycount = int(count)
    else:
        mycount = 10

    if len(events) > mycount:
        events = events[:mycount]
    return events