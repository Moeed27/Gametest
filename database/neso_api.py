import requests
from datetime import datetime
from config import logger


def request_carbon_intensity(start_datetime:datetime, end_datetime:datetime=None):
    table = "f93d1835-75bc-43e5-84ad-12472b180a98"
    if end_datetime:
        datetime_query = f'"DATETIME">=\'{str(start_datetime)}\' AND "DATETIME"<=\'{str(end_datetime)}\''
    else:
        datetime_query = f'"DATETIME"=\'{str(start_datetime)}\''
    query = f'SELECT "DATETIME","CARBON_INTENSITY" from "{table}" WHERE {datetime_query} ORDER BY "DATETIME" ASC'
    url = f'https://api.neso.energy/api/3/action/datastore_search_sql?sql={query}'
    logger.info(f"Sending query to NESO API at [{url.rsplit('=')[0]}]... \n>\tQUERY: {query}")
    file = requests.get(url).json()
    output_dict = {}
    for r in file['result']['records']:
        output_dict.update({datetime.strptime(r['DATETIME'], "%Y-%m-%dT%H:%M:%S"):float(r['CARBON_INTENSITY'])})
    return output_dict

#request_carbon_intensity(datetime(2020, 1, 1), datetime(2020, 1, 2))