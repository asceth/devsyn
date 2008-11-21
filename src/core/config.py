__all__ = ["Config"]

import __builtin__

from pandac.PandaModules import Filename
from ConfigParser import SafeConfigParser

APP_PATH = __builtin__.APP_PATH

class Config(SafeConfigParser):
  def parse_into_object(self, object):
    """Parses the configuration file and sets the properties of the specified
       object.  Most likely this will be __builtin__."""
    object.FULLSCREEN = self.getboolean("display", "fullscreen")
    object.LOAD_DISPLAY = self.get("display", "framework").replace(" ", "").lower().replace("directx", "dx").replace("opengl", "gl")
    res = self.get("display", "resolution")

    if(object.RESOLUTION is None or object.RESOLUTION.strip().lower() in ["", "auto", "none", "keep", "current", "detect", "autodetect", "auto-detect"]):
      object.RESOLUTION = None
    else:
      object.RESOLUTION = (int(self.get("display", "resolution").strip().lower().split("x")[0]),int(self.get("display", "resolution").strip().lower().split("x")[1]))
      object.WIN_SIZE = (int(self.get("display", "windowSize").strip().lower().split("x")[0]),int(self.get("display", "windowSize").strip().lower().split("x")[1]))

    object.SHOW_FPS = self.getboolean("performance", "showFpsMeter")
    object.USE_CACHE = self.getboolean("performance", "useTextureCache")
    object.INTERPOLATE_FRAMES = self.getboolean("performance", "interpolateFrames")

  def load(self, file_name = None):
    if(file_name == None):
      self.readfp(open(self.make_filename().toOsSpecific()))
    elif(isinstance(file_name, Filename)):
      self.readfp(open(file_name.toOsSpecific()))
    else:
      raise TypeError, "Invalid type for Config.load()!"

  @classmethod
  def make_filename(self):
    """Returns the filename that config files have on this platform."""
    return Filename(APP_PATH + "config.conf")
