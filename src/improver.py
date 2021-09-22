import man_db
from PyQt5.QtWidgets import QCompleter

class Improver:
	def __init__(self, path):
		Man_db = man_db.Man_Db(str(path))
		self.data = Man_db.read_db_history("url")

	def improve(self):
		data = self.data
		data = list(data)
		for x in range(0, len(data)):
			data[x] = str(data[x])
			data[x] = data[x].replace("'", "")
			data[x] = data[x].replace("(", "")
			data[x] = data[x].replace(")", "")
			data[x] = data[x].replace(",", "")
		completer = QCompleter(data)
		return(completer)
