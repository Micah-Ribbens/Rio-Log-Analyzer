from base.keyboard import Keyboard
from gui_components.window import Window
from pygame_library.keys import *
import json

screen_length = 2200
screen_height = 1200
background_color = (200, 200, 200)

keyboard = Keyboard()
# game_window = Window(screen_length, screen_height, background_color, "Game Basics")


json_file = json.load(open("config.json"))
SHOULD_WRITE_CLEANED_FILE = json_file.get("writeCleanedFile")
CLEANED_FILE_PATH = json_file.get("cleanedFilePath")
ANGLES_FILE_PATH = json_file.get("anglesFilePath")
GRAPH_GROUP_START = json_file.get("graphGroupStart")
GRAPH_GROUP_END = json_file.get("graphGroupEnd")
SHOULD_WRITE_GROUPS_FILE = json_file.get("writeGroupsFile")
GROUPS_FILE_PATH = json_file.get("groupsFilePath")
NUMBER_IN_GROUP = json_file.get("numberInGroup")
END_STRING_GROUP = "Pitch"