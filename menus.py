import sqlite3
import sys
import logar
import imprimir
import funcoesBanco
import registrar
import recuperar
conexao = sqlite3.connect('database.sqlite')
def mainMenu():
    print("""
    Bem-vindo selecione a opção desejada: 
    \t1 - Logar\n
    \t2 - Registrar\n
    \t3 - Recuperar senha\n
    \t0 - Sair do sistema \n
    """)


def menuLogin():
    print("""
    \n\n
    Selecione a opção desejada:
    \t1 - Imprimir novo arquivo\n
    \t2 - Consultar saldo \n
    \t3 - Realizar Recarga\n
    \t4 - Configurações\n\n
    \t0 - Deslogar \n
    """)


def config():
    print("""
    \n\n
    Selecione a opção desejada:
    \t1 - Ver dados\n
    \t2 - Alterar Email \n
    \t3 - Alterar senha\n
    \t4 - Ver ultimas impressões \n\n
    \t0 - Voltar \n
    """)


# Abre uma conexão como banco de dados

cursor = conexao.cursor()
def selOpcao(conexao):
    cursor = conexao.cursor()
    while(True):
        mainMenu()
        op = int(input("Informe a opção desejada: "))
        if(op == 0):
            print("Você escolheu sair! :( ")
            sys.exit()
        elif(op == 1):
            iduser = logar.logar(conexao)
            iduser = int(iduser)
            funcoesBanco.pa(conexao,iduser)
            if(iduser!= False):
                return iduser
                break
            elif(iduser == False):
                print("Erro ao logar")
        elif(op == 2):
           registrar.registrar(conexao)
        elif(op == 3):
            recuperar.recuperacao(conexao)



def inserirSaldo(conexao, idusuario):
    cursor = conexao.cursor()
    print("inserirsaldo")
    creditos = int(input("Quantos creditos deseja inserir? "))
    idusuario = int(input("Quantos creditos deseja inserir? "))

    sql = f"""INSERT INTO saldo(saldo_impressoes,userid) VALUES ({creditos},{idusuario})
    """
    cursor.execute(sql)
    conexao.commit
def consultarSaldo(conexao,idusuario):
    cursor = conexao.cursor()
    sql = f"""SELECT saldo_impressoes FROM saldo
            INNER JOIN usuario
            ON saldo.userid = usuario.userid
            WHERE usuario.userid = {idusuario} """
    cursor.execute(sql)
    saldo = cursor.fetchall()
    return saldo
def impressao(conexao,idusuario):
    saldo = consultarSaldo(conexao,idusuario)
    print(saldo[0][0])
    if(saldo[0][0] == "" or saldo[0][0] == 0):
        inserirSaldo(conexao, idusuario)
    elif(saldo[0][0] > 0):
        total = imprimir.impress(conexao,idusuario)
        novosaldo = total - saldo[0][0]
        sql = f"""UPDATE saldo SET saldo_impressoes = ({novosaldo})
                    WHERE userid = {idusuario}
    """
        cursor.execute(sql)
        conexao.commit


def menuLogado(conexao, idusuario):
    conexao = sqlite3.connect('database.sqlite')
    cursor = conexao.cursor()
    menuLogin()
    while(True):
        op = int(input("Opção: "))
        if(op == 1):
           impressao(conexao,idusuario)
           menuLogin()
        
        if(op == 4):
                menuConfig(conexao,idusuario)
        if(op == 0):
            break
            sys.exit()
# Fecha a conexão que foi criada com banco de dados
    conexao.close()



def verDados(conexao,idusuario):
    cursor = conexao.cursor()
    sql = f""" SELECT * FROM info
            WHERE userid = {idusuario} """
    cursor.execute(sql)
    consulta = cursor.fetchall()
    print("Informeações:")
    print("\n\tNome: ",consulta[0][1])
    print("\n\tSobrenome: ", consulta[0][2])
    print("\n\tApelido: ", consulta[0][5])
    print("\n\tCelular: ",consulta[0][3])
    print("\n\tCPF:", consulta[0][4])

def alterarEmail(conexao,idusuario):
    cursor = conexao.cursor()
    sql = f"""SELECT senha FROM usuario
                   WHERE userid = {idusuario}
       """
    cursor.execute(sql)
    senha = cursor.fetchall()
    senhainformada = input("Informe a sua senha: ")
    if(senha[0][0] == senhainformada):
            email = input("Informe o novo email: ")
            cemail = input("Confirme o email novamente: ")
            c = 0
            while(email != cemail):
                email = input("Informe o novo email: ")
                cemail = input("Confirme o email novamente:")
                c += 1
                if(c == 4):
                    print("Numero excedido de tentativas.")
                    sys.exit()
            sql = f"""UPDATE usuario SET email = "{cemail}"
                    WHERE userid = {idusuario}
            
            """
            cursor.execute(sql)
            conexao.commit()
            print("Email Alterado com sucesso, seu novo email > ", email)
    else:
        print("Senha Incorreta!")

def alterarSenha(conexao,idusuario):
    cursor = conexao.cursor()
    sql = f"""SELECT senha FROM usuario
                   WHERE userid = {idusuario}
       """
    cursor.execute(sql)
    senha = cursor.fetchall()
    conferirsenha = input("Informe a sua senha atual: ")
    
    if(senha[0][0] == conferirsenha):
            novasenha = input("Informe a sua nova senha: ")
            confirmarsenha = input("Confirme sua nova senha: ")
            while(novasenha != confirmarsenha):
                print("Senha incorreta")
                novasenha = input("Informe a sua nova senha: ")
                confirmarsenha = input("Confirme sua nova senha: ")


    sql = f"""UPDATE usuario SET senha = "{novasenha}"
                    WHERE userid = {idusuario}"""
    cursor.execute(sql)
    conexao.commit()
    print("Senha alterada com sucesso, sua nova senha > ", novasenha)        

def menuConfig(conexao,idusuario):
    cursor = conexao.cursor()
    op = None
    while(op != 0):
        config()
        op = int(input("Opção de config: "))
        if(op == 1):
            verDados(conexao,idusuario)

        if(op == 2):
            alterarEmail(conexao,idusuario)
        if(op == 3):
            alterarSenha(conexao,idusuario)
        if(op == 0):
            menuLogin()


# menuConfig(conexao,4)
conexao.close()
