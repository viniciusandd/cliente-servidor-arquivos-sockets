import socket
from threading import Thread
import glob
from threading import Lock
import time
import pickle
import os

def RecebendoMensagem():
    while True:
        retorno = conexao.recv(1024)
        mensagem = pickle.loads(retorno)
        arquivos = mensagem
        ConferindoArquivos(arquivos)

def ConferindoArquivos(arquivos):
    buscados = BuscandoArquivos()
    if len(arquivos) > 0:
        for i in arquivos:
            for h in buscados:
                if i == h:
                    buscados.remove(i)

    if len(buscados) == 0:
        print("TODOS ARQUIVOS ESTÃO SINCRONIZADOS!")
    else:
        print(" --------------- SINCRONIZANDO ARQUIVOS! ---------------")
        for i in buscados:
            print(i)

    EnviandoMensagem(buscados)

def BuscandoArquivos():
    arq = []
    arq_encontrados = []
    arq_encontrados = glob.glob(diretorio + "*")
    for i in arq_encontrados:
        nome_arquivo = i[60:]
        arq.append(nome_arquivo)

    return arq

def EnviandoMensagem(arquivos):
    if len(arquivos) > 0:
        for i in arquivos:
            nome = diretorio + i
            file = open(nome, 'rb').read()
            infos = {'nome':i, 'conteudo':file}
            print(infos)
            time.sleep(0.7)
            conexao.sendall(pickle.dumps(infos))

while True:
    diretorio = input("Informe o diretório (válido) que manterá os arquivos de sua aplicação: ")

    if os.path.exists(diretorio):
        print("Diretório selecionado com sucesso, agora vamos aguardar os clientes conectarem em nosso servidor!")
        break
    else:
        print("O DIRETÓRIO NÃO EXISTE!")


#Criando um servidor
tcp   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host  = ""
porta = 12345
tupla = (host, porta)

conectou = False
while True:
    try:
        tcp.bind(tupla)  # Aceita todas conexoes dessa tupla
        conectou = True
    except Exception as e:
        porta = int(input("A porta padrão que o sistema utiliza está ocupada, informe-nos uma nova porta (informe a mesma no cliente): "))
        host  = ""
        tupla = (host, porta)

    if conectou:
        print("A porta %s foi definida com sucesso, informe-a nos clientes que vão conectar no servidor!" % porta)
        break

tcp.listen(3) # Define o máximo de conexoes simultaneas
conexao, cliente = tcp.accept()
a, b = cliente

recebendo = Thread(target=RecebendoMensagem)
recebendo.start()