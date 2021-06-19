from io import FileIO
import os


def write_from_file_to_file(source_file: FileIO, destination_path):
	path = os.path.join(destination_path)
	fs_file = open(path, 'wb+')
	fs_file.write(source_file.read())
	fs_file.close()
	source_file.close()


def convert_bytes(bytes):

	i = 1
	while bytes >= 1024 and i < 5:
		bytes /= 1024
		i += 1

	labels = {
		1: 'B',
		2: 'KB',
		3: 'MB',
		4: 'GB'
	}

	return bytes, labels[i]
