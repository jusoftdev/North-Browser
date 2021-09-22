import os
import random


#os.rename(y, x)
#Changes directory to previous
olddir = os.getcwd()
os.chdir("../../")
ndir = os.getcwd()
olddir = olddir.replace(ndir + "\\", "")
nogit = True

print(os.listdir())
dir = os.listdir()
dst = ""
f = False

for _ in range(1, 100001):
	if not "Jusoft-Browser_v" + str(_) in os.listdir() and not f:
		dst = "Jusoft-Browser_v" + str(_)
		f = True

if dst == "":
	dst = "Jusoft-Browser"

input("PRESS ENTER TO BEGINN")
k = input("This will update your System and install some tools, type \"y\" to confirm: ")
if k == "y":
	try:
		a = os.system("sudo apt-get update")
		b = os.system("sudo apt-get upgrade")
		c = os.system("sudo apt-install git-all")
		d = os.system("sudo apt install python-wheel")
		if a == 1 or b == 1 or c == 1 or d == 1:
			e = os.system("apt-get update")
			f = os.system("apt-get upgrade")
			g = os.system("apt-install git-all")
			h = os.system("sudo apt install python-wheel")
			if e == 1 or f == 1 or g == 1 or h == 1:
				nogit = True
	except:
		try:
			os.system("apt-get update")
			os.system("apt-get upgrade")
			os.system("apt-install git-all")
			os.system("sudo apt install python-wheel")
		except:
			nogit=True


k = input("This will install new Version and needed requirements after that it starts the Browser, type \"y\" to confirm: ")
if k == "y":
	try:
		#Clones new version from Github
		i = os.system("git clone https://github.com/Lynix152/Jusoft-Browser.git " + str(dst))
		if i == 0:
			nogit = False
		os.system("pip install --upgrade pip")
		print("Successfully upgraded pip!")
		if not nogit:
			os.chdir(str(dst))
			os.system("pip install -r requirements.txt")
			print("Successfully installed requirements!")
			os.system("pip install --upgrade -r requirements.txt")
			print("Successfully upgraded requirements!")
			print("Successfully downloaded new Version!")
			os.chdir("src")
		try:
			if nogit:
				print("Please install git!")
				os.chdir(olddir)
				os.system("python main.py newvgit")
			else:
				os.system("python main.py newv")
					
		except:
			print("Failed to start Browser!")
	except:
		try:
			if nogit:
				print("Please install git!")
				os.chdir(olddir)
				os.system("python main.py newvgit")
			else:
				print("You have Git!")
				os.system("python main.py newv")
		except:
			print("Failed to start Browser!")
		print("Error by downloading new version, please check if the Server is avaiable and if you installed git!")

if nogit:
	print("Installation failed!!!")
	print("Please install Git!!!")
else:
	print("You can simply start your Browser py typing python {}\\main.py".format(os.getcwd()))
input("PRESS ENTER TO FINISH")
