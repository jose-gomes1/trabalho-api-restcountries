import requests
import pyttsx3
import sys

# -------------------------------
# Force Portuguese (Portugal)
# -------------------------------
def configurar_pt_pt(engine):
    voices = engine.getProperty('voices')
    for voice in voices:
        name = voice.name.lower()
        langs = str(voice.languages).lower()

        # Strict pt-PT preference
        if "pt-pt" in name or "pt-pt" in langs:
            engine.setProperty('voice', voice.id)
            return True

    # Fallback: any Portuguese
    for voice in voices:
        name = voice.name.lower()
        langs = str(voice.languages).lower()
        if "portuguese" in name or "pt" in langs:
            engine.setProperty('voice', voice.id)
            return True

    return False


# -------------------------------
# Input
# -------------------------------
try:
    numero_aluno = int(input("Digite o seu Número de Aluno: "))
except ValueError:
    print("Número inválido.")
    sys.exit(1)

# -------------------------------
# API Request
# -------------------------------
url = "https://restcountries.com/v3.1/all?fields=name,population,currencies"
response = requests.get(url, timeout=10)

if response.status_code != 200:
    print("Erro ao aceder à API.")
    sys.exit(1)

paises = response.json()

if not isinstance(paises, list):
    print("Erro: resposta inválida da API.")
    sys.exit(1)

# -------------------------------
# Country selection
# -------------------------------
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

mensagem = (
    f"O país sorteado pelo aluno {numero_aluno} é {nome_pais}. "
    f"A sua moeda é {nome_moeda}, com o símbolo {simbolo_moeda}. "
    f"O índice é {indice_riqueza:.2f}."
)

print(mensagem)

# -------------------------------
# SPEAK (engine 1)
# -------------------------------
engine_speak = pyttsx3.init()
engine_speak.setProperty('rate', 160)
if not configurar_pt_pt(engine_speak):
    print("⚠️ Aviso: voz pt-PT não encontrada, usando padrão.")

engine_speak.say(mensagem)
engine_speak.runAndWait()
engine_speak.stop()

# -------------------------------
# SAVE TO FILE (engine 2)
# -------------------------------
engine_save = pyttsx3.init()
engine_save.setProperty('rate', 160)
configurar_pt_pt(engine_save)

engine_save.save_to_file(mensagem, "audio.wav")
engine_save.runAndWait()
engine_save.stop()
