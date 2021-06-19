from io import FileIO
from data.repositories.namesrepo import NamesRepo
from data.repositories.repo import Repo
from os import path
import hashlib


class FilesRepo(Repo):
	'''
	Repository for working with the stored files.
	'''

	def __init__(self):
		self.names_repo = NamesRepo()
		super().__init__()

	def get(self, file_name: str) -> FileIO:
		id = self._hash_str(file_name)
		gfs = self.db_manager.get_gridFS()

		if not gfs.exists(id):
			raise FileNotFoundError

		return gfs.get(id)

	def save(self, file_path: str) -> str:
		if not path.isfile(file_path):
			raise FileNotFoundError

		file_name = self._get_file_name(path.basename(file_path))
		self.names_repo.save_name(file_name)
		self._save_file(open(file_path, 'rb'), file_name)

		return file_name

	def remove(self, file_name: str):
		gfs = self.db_manager.get_gridFS()
		id = self._hash_str(file_name)

		if gfs.exists(id):
			gfs.delete(id)

		self.names_repo.remove(file_name)

	def remove_all(self):
		self.db_manager.re_create_files_database()
		self.names_repo.remove_all()

	def exists(self, file_name: str):
		return self.db_manager.get_gridFS().exists(self._hash_str(file_name))

	def _save_file(self, file, file_name: str):
		id = self._hash_str(file_name)
		gfs = self.db_manager.get_gridFS()

		if not gfs.exists(id):
			gfs.put(file, _id=id)

	def _get_file_name(self, name: str):
		if not self.names_repo.exists(name):
			return name

		templ = name + ' ({})'
		i = 1
		while self.names_repo.exists(templ.format(i)):
			i+=1

		return templ.format(i)

	@staticmethod
	def _hash_str(text: str):
		sha = hashlib.sha256()
		sha.update(text.encode())
		return sha.hexdigest()
