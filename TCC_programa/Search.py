import time
import urllib.parse

from Configurations import Configurations
from Logs import WriteLog
from DbConnection import SearchDatabase, TweetsDatabse
from RequestTwitter import RequestFullArchive


class Search(object):

    def __init__(self, search_year, search_params):

        """Realiza as requisições dos tweets.

        Recebe como parâmetros tuplas, estruturadas em um array, no arquivo entrada.py
        Cada tupla contém informações do domínio, subdomínio e palavras-chave para cada busca.
        O método make_search é o bloco de código responsável por realizar as requisições.

        :param search_params: tuple
        :param log: object
        :return: None
        """
        self.log = WriteLog(search_year)  # Instancia do LOG
        self.key_word = search_params[2]
        self.query = Query(urllib.parse.quote(self.key_word))  # Expressão da query de requisição
        self.fields = Fields()  # Parâmetros para construir as fields
        self.search_database = SearchDatabase()  # Instância da Database das Requisições
        self.domain = search_params[0]
        self.subdomain = search_params[1]
        self.requested_data = RequestFullArchive(self.query, self.fields)  # Instância da requisição HTTP GET

    def make_search(self):
        count_documents = self.search_database.colecao.count_documents({})
        self.requested_data.make_request()  # Executa o método responsável por realizar a requisição HTTP GET
        # Dicionário com informações sobre a busca atual
        search_data = {
            "_id": count_documents + 1,
            "domain": self.domain,
            "sub_domain": self.subdomain,
            "start_search": time.time(),
            "end_search": 0,
            "total_requests": 0,
            "next_token": [],
            "total_tweets": self.requested_data.get_tweets_count(),
            "url": self.requested_data.get_url()
        }

        self.log.write(self.requested_data.get_url())
        self.log.write("Total de Tweets na requisicao: {}".format(self.requested_data.get_meta_data()["result_count"]))

        self.search_database.insert_search(search_data)  # Insere dados na Database das Requisições.
        self.log.write("# Buscando Tweets com '{}'".format(self.key_word))  # LOG
        self.log.write_request_date_time("# Início")  # LOG

        # Verifica se a primeira requisição não obteve tweets
        if self.requested_data.get_tweets_count() > 0:

            connection = TweetsDatabse()  # Instância da database principal, dos tweets.
            # Executa o método da instância, da classe TweetsDatabse, que insere dados na Database dos tweets.
            # Passa como parâmetro o dicionário "data", na instância da requisição atual e o iD da busca Atual.
            connection.insert_tweets(self.requested_data.get_data(), search_data["_id"])
            is_next_page = self.requested_data.is_next_page_present()  # Verificação se há uma próxima paginação na requisição.

            # 4 - Bloco de código em loop, que realizará as próximas requisições da busca atual, caso haja paginação.
            while is_next_page:
                next_page = self.requested_data.get_next_token()  # Next Token para a próxima paginação na requisição.
                self.requested_data.make_next_request(next_page)  # Método  que executa a próxima requisição HTTP GET
                # Passa como parâmetro o dicionário "data", na instância da requisição atual e o iD da busca Atual.
                connection.insert_tweets(self.requested_data.get_data(), search_data["_id"])
                # Bloco de códico para atualização da Database das Requisições
                search_data["next_token"].append(next_page)
                search_data["total_requests"] += 1
                search_data["total_tweets"] += self.requested_data.get_tweets_count()
                self.search_database.update_search(search_data, ["next_token", "total_requests", "total_tweets"])

                is_next_page = self.requested_data.is_next_page_present()  # Verifica se há uma próxima requisição

                self.log.write("next_token: {}".format(self.requested_data.get_next_token()))  # LOG
                self.log.write(
                    "Total de Tweets na requisicao: {}".format(
                        self.requested_data.get_meta_data()["result_count"]))  # LOG

            search_data["end_search"] = time.time()
            self.search_database.update_search(search_data, ["end_search"])

            self.log.write_request_date_time("# Fim")  # LOG
            self.log.write("*" * 150)  # LOG

        else:
            self.log.write("Busca por '{}' nao encontrou resultados".format(self.key_word))  # LOG
            self.log.write_request_date_time("# Busca sem resultados ")  # LOG
            self.log.write("*" * 150)  # LOG

        del self.requested_data


class Query(object):
    def __init__(self, hashtag):
        self.queries_conf = Configurations.load_queries()
        self.query = f'{hashtag}'

        for item in self.queries_conf:
            if item == "lang" or item == "is_retweet":
                self.query += urllib.parse.quote(" " + self.queries_conf[item])
            else:
                self.query += "&" + self.queries_conf[item]

    def __repr__(self):
        return self.query


class Fields(object):
    def __init__(self):
        self.fields_conf = Configurations.load_fields()
        self.fields_str = ""
        if self.fields_conf["tweet_fields"]:
            self.fields_str += "&tweet.fields="
            self.fields_str += self.fields_conf["tweet_fields_list"]

        if self.fields_conf["user_fields"]:
            self.fields_str += "&user.fields="
            self.fields_str += self.fields_conf["user_fields_list"]

    def __repr__(self):
        return self.fields_str
