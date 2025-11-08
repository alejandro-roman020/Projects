import requests
import sqlite3

connection = sqlite3.connect("histórico_de_moedas.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS moedas (id INTEGER PRIMARY KEY, moeda_origem TEXT, valor_origem FLOAT, " \
"moeda_destino TEXT, valor_destino FLOAT)")

while True:
    choice = input("Você quer converter uma moeda para outra, ver seu histórico ou sair? "
    "(1- converter, 2- histórico, 3- sair)\n>")
    if choice == "1":
        moeda_origem = input("Coloque a moeda origem (Ex: BRL)\n>").upper()
        valor_origem = float(input("Insira o valor que deseja converter\n"))
        moeda_destino = input("Coloque a moeda destino (Ex: USD)\n>").upper()
        url = f"https://open.er-api.com/v6/latest/{moeda_origem}"
        resposta = requests.get(url)
        dados = resposta.json()
        valor_destino = valor_origem * dados["rates"][moeda_destino]
        print(f"O valor {valor_origem:.2f} na moeda {moeda_origem} em {moeda_destino} é {valor_destino:.2f}")
        cursor.execute("INSERT INTO moedas (moeda_origem, valor_origem, moeda_destino, valor_destino) VALUES (?, ?, ?, ?)", 
        (moeda_origem, round(valor_origem, 2), moeda_destino, round(valor_destino, 2)))
        connection.commit()
    elif choice == "2":
        cursor.execute("SELECT * FROM moedas")
        moedas = cursor.fetchall()
        for moeda in moedas:
            print(f"{moeda[0]}: {moeda[1]} {moeda[2]} = {moeda[3]} {moeda[4]}")
    else:
        print("Saída do programa selecionada!")
        break

connection.close()
