from lib import utils, photos, clean, vk

import argparse

logger = utils.make_logger("Data/debug.log")


CLEAN_TARGETS = {
	"wall":clean.wall,
	"groups":clean.groups,
	"photos":clean.photos,
	"videos":clean.videos,
	"messages":clean.messages,
}


def main(vk_session, *args):
	parser = make_main_parser()
	args = parser.parse_args(*args)
	evaluate_args(vk_session, args)


def evaluate_args(vk_session, args):
	if args.prog == "clean":
		for target in args.targets:
			CLEAN_TARGETS[target](vk_session)


def make_main_parser():
	parser = argparse.ArgumentParser("VK Toolbox")
	subparser_creator = parser.add_subparsers(dest="prog")
	make_clean_parser(subparser_creator)
	return parser


def make_clean_parser(creator):
	parser = creator.add_parser("clean",
		help="Clean parts of VK profile according to vk_session provided")
	parser.add_argument("targets", nargs="+", choices=CLEAN_TARGETS.keys())
	


if __name__ == "__main__":
	main(vk.Vk("Data/token.txt", v="5.61"))
