from pymongo import MongoClient
from gridfs import GridFS


class DbManager:
	def __init__(self, cnn_str):
		self._client = MongoClient(cnn_str)
		self._gfs = GridFS(self.get_mongo_client().files_saver_files)

	def re_create_files_database(self):
		self.get_mongo_client().drop_database(self.get_mongo_client().files_saver_files)
		self._gfs = GridFS(self.get_mongo_client().files_saver_files)

	def get_gridFS(self):
		return self._gfs

	def get_mongo_client(self):
		return self._client

	def get_data_database(self):
		return self.get_mongo_client().files_saver_data

	def close(self):
		self._client.close()
