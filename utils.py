from os.path import join, dirname

def site_path(path):
	return join(dirname(__file__), path)
