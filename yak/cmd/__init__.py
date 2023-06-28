import argparse

# from yak.machine import ConsoleYakMachine, GraphicYakMachine, YakMachine
# from yak.util import set_up_yakdir


# def yak():
#     args = _parse_args()
#     return (
#         _make_yak(args.cli, args.port, args.debug)
#         .with_image(args.image)
#         .with_script(args.script)
#         .boot()
#     )

# def _parse_args() -> argparse.Namespace:
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-c', '--cli', action='store_true', help='run console only version of yak')
#     parser.add_argument('-s', '--script', type=str, help='path to the yak script to run')
#     parser.add_argument('-i', '--image', type=str, help='path to the yak image to load and run')
#     parser.add_argument('-p', '--port', type=int, default=4400, help='the port to run the YakInServer')
#     parser.add_argument('-d', '--debug', action='store_true', help='emit debug logs')
#     return parser.parse_args()


# def _make_yak(cli: bool, port: int, debug: bool) -> YakMachine:
#     if cli:
#         return ConsoleYakMachine(port, debug)
#     return GraphicYakMachine(port, debug)
