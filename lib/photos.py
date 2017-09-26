# from requests.exceptions import ConnectionError # In case internet goes down :)
import requests
import os


def download_all_albums(vk, dir_path="VK Photos"):
	os.makedirs(dir_path, exists_ok=True)
	albums = vk("photos.getAlbums", need_system=1)['items']
	for album in albums:
		album_name = album['title'].replace('/', '//') # Dumb names
		album_path = os.path.join(dir_path, album_name)
		os.makedirs(album_path, exists_ok=True)
		download_album(vk, album['id'], album_path)


def download_album(vk, album_id, album_path):
	photos = vk("photos.get", album_id=album_id)['items']
	for num, photo in enumerate(photos, start=1):
		file_name = f"{num}.jpg"
		file_path = os.path.join(album_path, file_name)
		url = get_photo_url(photo)
		download_file(url, file_path)


def download_file(url, save_path, overwrite=False):
	# We do not want to stream a file because if we restart downloading
	# the whole folder, this file will be left not fully downloaded
	if not (os.path.exists(save_path) and not overwrite):
		content = requests.get(url, stream=False)
		with open(save_path, "wb") as f:
			f.write(content)


def get_photo_url(photo):
	photo_sizes = (
		"photo_2560", "photo_1280", "photo_807",
		"photo_604", "photo_130", "photo_75"
	)
	for size in photo_sizes:
		if size in photo:
			return photo[size]
	else:
		raise ValueError("Photo size was not found")
