from Configurations import Configurations
from pymongo import MongoClient
import matplotlib.pyplot as plt


def conectar(ano):
    database_conf = Configurations.load_database()
    client = MongoClient(database_conf["host"], database_conf["port"])
    database_name = database_conf["database_name"]
    collection_name = database_conf["collection_name"]
    db = client[database_name]
    colecao = db[ano]
    return colecao


def gerar_total_ano(total_anos, lista):
    for ind in lista:
        collection = conectar(str(ind))
        filtro = {}
        total_anos.append(collection.count_documents(filtro))



total = []
lista_anos = [2015, 2016, 2017, 2018, 2019, 2020]
lables_eixo_x = ["2015", "2016", "2017", "2018", "2019", "2020"]
lables_eixo_y = []



gerar_total_ano(total, lista_anos)

plt.rcParams['figure.figsize'] = [15, 10]
font = {'family': 'Arial',
        'weight': 'bold',
        'size': 22}

plt.rc('font', **font)


plt.bar(lables_eixo_x, total, linewidth=10)
plt.title('GRÁFICO DE TOTAL BUSCAS POR ANO')
plt.xlabel("ANOS")
plt.ylabel("QUANTIDADE DE TWEETS")
plt.legend(bbox_to_anchor=(.75, 1), loc='upper left', borderaxespad=0.)
plt.grid(True)
plt.show()
