import json

class jsondb:
	def __init__(self, fname):
		self.data = None
		self.fname = fname
		try:
			self.load()
		except:
			pass

	def load(self):
		with open(self.fname, 'r') as f:
			self.data = json.loads(f.read())

	def dump(self):
		with open(self.fname, 'w') as f:
			f.write(json.dumps(self.data))

'''
# Tests
d = jsondb("test.db")

d.data = {
	"testing":"this",
	"another":"here",
	"key": {
		"many":"vals",
		"vals":"here,"
		}
	}

d.dump()

d2 = jsondb('test.db')
print d2.data
'''