import requests

numero_aluno = int(input("Digite o seu Número de Aluno: "))

url = "https://restcountries.com/v3.1/all?fields=name,population,currencies"
response = requests.get(url)

if response.status_code != 200:
    print("Erro ao aceder à API")
    exit()

paises = response.json()

if not isinstance(paises, list):
    print("Erro: a API não devolveu uma lista de países.")
    print(paises)
    exit()

indice = numero_aluno % len(paises)
pais = paises[indice]

nome_pais = pais["name"]["common"]
populacao = pais["population"]

currencies = pais.get("currencies", {})
codigo_moeda = next(iter(currencies))
dados_moeda = currencies[codigo_moeda]

nome_moeda = dados_moeda.get("name", "Desconhecida")
simbolo_moeda = dados_moeda.get("symbol", "?")

indice_riqueza = populacao / len(nome_pais)

print(
    f"O país sorteado pelo aluno {numero_aluno} é {nome_pais}. "
    f"A sua moeda é {nome_moeda} ({simbolo_moeda}) "
    f"e o Índice é {indice_riqueza:.2f}."
)
