from copy import deepcopy

from base.important_variables import screen_length, screen_height
from base.lines import LineSegment, Point
from gui_components.component import Component
from base.colors import black


class Graph(Component):
    """A component that displays a graph using x and y axis; only deals with positive numbers (at least for now)"""

    unmodified_lines = []
    color = ""
    modified_lines = []
    x_axis = None
    y_axis = None

    def __init__(self, lines, color, is_relative=False):
        """Initializes the object"""

        self.unmodified_lines = lines
        self.color = color

        for x in range(len(self.unmodified_lines)):
            self.unmodified_lines[x].set_color(color)

    def run(self):
        pass

    def render(self):
        """Renders the object on the screen"""

        x_axis = LineSegment(Point(self.left_edge, self.bottom_edge), Point(self.right_edge, self.bottom_edge))
        y_axis = LineSegment(Point(self.left_edge, self.top_edge), Point(self.left_edge, self.bottom_edge))

        x_axis.color, y_axis.color = black, black

        components = self.modified_lines

        for x in range(len(self.modified_lines)):
            self.modified_lines[x].set_color(self.color)

        for component in components:
            component.render()

    def scale_lines(self):
        """Makes the lines fit onto the graph"""

        all_points = []
        self.modified_lines = deepcopy(self.unmodified_lines)

        for line in self.modified_lines:
            all_points.append(line.start_point)
            all_points.append(line.end_point)

        self.scale_points(all_points)

    def get_x_delta(self, points):
        """returns: double; the max x coordinate of this graph"""

        return self.get_x_max(points) - self.get_x_min(points)

    def get_sorted_x_values(self, points):
        all_x_values = [point.x_coordinate for point in points]
        return sorted(all_x_values)

    def get_x_min(self, points):
        return self.get_sorted_x_values(points)[0]

    def get_x_max(self, points):
        return self.get_sorted_x_values(points)[len(points) - 1]

    def get_sorted_y_values(self, points):
        all_y_values = [point.y_coordinate for point in points]
        return sorted(all_y_values)

    def get_y_min(self, points):
        return self.get_sorted_y_values(points)[0]

    def get_y_max(self, points):
        return self.get_sorted_y_values(points)[len(points) - 1]

    def get_y_delta(self, points):
        """returns: double; the max y coordinate of this graph"""

        return self.get_y_max(points) - self.get_y_min(points)

    def scale_points(self, points):
        """Scales the points so that the fit on the graph and of all of equal 'units'"""

        x_unit = self.length / (self.get_x_delta(points) + pow(10, -9))
        y_unit = self.height / (self.get_y_delta(points) + pow(10, -9))

        print(self.get_x_delta(points), self.get_y_delta(points))
        print(self.get_y_min(points), self.get_y_max(points))

        total_graph_height = self.get_y_max(points) if self.get_y_max(points) > 0 else 0

        if self.get_y_min(points) < 0:
            total_graph_height += self.get_y_min(points) * -1

        # y_unit = self.height / total_graph_height
        x_min = self.get_x_min(points)
        y_min = self.get_y_min(points)

        for point in points:
            x_delta = point.x_coordinate - x_min
            y_delta = point.y_coordinate - y_min
            # y_delta = -1 * point.y_coordinate if point.y_coordinate < 0 else point.y_coordinate

            point.x_coordinate = self.left_edge + (x_unit * x_delta)
            point.y_coordinate = self.bottom_edge - (y_unit * y_delta)

    def number_set_dimensions(self, x_coordinate, y_coordinate, length, height):
        super().number_set_dimensions(x_coordinate, y_coordinate, length, height)
        self.scale_lines()

    def percentage_set_dimensions(self, percent_right, percent_down, percent_length, percent_height):
        super().percentage_set_dimensions(percent_right, percent_down, percent_length, percent_height, screen_length, screen_height)
        self.scale_lines()
