
class Plugin:
	def __init__(self):
		#self.tval="initialized"
		print "TTTT"
		self.tval='nope'


	def getName(self):
		#testCall()
		return "TestPlugin"


	def setter(self,val):
		self.tval=val

	def getter(self):
		return self.tval
