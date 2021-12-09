import json


class Configurations:
    @staticmethod
    def load_queries():
        with open("conf.json", "r") as conf:
            queries_dict = json.load(conf)["queries"]
        return queries_dict

    @staticmethod
    def load_fields():
        with open("conf.json", "r") as conf:
            expansions_dict = json.load(conf)["fields"]
        return expansions_dict

    @staticmethod
    def load_database():
        with open("conf.json", "r") as conf:
            expansions_dict = json.load(conf)["database"]
        return expansions_dict
