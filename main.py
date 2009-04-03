#!/usr/bin/env python
__all__ = []

import sys
import os
import __builtin__
from optparse import OptionParser, OptionGroup, OptionValueError

from pandac.PandaModules import Filename
from pandac.PandaModules import loadPrcFileData

__builtin__.WINDOW_TITLE = "DevSyn Games"
__builtin__.GAME = "rpg"
__builtin__.FULLSCREEN = False
__builtin__.SHOW_FPS = True # FPS meter in the top right corner of the screen
__builtin__.DEBUG_MODE = False # offers gadgets useful for debugging
__builtin__.ENABLE_DIRECTTOOLS = False # for heavy debugging
__builtin__.ENABLE_PSTATS = False # whether to enable performance statistics or not
__builtin__.INTERPOLATE_FRAMES = True # smooth frame interpolation for low framerates
__builtin__.LOAD_DISPLAY = "gl" # either gl or dx9 or dx8
__builtin__.RESOLUTION = None # either a two-tuple or None, which means auto
__builtin__.WIN_SIZE = (1024, 768) # the window size, when running windowed
__builtin__.APP_PATH = Filename.fromOsSpecific(os.path.abspath(os.path.join(sys.path[0]))).getFullpath() + "/"

from devsyn.core import Config

__builtin__.CONFIG = Config()
__builtin__.CONFIG.load(__builtin__.CONFIG.make_filename())
__builtin__.CONFIG.parse_into_object(__builtin__)

# parse command line options
def validate_resolution_size(option, opt_str, value, parser):
  dmode = value.lower().split("x")
  try:
    if(len(dmode) != 2):
      raise
    dmode = (int(dmode[0]), int(dmode[1]))
    assert dmode[0] >= 0 and dmode[1] >= 0
  except:
    raise OptionValueError("Invalid display mode! Must be in the form of -s WxH or --size=WxH.")
  setattr(parser.values, option.dest, tuple(dmode))


parser = OptionParser("usage: main.py [options]", version="DevSyn Prototypes")
parser.add_option("-g", "--game", action="store", dest="game",
                  default=__builtin__.GAME,
                  help="run the specified game")
parser.add_option("-f", "--fullscreen", action="store_true",
                  dest="fullscreen", default=__builtin__.FULLSCREEN,
                  help="run devsyn as fullscreen")
parser.add_option("-w", "--windowed", action="store_false",
                  dest="fullscreen", help="run devsyn in windowed mode")
parser.add_option("-r", "--res", action="callback",
                  callback=validate_resolution_size, type=str,
                  nargs=1, dest="size", default="",
                  help="use the specified resolution or window size")
parser.add_option("--use-cache", action="store_true", dest="cache",
                  default=__builtin__.USE_CACHE,
                  help="make use of texture caching")
parser.add_option("--no-cache", action="store_false", dest="cache",
                  help="don't use the texture cache")
group = OptionGroup(parser, "Debug Options",
                    "These are options useful for debugging purposes.")
group.add_option("-p", "--pstats", action="store_true", dest="pstats",
                 default=__builtin__.ENABLE_PSTATS,
                 help="try to connect to the performance analysis tool")
group.add_option("-d", "--debug", action="store_true", dest="debug",
                 default=__builtin__.DEBUG_MODE,
                 help="run devsyn in debug mode")
group.add_option("-a", "--analyze", action="store_true", dest="analyze",
                 default=__builtin__.ENABLE_DIRECTTOOLS,
                 help="show the analyzer window")
parser.add_option_group(group)

args = parser.parse_args()[0]
DEBUG_MODE = args.debug
ENABLE_DIRECTTOOLS = args.analyze
ENABLE_PSTATS = args.pstats
FULLSCREEN = args.fullscreen
USE_CACHE = args.cache
RESOLUTION = args.size
WIN_SIZE = args.size
GAME = args.game
LOAD_DISPLAY = __builtin__.LOAD_DISPLAY
WINDOW_TITLE = __builtin__.WINDOW_TITLE
INTERPOLATE_FRAMES = __builtin__.INTERPOLATE_FRAMES
SHOW_FPS = __builtin__.SHOW_FPS

# put everything under a "try" now, to catch errors
cfg_string = ""
if(DEBUG_MODE): cfg_string += "notify-level-glgsg debug\n"
cfg_string += "basic-shaders-only 1\n"
cfg_string += "sync-video 0\n"
cfg_string += "win-origin 0 0\n"
if(LOAD_DISPLAY.startswith("panda")):
  cfg_string += "load-display %s\n" % LOAD_DISPLAY
else:
  cfg_string += "load-display panda%s\n" % LOAD_DISPLAY
# cfg_string += "prefer-parasite-buffer 0\n"
cfg_string += "want-directtools %d\n" % ENABLE_DIRECTTOOLS
cfg_string += "want-pstats %d\n" % ENABLE_PSTATS
cfg_string += "task-timer-verbose %d\n" % ENABLE_PSTATS
cfg_string += "pstats-tasks %d\n" % ENABLE_PSTATS
cfg_string += "window-title %s\n" % WINDOW_TITLE
cfg_string += "interpolate-frames %d\n" % INTERPOLATE_FRAMES
cfg_string += "show-frame-rate-meter %d\n" % SHOW_FPS
cfg_string += "fullscreen %d\nundecorated %d\n" % (FULLSCREEN, FULLSCREEN)
loadPrcFileData("", cfg_string)

import direct.directbase.DirectStart

# Load the game
exec "from games." + args.game + " import Game"

game = Game()
__builtin__.base.taskMgr.run()

