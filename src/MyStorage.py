class Storage:
	def __init__(self):
		self.item1 = None
		self.item2 = None
		self.item3 = None
		self.item4 = None
		self.item5 = None
		self.item6 = None
		self.item7 = None
		self.item8 = None
		self.item9 = None
		self.item10 = None
		
	def getter(self, item):
		if item == "item1":
			return(self.item1)
		elif item == "item2":
			return(self.item2)
		elif item == "item3":
			return(self.item3)
		elif item == "item4":
			return(self.item4)
		elif item == "item5":
			return(self.item5)
		elif item == "item6":
			return(self.item6)
		elif item == "item7":
			return(self.item7)
		elif item == "item8":
			return(self.item8)
		elif item == "item9":
			return(self.item9)
		elif item == "item10":
			return(self.item10)
		else:
			return(False)
	
	def setter(self, item, value):
		if item == "item1":
			self.item1 = value
		elif item == "item2":
			self.item2 = value
		elif item == "item3":
			self.item3 = value
		elif item == "item4":
			self.item4 = value
		elif item == "item5":
			self.item5 = value
		elif item == "item6":
			self.item6 = value
		elif item == "item7":
			self.item7 = value
		elif item == "item8":
			self.item8 = value
		elif item == "item9":
			self.item9 = value
		elif item == "item10":
			self.item10 = value
		else:
			return(False)
