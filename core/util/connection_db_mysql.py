import mysql.connector
from mysql.connector import errorcode

def abrirConexao():
    try:
        cnx = mysql.connector.connect(user='phoenix', password='aq1sw2de3fr4', database='projeto_phoenix')
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("=======================================Usuario ou senha invalidos!")
            return ""
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("=======================================Banco de dados inexistente")
            return ""
        else:
            return err


def fecharConexao(cursor, cnx):
    cursor.close()
    cnx.close()
