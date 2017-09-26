from logging import getLogger
logger = getLogger("vk_tools.clean")


def groups(vk):
	groups = vk("groups.get", count=1000)['items']
	for group in groups:
		vk("groups.leave", group_id=group)
		logger.debug(f"You left {group}")


def photos(vk):
	albums = vk("photos.getAlbums", need_system=1)['items']
	regular_albums = []
	system_albums = []
	for album in albums:
		if album['id'] > 0:
			regular_albums.append(album['id'])
		else:
			system_albums.append(album['id'])

	while regular_albums:
		for album in regular_albums:
			vk("photos.deleteAlbum", album_id=album)
			regular_albums.remove(album)
			logger.debug(f"Album {album} deleted.")

	while system_albums:
		for album in system_albums:
			photos = vk("photos.get", album_id=album)['items']
			for photo in photos:
				vk("photos.delete", photo_id=photo['id'])
				logger.debug(f"Photo {photo['id']} deleted.")
			system_albums.remove(album)


def videos(vk):
	user_id = vk("users.get")[0]['id']
	request = vk("video.get", count=200)
	videos = request['items']
	for video in videos:
		try:
			vk("video.delete", video_id=video['id'], target_id=user_id)
			logger.debug(f"Видео '{video['title']}' удалено.")
		except:
			logger.debug(f"Видео '{video['title']}' не удалено.")


def wall(vk):
	count = vk("wall.get")['count']
	while count:
		wall = vk("wall.get", сount=100)
		count = wall['count']
		for post in wall['items']:
			vk("wall.delete", post_id=post['id'])
			logger.debug(f"Post {post['id']} deleted.")


def messages(vk):
	count = vk("messages.getDialogs")['count']
	while count:
		request = vk("messages.getDialogs")
		count = request['count']
		for dialog in request['items']:
			if 'chat_id' in dialog['message']:
				peer_id = dialog['message']['chat_id'] + 2000000000
			elif 'user_id' in dialog['message']:
				peer_id = dialog['message']['user_id']
			vk("messages.deleteDialog", peer_id=peer_id)
			logger.debug(f"Dialog with {peer_id} was deleted.")
