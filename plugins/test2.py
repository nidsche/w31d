
class Plugin:
	def __init__(self):
		#self.tval="initialized"
		print "T2"
		self.tval='XXX'


	def getName(self):
		#testCall()
		return "Test2"


	def setter(self,val):
		self.tval=val

	def getter(self):
		return self.tval
