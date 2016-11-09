import unittest
import app
import json


class TestBuild(unittest.TestCase):
	
	def setUp(self):
		self.app = app.app.test_client()


	def tearDown(self):
		pass


	def test_new_build(self):
		postbuild = self.app.post('/build', data={'path'='https://github.com/mat105/GITPYTHONTESTS.git'})

		assert postbuild.statuscode == 200

		data = postbuild.get_json()

		assert data != None
		
		getbuild = self.app.get('/build/'+data['id'])

		assert getbuild.statuscode == 200

		data = getbuild.get_json()

		assert data != None

		assert data['finished'] == False


if __name__ == '__main__':
	unittest.main()
