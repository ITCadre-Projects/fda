import urllib.request
import urllib.error
from urllib.parse import urlparse
from .classes import DataPoint
import json


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
    my_data = []
    for product in my_products:
        print(product)
        search = 'patient.drug.medicinalproduct:{}+AND+receivedate:[{}+TO+{}]+AND+primarysourcecountry:ca'.format(
            product,
            start_date,
            end_date)
        count = "receivedate"
        url = "{}?search={}&count={}".format(base, search, count)
        # print(url)
        data = get_json(url)
        # print(data)
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
