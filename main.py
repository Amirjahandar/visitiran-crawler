from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import requests
import time
import json
import logging


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def save_data(data, filename="data.json"):
    with open(f"{filename}", "w") as myfile:
        json.dump(data, myfile, indent=4)

def elastic_load(data_file):
    es = Elasticsearch(['https://elastic:amir1374@localhost:9200'], verify_certs=False)
    with open(data_file) as file:
        for idx, value in enumerate(file):
            result = es.index(index="visitiranindex", id=idx, document=value)
        print(result)





def fetch(url, method='GET', headers={"User-Agent":"Safari/iphone13"}):
    response = requests.get(url ,headers=headers ,verify=False)
    logging.info(f"I fetch url:{url} response_code: {response.status_code} response_time: {response.elapsed}")
    
    return response




def extract_categories(url):
    '''
    this function extract data_id of lables in visit iran.ir
    '''
    response = fetch(url)
    page = BeautifulSoup(response.text, 'html.parser')
    filters = page.find_all('input', class_ = 'uk-checkbox mapFilters')
    categories = []
    keys  = ["data-code", "data-name", "data-randomcode" ]

    for filter in filters:
        category = {k: filter[k] for k in keys if filter.get(k)}
        categories.append(category)

    save_data(categories)

    logging.debug(f"Response: {categories}")
    logging.info(f"fetched {len(categories)} categories, url:{url}")

    return categories



def main():
    categories = extract_categories("https://www.visitiran.ir/en/TourismMap")
    url = "https://www.visitiran.ir/api/map/search/withFilter?language=en&filter=1181"

    # for category in categories:
    #     data_url = url + category["data-code"] + ','
    #     url = data_url
    
    print(url)
    response = fetch(url)
    obj = json.loads(response.text)
    results = obj.get("result")
    print(results)
    save_data(results, filename="crawl_results.json")

    # elastic_load("crawl_results.json")

    return response.status_code




if __name__ == "__main__":
    while True:
        main()
        print("Wait For Reloading.....")
        SLEEP_REQUEST = 60
        time.sleep(SLEEP_REQUEST)
        print("New Request....")
        
    




















