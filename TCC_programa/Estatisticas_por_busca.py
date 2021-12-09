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


def montar_filtro(id):
    filtro = {
        'request_id': id
    }
    return filtro


def gerar_estatisticas(anos, id_searchs):
    estatistica_ano = []
    for index, id_search in enumerate(id_searchs):
        colecao_ano = conectar(str(anos[index]))

        filtro = montar_filtro(id_search)

        estatistica_ano.append(colecao_ano.count_documents(filtro))

    return estatistica_ano


anos = [2015, 2016, 2017, 2018, 2019, 2020]
labels_busca = [
    "#prep",
    "#truvada",
    "#aTripla",
    "#HIVinfection",
    "#epzicom",
    "#complera",
    "#ftc hiv",
    "#hiv drug",
    "#hiv treatment",
    "#3tc hiv",
    "#triple therapy hiv",
    "#anti hiv",
    "#isentress",
    "#reyataz",
    "#complera",
    "#norvir",
    "#livingwithaids",
    "#peptreatment",
    "#NormalizingHIVChallenge",
    "sustiva",
    "stocrin",
    "viread",
    "#pepforhiv",
    "#pepforearlyhiv",
    "#pepindelhi",
    "#peptreatment",
    "#peptreatmentinmalviyanagar",
    "#pepcenterforhiv",
    "#pephivcenter",
    "#pepforealryexposer"
]
busca_total = []

for i in range(0, 30):  # alterar até 30 !
    id_searchs = [151 + i, 121 + i, 91 + i, 61 + i, 31 + i, 1 + i]  # Número do ID Inicial
    lista_estatisticas = gerar_estatisticas(anos, id_searchs)
    busca_total.append(lista_estatisticas)

plt.rcParams['figure.figsize'] = [26, 12]
font = {'family': 'Arial',
        'weight': 'bold',
        'size': 22}
plt.rc('font', **font)

for index, lista_estatisticas in enumerate(busca_total[0:10]):
    plt.plot(["2015", "2016", "2017", "2018", "2019", "2020"], lista_estatisticas, label=labels_busca[0 + index],
             linewidth=10)

plt.title('GRÁFICO DE BUSCAS')
plt.xlabel("ANOS")
plt.yscale("log")
plt.ylabel("QUANTIDADE DE TWEETS")
plt.legend(bbox_to_anchor=(.96, 1), loc='upper left', borderaxespad=0.)
plt.grid(True)
# plt.savefig('grafico1.png', dpi=900)
plt.show()

for index, lista_estatisticas in enumerate(busca_total[10:20]):
    plt.plot(["2015", "2016", "2017", "2018", "2019", "2020"], lista_estatisticas, label=labels_busca[10 + index],
             linewidth=10)

plt.title(f'GRÁFICO DE BUSCAS')
plt.xlabel("ANOS")
plt.yscale("log")
plt.ylabel("QUANTIDADE DE TWEETS")
plt.legend(bbox_to_anchor=(.96, 1), loc='upper left', borderaxespad=0.)
plt.grid(True)
# plt.savefig('grafico2.png', dpi=900)
plt.show()

for index, lista_estatisticas in enumerate(busca_total[20:30]):
    plt.plot(["2015", "2016", "2017", "2018", "2019", "2020"], lista_estatisticas, label=labels_busca[20 + index],
             linewidth=10)

plt.title(f'GRÁFICO DE BUSCAS')
plt.xlabel("ANOS")
plt.yscale("log")
plt.ylabel("QUANTIDADE DE TWEETS")
plt.legend(bbox_to_anchor=(.96, 1), loc='upper left', borderaxespad=0.)
plt.grid(True)
# plt.savefig('grafico3.png', dpi=900)
plt.show()
