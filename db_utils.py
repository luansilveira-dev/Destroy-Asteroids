import sqlite3 as lite
import os

pastaPrincioal = os.path.dirname(__file__)
pastaDataBase = os.path.join(pastaPrincioal, 'data') 
BancoDados = os.path.join(pastaDataBase, 'database.db')

con = lite.connect(BancoDados)

def criarBancoDeDados():
    con = lite.connect(BancoDados)

    with con:
        cursor = con.cursor()
        cursor.execute("CREATE TABLE record(recordPontos INTEGER)")


def inserirDados(i):
    con = lite.connect(BancoDados)
    with con:
        cursor = con.cursor()
        query = ("INSERT INTO record(recordPontos) VALUES (?)")
        cursor.execute(query, i)

def verDados():
    con = lite.connect(BancoDados)
    ver_dados = []

    with con:
        cursor = con.cursor()
        query = ("SELECT * FROM record")
        cursor.execute(query)

        rows = cursor.fetchall()
        for row in rows:
            ver_dados.append(row)
        return ver_dados
    
    
def atualizarDados(i):
    con = lite.connect(BancoDados)
    with con:
        cursor = con.cursor()
        query = ("UPDATE record SET recordPontos=? WHERE recordPontos < ?")
        cursor.execute(query, i)


