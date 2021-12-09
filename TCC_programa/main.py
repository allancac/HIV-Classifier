from Search import Search
from Configurations import Configurations
from entrada import key_words_params


def main():
    for param in key_words_params:
        search_year = Configurations.load_database()["collection_name"]
        search = Search(search_year, param)
        search.make_search()


if __name__ == "__main__":
    main()
