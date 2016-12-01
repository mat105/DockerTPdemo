import unittest
import app
import json

from base64 import b64encode


class TestBuild(unittest.TestCase):
	
	def setUp(self):
		self.app = app.app.test_client()


	def tearDown(self):
		pass

	def test_new_build(self):
		headers = {
			'Authorization': 'Basic ' + b64encode("{0}:{1}".format('admin', 'admin'))
		}

		total_builds = self.app.get('/build', headers=headers)

		assert total_builds.status_code == 200

		postbuild = self.app.post('/build', data={'path':'https://github.com/mat105/GITPYTHONTESTS.git'}, headers=headers)

		assert postbuild.status_code == 200

		
		getbuild = self.app.get('/build/'+data['id'], headers=headers)

		assert getbuild.status_code == 200


if __name__ == '__main__':
	unittest.main()
