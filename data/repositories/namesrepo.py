from data.repositories.repo import Repo


class NamesRepo(Repo):
	def save_name(self, name):
		self._get_file_names_collection().insert_one(self._get_doc(name))

	def get_all(self):
		return [i['name'] for i in self._get_file_names_collection().find()]

	def remove(self, name):
		self._get_file_names_collection().delete_one({'name': name})

	def remove_all(self):
		self._get_file_names_collection().drop()
		self._get_file_names_collection()

	def exists(self, name):
		return self._get_file_names_collection().find_one({'name': name}) is not None

	@staticmethod
	def _get_doc(name):
		return {
			'name': name
		}

	def _get_file_names_collection(self):
		return self.db_manager.get_data_database().file_names
