import sqlite3

def criar_tabela_relatorios(conexao):
    conexao = sqlite3.connect('database.sqlite')
    cursor = conexao.cursor()
    sql = """
        CREATE TABLE IF NOT EXISTS relatorios (
            id_relatorios INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_impresso TEXT NOT NULL UNIQUE,
            totaldepg integer NOT NULL UNIQUE,
            dia char(2) NOT NULL,
            mes char(2) NOT NULL,
            ano char(4) NOT NULL,
            hora char(2) NOT NULL,
            min char(2) NOT NULL,

            userid INTEGER NOT NULL,
            FOREIGN KEY (userid) REFERENCES usuario(userid)
        )
    """
    cursor.execute(sql)
    conexao.close()
