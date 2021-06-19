import argparse


class ProgramInput:
	'''
	Parses console input of the program.
	'''

	def __init__(self):
		self._input_parser = argparse.ArgumentParser(
			description='Backup utility')

		parent_parser = argparse.ArgumentParser(add_help=False)
		parent_parser.add_argument(
			'--cnn', '--connection-string', '-c', dest='connection_string', metavar='connection-string', type=str,
			help='the connection string to be used to connect to a database (MongoDb only)'
		)

		subparsers = self._input_parser.add_subparsers()
		retrieval_parser = subparsers.add_parser(
			'retrieve', help='Get information form the database', parents=[parent_parser])
		putting_parser = subparsers.add_parser(
			'put', help='Save file to the database', parents=[parent_parser])
		removing_parser = subparsers.add_parser(
			'remove', help='Remove file from the database')
		config_parser = subparsers.add_parser(
			'config', help='Manager the configuration')

		retrieval_parsers = retrieval_parser.add_subparsers()
		retrieval_parsers.add_parser('names', parents=[parent_parser]).add_argument(
			'--names', default=True, action='store_true', help=argparse.SUPPRESS)
		file_retrieval_parser = retrieval_parsers.add_parser(
			'file', parents=[parent_parser])
		file_retrieval_parser.add_argument(
			'--file-name', '-n', type=str, required=True, help='The name of the file to retrieve')
		file_retrieval_parser.add_argument('--directory', '-d', type=str, required=True,
										   dest='fs_dir', metavar='directory', help='Directory to save the file')
		file_retrieval_parser.add_argument(
			'--remove', '-r', action='store_true', default=False, help='Remove file after retrieval')

		putting_parser.add_argument(
			'path', action='extend', nargs='+', metavar='path', type=str, help='The path to the file to back up'
		)
		putting_parser.add_argument('--recursive', '-r', action='store_true', default=False,
									help='If directory is passed, whether to save files from subdirectories or not')

		removing_parser_group = removing_parser.add_mutually_exclusive_group()
		removing_parser_group.add_argument(
			'--file-name', type=str, help='The name of the file to delete')
		removing_parser_group.add_argument(
			'--all', action='store_true', default=False, help='Remove all files from the database')

		config_subparsers = config_parser.add_subparsers()
		set_config_parsers = config_subparsers.add_parser(
			'set', help='Change configuration').add_subparsers()

		set_config_cnn_parsers = set_config_parsers.add_parser('connection')
		set_config_cnn_parsers.add_argument(
			'connection', type=str, help='Connections string')

		self._exec_parser()

	def get_paths(self) -> 'list[str]':
		return self.argvals.path

	def has_paths(self):
		return hasattr(self.argvals, 'path')

	def find_files_recursively(self):
		return hasattr(self.argvals, 'recursive') and self.argvals.recursive

	def get_name_of_file_to_retrieve(self):
		return self.argvals.file_name

	def has_file_name_to_retrieve(self):
		return hasattr(self.argvals, 'file_name')

	def get_directory_to_retrieve_to(self):
		return self.argvals.fs_dir

	def has_directory_to_retrieve_to(self):
		return hasattr(self.argvals, 'fs_dir')

	def get_connection_string(self) -> str:
		return self.argvals.connection_string

	def has_connection_string(self):
		return hasattr(self.argvals, 'connection_string') and self.argvals.connection_string is not None

	def need_to_retrieve_names(self) -> bool:
		return hasattr(self.argvals, 'names')

	def get_file_to_delete(self):
		return self.argvals.file_name

	def has_file_to_delete(self):
		return hasattr(self.argvals, 'file_name') and self.argvals.file_name is not None

	def remove_all_files(self):
		return hasattr(self.argvals, 'all') and self.argvals.all

	def remove_file_after_retrieval(self) -> bool:
		return self.argvals.remove

	def get_config_connection_string(self):
		return self.argvals.connection

	def has_config_connection_string(self):
		return hasattr(self.argvals, 'connection')

	def print_usage(self):
		self._input_parser.print_usage()

	def print_help(self):
		self._input_parser.print_help()

	def _exec_parser(self):
		self.argvals = self._input_parser.parse_args()
