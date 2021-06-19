import os
from configmanager import *
from programargs import ProgramInput
from data.repositories import repo
from data.repositories.filesrepo import FilesRepo
from data.repositories.namesrepo import NamesRepo
import sys
from helpers import pathhelper, filehelper


def ask_yes_no_question(question: str) -> bool:

	print(f'{question} (Y/n)')
	ans = input()
	if (not ans) or ans.isspace() or ans.lower() == 'y':
		return True
	elif ans.lower() == 'n':
		return False
	else:
		return ask_yes_no_question(question)


def get_configuration(program_input: ProgramInput):
	if program_input.has_connection_string():
		return ConfigManager(program_input.get_connection_string())

	return JsonConfigManager(os.getcwd())


def save_files_from_dir(dir, i: int = 1, recursive=False):
	pic_repo = FilesRepo()
	excluded_files = JsonConfigManager(os.getcwd()).get_files_to_exclude()

	def save_files(dir, files):
		nonlocal i
		for file in files:
			if file not in excluded_files:
				print(f'Saving file ({i})...')
				file_name = pic_repo.save(os.path.join(dir, file))
				print(f'Name assigned to the file: {file_name}')
				i += 1

	if not recursive:
		file_names = next(os.walk(dir), (None, None, []))[2]
		save_files(dir, file_names)
	else:
		for cur_dir, _, file_names in os.walk(dir):
			save_files(cur_dir, file_names)

	return i


def save_files(paths: 'list[str]', recursively = False):
	pic_repo = FilesRepo()

	if len(paths) == 1:
		paths[0] = os.path.abspath(paths[0])

		if os.path.isfile(paths[0]):
			print('Saving file...')
			file_name = pic_repo.save(paths[0])
			print('Saved!')
			print(f'Name assigned to the file: {file_name}')
		elif os.path.isdir(paths[0]):
			size = pathhelper.calc_dir_size(paths[0], recursively)
			size = filehelper.convert_bytes(size)

			print(f'The total size of files to save is {"{:,}".format(round(size[0], 1))} {size[1]}')

			if ask_yes_no_question(f'Save files?'):
				save_files_from_dir(paths[0], recursive=recursively)
			else:
				sys.exit()
		else:
			print(f'Given path is invalid: {paths[0]}')
			sys.exit()
	else:
		i = 1
		try:
			size = pathhelper.calc_paths_size(paths, recursively)
		except IOError as ioerr:
			print(str(ioerr))
			sys.exit()

		size = filehelper.convert_bytes(size)

		print(f'The total size of files to save is {"{:,}".format(round(size[0], 1))} {size[1]}')

		if not ask_yes_no_question(f'Save files?'):
			sys.exit()

		for path in paths:
			path = os.path.abspath(path)

			if os.path.isfile(path):
				print(f'Saving file ({i})...')
				file_name = pic_repo.save(path)
				print(f'Name assigned to the file: {file_name}')
				i += 1
			elif os.path.isdir(path):
				i = save_files_from_dir(path, i, recursively)

		print('Done')


def retrieve_file(file_name, dir):

	if not os.path.isdir(dir):
		print('Given directory path is invalid')
		sys.exit(0)

	pic_repo = FilesRepo()
	print('Retrieving file...')

	try:
		file = pic_repo.get(file_name)
	except FileNotFoundError:
		print('There is no file with the given name.')
		sys.exit(0)

	print('Writing to the file..')
	filehelper.write_from_file_to_file(file, os.path.join(dir, file_name))
	print('Done')


def retrieve_names():
	names_repo = NamesRepo()
	print('Retrieving...')
	i = 1
	for name in names_repo.get_all():
		print(f'{i}. {name}')
		i += 1

	if i == 1:
		print('There are no entries')


def remove_file(name):
	files_repo = FilesRepo()
	print('Removing...')
	files_repo.remove(name)
	print('Done')

def remove_all_files():
	files_repo = FilesRepo()
	print('Removing...')
	files_repo.remove_all()
	print('Done')

def set_cnn_str_config(cnn):
	config = JsonConfigManager(os.getcwd())
	config.set_connection_string(cnn)

program_input = ProgramInput()
repo.set_config(get_configuration(program_input))

if len(sys.argv) <= 1:
	program_input.print_help()
	sys.exit()

if program_input.has_paths():
	paths = program_input.get_paths()
	save_files(paths, program_input.find_files_recursively())
elif program_input.has_file_name_to_retrieve() and program_input.has_directory_to_retrieve_to():
	file_name = program_input.get_name_of_file_to_retrieve()
	dir = program_input.get_directory_to_retrieve_to()
	retrieve_file(file_name, dir)

	if program_input.remove_file_after_retrieval():
		remove_file(file_name)

elif program_input.need_to_retrieve_names():
	retrieve_names()
elif program_input.has_file_to_delete():
	remove_file(program_input.get_file_to_delete())
elif program_input.remove_all_files():
	remove_all_files()
elif program_input.has_config_connection_string():
	set_cnn_str_config(program_input.get_config_connection_string())



