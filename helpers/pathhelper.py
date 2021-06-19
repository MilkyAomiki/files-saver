from pathlib import Path
from typing import List
import os


def calc_dir_size(dir, recursive=True):
	dir = Path(dir)
	pattern = '**/*' if recursive else '*'
	return sum(f.stat().st_size for f in dir.glob(pattern) if f.is_file())


def calc_paths_size(paths: List, recursively=False):
	size = 0

	for path in paths:
		path = os.path.abspath(path)
		if os.path.isfile(path):
			size += os.path.getsize(path)
		elif os.path.isdir(path):
			size += calc_dir_size(path, recursively)
		else:
			raise IOError(f'Given path is invalid: {path}')

	return size
