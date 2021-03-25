from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import sqlite3, time, os
import dbExt


dbExt.createDB()
print('db created!')
time.sleep(0.5)

dbExt.createTable()
print('table created!')
time.sleep(0.5)


conn = sqlite3.connect('loginData')
cursor = conn.cursor()
cursor.execute('SELECT action_url, username_value, password_value FROM logins')
data = cursor.fetchall()

key = open('encryptKey', 'rb').read()
aesgcm = AESGCM(key)
print("[+] AES256 GCM key dumped: " + "".join('%02X' % c for c in key) + "\n")

event = 0
for i in range(len(data)):
	pwdcipher = data[i][2][15:]
	nonce = data[i][2][3:15]
	decPassword = aesgcm.decrypt(nonce, pwdcipher, None).decode()
	nonce = str("".join('%02X' % c for c in nonce))
	PasswordCipher = str("".join('%02X' % c for c in pwdcipher))
	Raw_db_pwd_data = str("".join('%02X' % c for c in data[i][2]))
	url = str(data[i][0])
	login = str(data[i][1])
	event+=1
	print(event, '/', len(data))
	dbExt.dataFill(url, login, decPassword, Raw_db_pwd_data, nonce, PasswordCipher)

input('Finised. Press any key.')
