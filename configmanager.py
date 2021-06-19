import json
from os import path


class ConfigManager:
	'''
			Class that represents configuration of the program
	'''

	def __init__(self, cnn: str):
		if cnn.isspace():
			raise ValueError(cnn)

		self.config = {
			'cnn': cnn
		}

	def get_connection_string(self):
		return str(self.config['cnn'])


class JsonConfigManager(ConfigManager):
	'''
			Manager to read / write configuration of the program.
	'''

	file_name = 'configuration.json'

	def __init__(self, dir):
		self.dir = str(dir)
		self.dir = path.abspath(self.dir)

		if not path.isdir(self.dir):
			raise NotADirectoryError

		self.config_path = path.join(self.dir, self.file_name)

	def get_connection_string(self):
		return str(self._read_config()['MongoConnection'])

	def set_connection_string(self, cnn):
		if self._config_exists():
			config = self._read_config()
			config['MongoConnection'] = cnn
		else:
			config = {
				'MongoConnection': cnn
			}

		self._write_config(config)

	def set_files_to_exclude(self, files: list):
		if self._config_exists():
			config = self._read_config()
			config['ExcludedFiles'] = files
		else:
			config = {
				'ExcludedFiles': files
			}

		self._write_config(config)

	def get_files_to_exclude(self):
		return list(self._read_config()['ExcludedFiles'])

	def _read_config(self):
		file = open(self.config_path, 'r')
		content = file.read()
		file.close()
		return json.loads(content)

	def _write_config(self, text):
		file = open(self.config_path, 'w')
		file.write(json.dumps(text))
		file.close()

	def _config_exists(self):
		return path.exists(self.config_path)
