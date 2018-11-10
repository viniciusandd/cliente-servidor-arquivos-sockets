import socket
from threading import Thread
import glob
import time
import pickle
import subprocess
import os

def RecebendoMensagens():
    while True:
        try:
            retorno = cliente.recv(6053)
            infos = pickle.loads(retorno)

            nome = infos['nome']
            conteudo = infos['conteudo'].decode()

            arquivo = diretorio + nome

            comando = "touch %s && echo '%s' > %s" % (arquivo, conteudo, arquivo)

            subprocess.check_output(comando, shell=True)

        except Exception as e:
            print("Erro: % s" % e)

def EnviandoMensagens():
    while True:
        arquivos = BuscandoArquivos()
        cliente.send(pickle.dumps(arquivos))
        time.sleep(5)

def BuscandoArquivos():
    arquivos = []
    arquivos_encontrados = []
    arquivos_encontrados = glob.glob(diretorio + "*")
    for i in arquivos_encontrados:
        nome_arquivo = i[60:]
        arquivos.append(nome_arquivo)

    return arquivos

while True:
    diretorio = input("Informe o diretório que receberá os arquivos: ")

    if os.path.exists(diretorio):
        print("Diretório selecionado com sucesso, agora a sincronização entre seu repositório e o de nosso servidor é AUTOMÁTICA!")
        break
    else:
        print("O DIRETÓRIO INFORMADO NÃO EXISTE!")

host = "localhost"
porta = 12345
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tupla = (host, porta)
cliente.connect(tupla)

recebendo = Thread(target=RecebendoMensagens)
recebendo.start()

enviando = Thread(target=EnviandoMensagens)
enviando.start()

