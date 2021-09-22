#https://www.youtube.com/watch?v=mqhxxeeTbu0&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX
from flask import Flask, render_template, request, redirect, url_for
import os
import man_db
import MyStorage
from datetime import datetime

Man_db = man_db.Man_Db(path="..\\ressources\\data\\db.db")
storage = MyStorage.Storage()

p = str(os.getcwd())
p = p.replace("\src", "")
p = p + "\\ressources\\templates"
app = Flask(__name__, template_folder=str(p))



@app.route("/")
def index():
	return render_template("index.html")


@app.route("/history/", methods=["POST", "GET"])
def history():

	page = request.args.get("page")
	prevp = request.args.get("previouspage")
	nextp = request.args.get("nextpage")
	pp = storage.getter(item="item1")
	if pp == None:
		pp = 1
	if page == None:
		if prevp and nextp == None:
			page = 1
		elif prevp == "True":
			page = int(pp) - 1
		elif nextp == "True":
			page = int(pp) + 1
		else:
			page = 1


	storage.setter("item1", page)

	p1=1
	p2=2
	p3=3
	p4=4
	p5=5

	url_history = []
	date_history = []
	history = Man_db.read_db_history(item="Url, Date", Order="ORDER BY Date DESC")
	for x in range(0, len(history)):
		url, date = history[x]
		url_history.append(url)
		date_history.append(date)
	for x in range(0, len(date_history)-1):
		if date_history[x] != "":
			date_history[x] = datetime.strptime(date_history[x], "%Y-%m-%d %H:%M:%S.%f")
			date_history[x] = date_history[x].strftime("%m/%d/%Y, %H:%M:%S")



	dates = []
	urls = []
	page = int(page)
	max = page*10
	for x in range(int(max)-11, int(max)-1):
		try:
			urls.append(url_history[x])
			dates.append(date_history[x])
		except:
			urls.append("")
			dates.append("")


	if urls[9] == "" or dates[9] == "":
		p1 = ""
		p2 = ""
		p3 = ""
		p4 = ""
		p5 = ""

	return render_template("history.html", url1=urls[0], url2=urls[1], url3=urls[2], url4=urls[3], url5=urls[4], url6=urls[5], url7=urls[6], url8=urls[7], url9=urls[8], url10=urls[9],
						   date1=dates[0], date2=dates[1], date3=dates[2], date4=dates[3], date5=dates[4], date6=dates[5], date7=dates[6], date8=dates[7], date9=dates[8], date10=dates[9],
						   p1=p1, p2=p2, p3=p3, p4=p4, p5=p5)


@app.route("/newv")
def newv():
	return render_template("newv.html")

@app.route("/darkmode")
def darkmode():
	return render_template("darkmode.html")

@app.route("/whitemode")
def whitemode():
	return render_template("whitemode.html")


@app.route("/https_warning")
def https_warning():
	return render_template("https_warning.html")

@app.route("/error_404")
def error_404():
	return render_template("404.html")

@app.route("/source")
def source():
	return render_template("cpage.html")


if __name__ == "__main__":
	app.run(host="localhost", port=80)
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True