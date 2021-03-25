import sqlite3, random, os


def createDB():
	os.chdir('userData')
	con = sqlite3.connect('userData.db')
	con.close()


def createTable():
	con = sqlite3.connect('userData.db')
	cur = con.cursor()
	cur.execute('''CREATE TABLE data
				(URL_Entry text, Login text, Dec_password text, Raw_db_pwd_data text, Nonce text, Password_cipher text)''')
	con.commit()
	con.close()



def dataFill(URL_Entry, Login, Dec_password, Raw_db_pwd_data, Nonce, Password_cipher):
	con = sqlite3.connect('userData.db')
	cur = con.cursor()
	cur.execute(f"INSERT INTO data VALUES ('{URL_Entry}', '{Login}', '{Dec_password}', '{Raw_db_pwd_data}', '{Nonce}', '{Password_cipher}')")
	con.commit()

