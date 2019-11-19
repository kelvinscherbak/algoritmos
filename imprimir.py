import tempfile
import win32api
import win32print
import os
import sys
import menus
from funcoesBanco import reg_impressao
from PyPDF2 import PdfFileReader
def numpage(arquivo): 
    for path in arquivo:
        pdf_reader = PdfFileReader(path)
    return pdf_reader.getNumPages()

def impress(conexao,id):
    global nome
    lista = os.listdir()
    # print(lista)
    for i in range(len(lista)):
        # numero = i + 1
        print(i,lista[i])
    selec = input("Qual numero do arquivo desejado:  ")
    if(selec == ""):
        sys.exit()
    selec = int(selec)
    nome = lista[selec]
    arquivo = [nome]
    if(".pdf" not in nome):
        print("Este arquivo não é um arquivo valido")
        sys.exit()
    numero = numpage(arquivo)
    saldo = menus.consultarSaldo(conexao,id)
    if(numero <= saldo[0][0]):
        print("saldo insuficiente!")
        exit
        sys.exit()
    r = input(f"Deseja imprimir um total de {numero} páginas?")
    r = str.upper(r)
    if(r == "S"):
        try:
            print(f"Imprimindo {nome}")
            print("impresso com sucesso")
            reg_impressao(conexao,id,nome,numero)
        except:
            print("Erro na impressão, tente novamente")
        return numero