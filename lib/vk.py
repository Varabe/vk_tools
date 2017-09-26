from requests.exceptions import SSLError
import requests
import time
import os


class Vk:
	def __init__(self, token, sleep_time=0.5, is_offline=False, **config):
		config['access_token'] = get_token(token)
		self.sleep_time = sleep_time
		self.is_offline = is_offline
		self.config = config
		if is_offline:
			# Dummy method for testing
			self.send_request = lambda *a, **k: {"items":[], "count":0}

	def __call__(self, method, **kwargs):
		kwargs.update(self.config)
		url = f"https://api.vk.com/method/{method}"
		time.sleep(self.sleep_time)
		return self.send_request(method, **kwargs)

	def send_request(self, method, **kwargs):
		try:
			response = requests.post(method, kwargs)
		except SSLError as e:
			raise NO_INTERNET from e
		else:
			return get_response_dict(response)


def get_token(token):
	token = str(token) # To prevent os.path.exists errors
	if os.path.exists(token):
		with open(token) as f:
			return f.read().strip()
	else:
		return token.strip()


def get_response_dict(response):
	json_dict = response.json()
	if "response" in json_dict:
		return json_dict['response']
	elif "error" in json_dict:
		raise ResponseError(json_dict['error'])
	else:
		return json_dict


class LongpollServer:
	def __init__(self, vk_session, version=2, wait_time=30):
		self.vk = vk_session
		self.version = version
		self.wait_time = wait_time
		self.server, self.key, self.ts = self.get_server_info()
		self.kwargs = self.make_config()
		self.url = "https://" + self.server

	def __call__(self):
		return self.send_longpoll_request()

	def get_server_info(self):
		response = self.vk("messages.getLongPollServer")
		return response['server'], response['key'], response['ts']

	def make_config(self):
		return {"act":"a_check", "key":self.key, "ts":self.ts,
				"wait":self.wait_time, "version":self.version}

	def send_longpoll_request(self):
		response = requests.post(self.url, self.kwargs)
		response = get_response_dict(response)
		self.kwargs['ts'] = response['ts']
		return response


class VkError(Exception):
	pass


class ResponseError(VkError):
	def __init__(self, error):
		params = self.extract_request_params(error)
		message = "{}\nParameters: {}".format(error['error_msg'], params)
		super().__init__(message)
	
	@staticmethod
	def extract_request_params(error):
		return {p['key']:p['value'] for p in error['request_params']}



NO_INTERNET = VkError("No internet connection")
