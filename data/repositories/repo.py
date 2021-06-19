from configmanager import ConfigManager
from data.db import DbManager

_config : ConfigManager

def set_config(config: ConfigManager):
	global _config
	_config = config

def get_config():
	return _config

class Repo:

	def __init__(self):
		self.db_manager = DbManager(_config.get_connection_string())
