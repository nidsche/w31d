import re


# indicator: Location: http://187.211.59.90/login.lp
# Set-Cookie: xAuth_SESSION_ID=WVB5FtdaJCiIbXP/IMc00gA=; path=/;

class Plugin:
	def __init__(self):
		#self.tval="initialized"
		#print "T2"
		#self.tval='XXX'
		pass


	def getName(self):
		#testCall()
		return "Detect Technicolor TG582n"

	def evalRequest(self,r):
		print "EVAL"
		print r
		return

	def evalHeader(self,r):
		er=0
		if "location" in r:
			if re.match(r"^http.*login.lp$", r['location']):
				er+=1
		if "set-cookie" in r:
			if re.match(r"^xAuth_SESSION_ID=", r['set-cookie']):
				er+=1
		#for h in r:
		#	print "## "+h		
		return er

	def setter(self,val):
		self.tval=val
		return

	def getter(self):
		#return self.tval
		pass
