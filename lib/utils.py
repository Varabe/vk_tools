import logging
import sys


def make_logger(file_name):
	logger = logging.getLogger('vk_tools')
	logger.setLevel("DEBUG")
	fh = logging.FileHandler(file_name, mode="a")
	sh = logging.StreamHandler(stream=sys.stdout)
	fh_formatter = logging.Formatter('[%(asctime)s] %(name)s: %(message)s')
	sh_formatter = logging.Formatter('%(name)s: %(message)s')
	fh.setFormatter(fh_formatter)
	sh.setFormatter(sh_formatter)
	logger.addHandler(fh)
	logger.addHandler(sh)
	return logger


def get_token():
	""" Создает токен для заданного приложения """
	import webbrowser as wb
	client_id = 5747467
	scope = 2047391
	url = f"https://oauth.vk.com/authorize?client_id={client_id}&display=page&redirect_uri=http://vk.com&response_type=token&v=5.60&scope={scope}"
	wb.open(url, new=2)
