# from base.dimensions import Dimensions
# from gui_components.grid import Grid
# from gui_components.screen import Screen
from base.important_variables import *
from base.colors import *
from base.lines import LineSegment, Point
from base.utility_functions import *
# from gui_components.graph import Graph
# from gui_components.text_box import TextBox
import matplotlib.pyplot as plot

class MainScreen:
    """The main screen of the application"""

    # run_button = TextBox("Run", 18, pleasing_green, white, True)
    current_line = LineSegment(Point(0, 0), Point(0, 0))
    graphs = []

    def __init__(self):
        """Initializes the screen"""

        lines = [
            LineSegment(Point(0, 0), Point(1, 5)),
            LineSegment(Point(1, 5), Point(2, 8)),
            LineSegment(Point(2, 8), Point(3, 0)),
            LineSegment(Point(3, 0), Point(4, 2))
        ]
        # self.graph = Graph(lines, blue, False)
        # self.graph.percentage_set_dimensions(0, 0, 100, 90)

        self.do_if(SHOULD_WRITE_CLEANED_FILE, self.write_cleaned_file)
        self.do_if(SHOULD_WRITE_GROUPS_FILE, self.write_groups_file)
        self.set_up_graphs()
        # self.run_button.percentage_set_dimensions(0, 90, 100, 10, screen_length, screen_height)



    def set_up_graphs(self):
        config_json_file = json.load(open("config.json"))
        group_json_file = json.load(open(GROUPS_FILE_PATH))

        graph_start_group = config_json_file.get("graphStartGroup")
        graph_end_group = config_json_file.get("graphEndGroup")
        step_size = config_json_file.get("stepSize")

        if graph_start_group == "START":
            graph_start_group = 0

        if graph_end_group == "END":
            graph_end_group = len(group_json_file.keys())

        # grid = Grid(Dimensions(0, 0, screen_length, screen_height * .9), 3, None)

        yaw_values = self.get_gyro_values(graph_start_group, graph_end_group, "Yaw", group_json_file)
        roll_values = self.get_gyro_values(graph_start_group, graph_end_group, "Roll", group_json_file)
        pitch_values = self.get_gyro_values(graph_start_group, graph_end_group, "Pitch", group_json_file)

        # yaw_graph = Graph(self.get_gyro_base_lines(yaw_values, step_size), blue)
        # roll_graph = Graph(self.get_gyro_base_lines(roll_values, step_size), pleasing_green)
        # pitch_graph = Graph(self.get_gyro_base_lines(pitch_values, step_size), purple)

        figure, axis = plot.subplots(2, 2)
        axis[1][1].set_title("All")
        self.show_gyro_base_lines(yaw_values, step_size, blue, "Yaw", axis[0][0], axis[1][1])
        self.show_gyro_base_lines(roll_values, step_size, pleasing_green, "Roll", axis[0][1], axis[1][1])
        self.show_gyro_base_lines(pitch_values, step_size, purple, "Pitch", axis[1][0], axis[1][1])
        plot.show()


    def get_gyro_values(self, graph_start_group, graph_end_group, gyro_type_name, json_file):
        return_value = []
        for x in range(graph_start_group, graph_end_group):
            group = json_file.get(str(x + 1))

            return_value.append(group.get(gyro_type_name))

        return return_value

    def show_gyro_base_lines(self, gyro_values, step_size, color, gyro_value_name, axis, figure2):

        y_coordinates = []
        x_coordinates = []

        for x in range(0, len(gyro_values), step_size):
            x_coordinates.append(x)
            y_coordinates.append(gyro_values[x])

        axis.plot(x_coordinates, y_coordinates)
        figure2.plot(x_coordinates, y_coordinates)

        axis.set_title(gyro_value_name)

    def write_cleaned_file(self):
        angle_file = open(ANGLES_FILE_PATH, "r")
        angle_file_lines = get_items(angle_file.read(), "\n")
        angle_file.close()

        cleaned_file_lines = get_lines_containing(angle_file_lines, ["Roll", "Yaw", "Pitch"])
        
        cleaned_file = open(CLEANED_FILE_PATH, "w+")
        cleaned_file.write(get_string(cleaned_file_lines))
        cleaned_file.close()
    
    def write_groups_file(self):
        cleaned_file = open(CLEANED_FILE_PATH, "r")
        cleaned_file_lines = get_items(cleaned_file.read(), "\n")
        cleaned_file.close()

        groups_file = open(GROUPS_FILE_PATH, "w+")
        groups_file_json = {}
        current_group_json = {}
        current_group_number = 1

        for cleaned_file_line in cleaned_file_lines:
            yaw_index = self.get_index(cleaned_file_line, "Yaw: ")
            roll_index = self.get_index(cleaned_file_line, "Roll: ")
            pitch_index = self.get_index(cleaned_file_line, "Pitch: ")

            possible_indexes = [yaw_index, roll_index, pitch_index]
            line_start_names = ["Yaw", "Roll", "Pitch"]

            index = self.get_valid_substring(possible_indexes)
            line_start_name = line_start_names[index]
            number_start_index = possible_indexes[index]
            number = float(cleaned_file_line[number_start_index:])

            current_group_json[line_start_name] = number

            # The group has come to an end, so we should add it to the main json file
            if line_start_name == END_STRING_GROUP:
                groups_file_json[current_group_number] = current_group_json
                current_group_json = {}
                current_group_number += 1

        json.dump(groups_file_json, groups_file, indent=4)
    def get_index(self, string, substring):
        try:
            return string.index(substring) + len(substring)

        except:
            return -1

    def get_valid_substring(self, possible_substring_start_indexes):
        return_value = 0
        for x in range(len(possible_substring_start_indexes)):
            possible_substring_start_index = possible_substring_start_indexes[x]

            if possible_substring_start_index != -1:
                return_value = x

        return return_value

    def do_if(self, condition, function):
        if condition:
            function()

    def run(self):
        if self.run_button.got_clicked():
            self.change_current_line()

    def change_current_line(self):
        config_json_file = json.load(open("config.json"))
        group_line_index = config_json_file.get("groupLineIndex")

        group_json_file = json.load(open(GROUPS_FILE_PATH))

        graph_start_group = config_json_file.get("graphStartGroup")
        graph_end_group = config_json_file.get("graphEndGroup")

        if graph_start_group == "START":
            graph_start_group = 0

        if graph_end_group == "END":
            graph_end_group = len(group_json_file.keys())

        total_number_of_groups = graph_end_group - graph_start_group
        conversion_factor = screen_length / total_number_of_groups
        line_left_edge = conversion_factor * group_line_index

        self.current_line = LineSegment(Point(line_left_edge, 0), Point(line_left_edge, screen_height))

    def get_components(self):
        # return [self.graph]
        return self.graphs + [self.current_line, self.run_button]
