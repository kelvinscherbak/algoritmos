import datetime
import sqlite3
import sys
import usuario
import cartao
import info
import saldo
import relatorios

conexao = sqlite3.connect('database.sqlite')
# sqlite3.connect('database.sqlite')
def pa(conexao,idusuario):
    cursor = conexao.cursor()
    sql = f"""SELECT primeiroacesso FROM usuario
            WHERE userid = '{idusuario}'
       """
    cursor.execute(sql)
    valor = cursor.fetchall()
    if(valor[0][0] == 1):
        finalizarCadastro(conexao,idusuario)


##Finalizar o cadastro
def finalizarCadastro(conexao,id):
    cursor = conexao.cursor()
    nome = input("Informe seu nome: ")
    sobrenome = input("Informe seu sobrenome: ")
    apelido = input("Há algum apelido ao qual deseja infomar? ")
    tel = input("Informe seu numero de celular: ")
    cpf = input("Informe seu cpf: ")

    sql = f"""INSERT INTO info(nome,sobrenome,cpf,telefone,apelido,userid) 
    VALUES("{nome}","{sobrenome}","{tel}","{cpf}","{apelido}",{id})
    """
    cursor.execute(sql)
    conexao.commit()
    sql = f"""UPDATE usuario 
    SET primeiroacesso = 0
    WHERE userid = {id}
    """
    cursor.execute(sql)
    conexao.commit()
    creditos = 9
    sql = f"INSERT INTO saldo(saldo_impressoes,userid) VALUES ({creditos},{id})"
    cursor.execute(sql)
    conexao.commit()
def criarTabelas(conexao):
    usuario.criar_tabela_usuario(conexao)
    saldo.criar_tabela_saldo(conexao)
    cartao.criar_tabela_card(conexao)
    info.criar_tabela_info(conexao)
    relatorios.criar_tabela_relatorios(conexao)

def pegaData():
    hoje = datetime.date.today()
    mes = hoje.month
    ano = hoje.year
    dia = hoje.day

    hora = datetime.datetime.now()
    h = hora.hour
    m = hora.minute
    s = hora.second
    if(h <= 10):
        h = str(h)
        h = "0" + h

    if(m <= 10):
        m = str(m)
        m = "0" + m

    if(s < 10):
        s = str(s)
        s = "0" + s

    s = str(s)
    m = str(m)
    h = str(h)
    return dia,mes,ano,h,m,s



def reg_impressao(conexao,idusuario,doc,total):
    from funcoesBanco import pegaData
    data = pegaData()
    cursor = conexao.cursor()
    sql = f"""INSERT INTO relatorios(doc_impresso,totaldepaginas,dia,mes,ano,hora,min,userid)
    VALUES ("{doc}","{total}","{data[0][0]}","{data[0][1]}","{data[0][2]}","{data[0][3]}",{idusuario})    
    
    """
    cursor.execute(sql)
    conexao.commit

conexao.close()
