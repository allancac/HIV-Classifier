import os
import requests
import time
from Logs import WriteLog
from Configurations import Configurations
import json


class RequestFullArchive(object):

    def __init__(self, query, fields):
        self.bearer_token = os.environ.get("BEARER_TOKEN")
        self.url = "https://api.twitter.com/2/tweets/search/all?query={}&{}".format(query, fields)
        self.headers = {"Authorization": "Bearer {}".format(self.bearer_token)}
        self.response = None

    def change_keys(self):
        if self.response["data"]:
            for tweet in self.response["data"]:
                tweet["_id"] = tweet["id"]
                del tweet["id"]
                tweet["target"] = ""
                tweet["sentiment"] = ""
                tweet["request_id"] = []

    def make_request(self):
        self.response = requests.request("GET", self.url, headers=self.headers)

        if self.response.status_code == 503:
            ano_pesquisa = Configurations.load_database()["collection_name"]
            log = WriteLog(ano_pesquisa)
            log.write(f'Erro {self.response.status_code}. Detalhes: {self.response.text}')
            is_unavailable = True
            while is_unavailable:
                time.sleep(60)
                self.response = requests.request("GET", self.url, headers=self.headers)
                if self.response.status_code == 200:
                    is_unavailable = False

        if self.response.status_code == 200:
            self.response = self.response.json()
            time.sleep(1)  # Garante a taxa de requisições da API do Twitter > 1 requisição/segundo.
        else:
            raise Exception(self.response.status_code, self.response.text)
        if self.response["meta"]["result_count"] > 0:
            self.change_keys()

    def make_next_request(self, next_token):
        self.response = requests.request("GET", "{}&next_token={}".format(self.url, next_token),
                                         headers=self.headers)

        if self.response.status_code == 503:
            ano_pesquisa = Configurations.load_database()["collection_name"]
            log = WriteLog(ano_pesquisa)
            is_unavailable = True
            while is_unavailable:
                log.write(f'Erro {self.response.status_code}. Detalhes: {self.response.text}')
                time.sleep(60)
                self.response = requests.request("GET", "{}&next_token={}".format(self.url, next_token),
                                                 headers=self.headers)
                if self.response.status_code == 200:
                    is_unavailable = False

        if self.response.status_code == 200:
            self.response = self.response.json()
            time.sleep(15)  # Garante a taxa de requisições da API do Twitter 300 requisições/15 min.

        else:
            raise Exception(self.response.status_code, self.response.text)
        self.change_keys()

    def get_data(self):
        if self.response["meta"]["result_count"] > 0:
            return self.response["data"]
        else:
            return None

    def print_data(self):
        for documento in self.response["data"]:
            print(json.dumps(documento, indent=4, sort_keys=True))

    def get_meta_data(self):
        return self.response["meta"]

    def is_next_page_present(self):
        if "next_token" in self.response["meta"]:
            return True
        else:
            return False

    def get_next_token(self):
        if self.is_next_page_present():
            return self.response["meta"]["next_token"]

    def get_tweets_count(self):
        return self.response["meta"]["result_count"]

    def get_url(self):
        return self.url
