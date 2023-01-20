# from base.dimensions import Dimensions
# from gui_components.grid import Grid
import os

from math import ceil

from gui_components.screen import Screen
from base.important_variables import *
from base.colors import *
from base.lines import LineSegment, Point
from base.utility_functions import *
# from gui_components.graph import Graph
from gui_components.text_box import TextBox
import matplotlib.pyplot as plot
import statistics

class MainScreen(Screen):
    """The main screen of the application"""

    run_button = TextBox("Run", 18, pleasing_green, white, True)
    current_line = LineSegment(Point(0, 0), Point(0, 0))
    graphs = []

    def __init__(self):
        """Initializes the screen"""

        # self.do_if(SHOULD_WRITE_CLEANED_FILE, self.write_cleaned_file)
        # self.do_if(SHOULD_WRITE_GROUPS_FILE, self.write_groups_file)
        # self.run_button.percentage_set_dimensions(0, 90, 100, 10, screen_length, screen_height)
        # self.do_if(SHOULD_WRITE_STATS_GROUP_FILE, self.write_stats_group_file)

        # self.create_cleaned_files()
        # self.create_group_files()
        self.save_graphs()

    def save_graphs(self):
        angle_file_names = list(filter(lambda item: item.__contains__(".txt"), os.listdir("angle_paths")))
        group_file_paths = [f"group_{angle_file_name[:-4]}.json" for angle_file_name in angle_file_names]
        image_file_paths = [f"{angle_file_name[:-4]}.png" for angle_file_name in angle_file_names]

        for x in range(len(group_file_paths)):
            self.save_graph(image_file_paths[x], group_file_paths[x], 0, len(self.get_group_json_file(group_file_paths[x]).keys()), 1)

            plot.clf()

    def create_cleaned_files(self):
        angle_file_names = list(filter(lambda item: item.__contains__(".txt"), os.listdir("angle_paths")))
        cleaned_file_paths = [f"cleaned_{angle_file_path}" for angle_file_path in angle_file_names]

        for x in range(len(angle_file_names)):
            self.write_cleaned_file(f"angle_paths/{angle_file_names[x]}", cleaned_file_paths[x])

    def create_group_files(self):
        angle_file_names = list(filter(lambda item: item.__contains__(".txt"), os.listdir("angle_paths")))
        cleaned_file_paths = [f"cleaned_{angle_file_path}" for angle_file_path in angle_file_names]
        group_file_paths = [f"group_{angle_file_path[:-4]}.json" for angle_file_path in angle_file_names]

        for x in range(len(cleaned_file_paths)):
            self.write_groups_file(cleaned_file_paths[x], group_file_paths[x])

    def set_up_graphs(self, group_json_file_path=None, graph_start_group=None, graph_end_group=None, step_size=None):
        # self.do_if(SHOULD_WRITE_STATS_GROUP_FILE, self.write_stats_group_file)

        group_json_file_path = group_json_file_path if group_json_file_path is not None else GROUPS_FILE_PATH
        group_json_file = self.get_group_json_file(group_json_file_path)

        file_graph_start_group, file_graph_end_group, file_step_size = self.get_group_file_numbers_from_config_file()
        graph_start_group = graph_start_group if graph_start_group is not None else file_graph_start_group
        graph_end_group = graph_end_group if graph_end_group is not None else file_graph_end_group
        step_size = step_size if step_size is not None else file_step_size


        yaw_values = self.get_gyro_values(graph_start_group, graph_end_group, "Yaw", group_json_file)
        roll_values = self.get_gyro_values(graph_start_group, graph_end_group, "Roll", group_json_file)
        pitch_values = self.get_gyro_values(graph_start_group, graph_end_group, "Pitch", group_json_file)

        figure, axis = plot.subplots(2, 2)
        figure.tight_layout()

        all_gyro_values_graph = axis[1][1]

        all_gyro_values_graph.set_title("All")
        self.show_gyro_base_lines(yaw_values, step_size, "Yaw", axis[0][0], all_gyro_values_graph, "#f8d568")
        self.show_gyro_base_lines(roll_values, step_size, "Roll", axis[0][1], all_gyro_values_graph, "red")
        self.show_gyro_base_lines(pitch_values, step_size, "Pitch", axis[1][0], all_gyro_values_graph, "purple")

    def show_graph(self, group_json_file_path=None):
        self.set_up_graphs(group_json_file_path)
        plot.show()

    def save_graph(self, file_name, group_json_file_path=None, graph_start_group=None, graph_end_group=None, step_size=None):
        self.set_up_graphs(group_json_file_path, graph_start_group, graph_end_group, step_size)
        plot.savefig(file_name)

    def get_gyro_values(self, graph_start_group, graph_end_group, gyro_type_name, json_file):
        return_value = []
        for x in range(graph_start_group, graph_end_group):
            group = json_file.get(str(x + 1))

            return_value.append(group.get(gyro_type_name))

        return return_value

    def show_gyro_base_lines(self, gyro_values, step_size, gyro_value_name, current_gyro_value_graph, all_gryo_values_graph, color):

        y_coordinates = []
        x_coordinates = []

        for x in range(0, len(gyro_values), step_size):
            x_coordinates.append(x)
            y_coordinates.append(gyro_values[x])

        current_gyro_value_graph.plot(x_coordinates, y_coordinates, color=color)
        all_gryo_values_graph.plot(x_coordinates, y_coordinates, color=color)

        current_gyro_value_graph.set_title(gyro_value_name)

    def write_cleaned_file(self, angle_file_path=None, cleaned_file_path=None):

        angle_file_path = angle_file_path if angle_file_path is not None else ANGLES_FILE_PATH
        cleaned_file_path = cleaned_file_path if cleaned_file_path is not None else CLEANED_FILE_PATH

        angle_file = open(angle_file_path, "r")
        angle_file_lines = get_items(angle_file.read(), "\n")
        angle_file.close()

        cleaned_file_lines = get_lines_containing(angle_file_lines, ["Roll", "Yaw", "Pitch"])
        
        cleaned_file = open(cleaned_file_path, "w+")
        cleaned_file.write(get_string(cleaned_file_lines))
        cleaned_file.close()
    
    def write_groups_file(self, cleaned_file_path=None, groups_file_path=None):
        cleaned_file_path = cleaned_file_path if cleaned_file_path is not None else CLEANED_FILE_PATH
        group_file_path = groups_file_path if groups_file_path is not None else GROUPS_FILE_PATH

        cleaned_file = open(cleaned_file_path, "r")
        cleaned_file_lines = get_items(cleaned_file.read(), "\n")
        cleaned_file.close()

        groups_file = open(group_file_path, "w+")
        groups_file_json = {}
        current_group_json = {}
        current_group_number = 1

        for cleaned_file_line in cleaned_file_lines:
            yaw_index = self.get_index(cleaned_file_line, "Yaw: ")
            roll_index = self.get_index(cleaned_file_line, "Roll: ")
            pitch_index = self.get_index(cleaned_file_line, "Pitch: ")

            possible_indexes = [yaw_index, roll_index, pitch_index]
            line_start_names = ["Yaw", "Roll", "Pitch"]

            index = self.get_valid_substring_index(possible_indexes)
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

    def get_group_file_numbers_from_config_file(self):
        """:returns: [graph_start_group, graph_end_group, step_size]; the numbers from the config file that deal with the group_json_file"""

        config_json_file = self.get_config_json_file()
        group_json_file = self.get_group_json_file()

        graph_start_group = config_json_file.get("graphStartGroup")
        graph_end_group = config_json_file.get("graphEndGroup")
        step_size = config_json_file.get("stepSize")

        if graph_start_group == "START":
            graph_start_group = 0

        if graph_end_group == "END":
            graph_end_group = len(group_json_file.keys())

        return [graph_start_group, graph_end_group, step_size]

    def get_group_json_file(self, group_json_file_path=None):
        """:returns: dictionary; the contents of the group json file gotten from json.load(file)"""

        group_json_file_path = group_json_file_path if group_json_file_path is not None else GROUPS_FILE_PATH
        return json.load(open(group_json_file_path))
    def get_config_json_file(self):
        """:returns: dictionary; the contents of the config json file gotten from json.load(file)"""

        return json.load(open("config.json"))

    def get_stats_group_file(self):
        """:returns: dictionary; the contents of the stats group file"""

        return json.load(open(STATS_GROUP_FILE_PATH))
    def write_stats_group_file(self):
        group_json_file = json.load(open(GROUPS_FILE_PATH))
        graph_start_group, graph_end_group, step_size = self.get_group_file_numbers_from_config_file()

        config_file = self.get_config_json_file()
        stats_step_size = config_file.get("statsStepSize")

        yaw_values = self.get_gyro_values(graph_start_group, graph_end_group, "Yaw", group_json_file)
        roll_values = self.get_gyro_values(graph_start_group, graph_end_group, "Roll", group_json_file)
        pitch_values = self.get_gyro_values(graph_start_group, graph_end_group, "Pitch", group_json_file)

        statistics_groups_json = {"statsStepSize": stats_step_size}
        current_group_item = {}
        current_group_number = 1
        graph_group_length = graph_end_group - graph_start_group
        start_index = 0

        for x in range(ceil(graph_group_length / stats_step_size)):
            end_index = start_index + stats_step_size

            if end_index >= graph_group_length:
                end_index = graph_group_length

            # Stats Data Can't be Analyzed if there is less than 2 data points
            if end_index - start_index < 2:
                break

            yaw_vals = yaw_values[start_index: end_index]
            roll_vals = roll_values[start_index: end_index]
            pitch_vals = pitch_values[start_index: end_index]

            yaw_stats = self.get_stats_values(yaw_vals)
            roll_stats = self.get_stats_values(roll_vals)
            pitch_stats = self.get_stats_values(pitch_vals)

            # Adding 1 because groups and indexes are off by one. And adding graph_start_group because the groups
            # May not start at 0. They could start at 100, 50, etc.
            current_group_item["groupNumbers"] = f"{start_index + 1 + graph_start_group} - {end_index + 1 + graph_start_group   }"
            self.set_stats_json_item(yaw_stats, "Yaw", current_group_item)
            self.set_stats_json_item(roll_stats, "Roll", current_group_item)
            self.set_stats_json_item(pitch_stats, "Pitch", current_group_item)

            statistics_groups_json[current_group_number] = current_group_item
            current_group_item = {}
            current_group_number += 1
            start_index += stats_step_size

        json.dump(statistics_groups_json, open(STATS_GROUP_FILE_PATH, "w+"), indent=4)

    def set_stats_json_item(self, stats, gyro_value_name, stats_json_item):
        mean, standard_deviation, median, min__value, max__value, range_value = stats

        stats_json_item[f"{gyro_value_name}-Mean"] = mean
        stats_json_item[f"{gyro_value_name}-Standard-deviation"] = standard_deviation
        stats_json_item[f"{gyro_value_name}-Median"] = median
        stats_json_item[f"{gyro_value_name}-Min"] = min__value
        stats_json_item[f"{gyro_value_name}-Max"] = max__value
        stats_json_item[f"{gyro_value_name}-Range"] = range_value

    def get_index(self, string, substring):
        try:
            return string.index(substring) + len(substring)

        except:
            return -1

    def get_valid_substring_index(self, possible_substring_start_indexes):
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
            self.show_graph()

    def get_stats_values(self, values):
        """:returns: [mean, standard_deviation, median, min, max, range_value] """

        sorted_values = sorted(values)
        mean = statistics.mean(values)
        standard_deviation = statistics.stdev(values, mean)
        median = statistics.median(values)

        min_value = sorted_values[0]
        max_value = sorted_values[1]

        return [mean, standard_deviation, median, min_value, max_value, max_value - min_value]

    def get_components(self):
        return [self.run_button]

