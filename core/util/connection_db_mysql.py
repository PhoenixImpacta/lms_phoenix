import mysql.connector
from mysql.connector import errorcode

def abrirConexao():
    try:
        cnx = mysql.connector.connect(user='phoen598_admin', password='phoenix', database='phoen598_desenv', host='192.185.217.18')
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("=======================================Usuario ou senha invalidos!")
            print(err.errno)
            return ""
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("=======================================Banco de dados inexistente")
            return ""
        else:
            return err


def fecharConexao(cursor, cnx):
    cursor.close()
    cnx.close()
