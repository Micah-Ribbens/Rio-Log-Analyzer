import pygame

from base.colors import pleasing_green
# from base.important_variables import game_window
from pygame_library import library_abstraction


class Point:
    x_coordinate = 0
    y_coordinate = 0

    def __init__(self, x_coordinate, y_coordinate):
        self.x_coordinate, self.y_coordinate = x_coordinate, y_coordinate


class LineSegment:
    start_point = None
    end_point = None
    slope = None
    y_intercept = None
    color = pleasing_green
    is_runnable = False

    def __init__(self, start_point, end_point):
        self.start_point, self.end_point = start_point, end_point

        self.update_line_values()

    def set_color(self, color):
        self.color = color

    def update_line_values(self):
        """Updates the line so it reflects the values in the points"""

        start_point, end_point = self.start_point, self.end_point

        if start_point.x_coordinate == end_point.x_coordinate:
            end_point.x_coordinate += pow(10, -9)

        self.slope = (end_point.y_coordinate - start_point.y_coordinate) / (end_point.x_coordinate - start_point.x_coordinate)
        self.y_intercept = start_point.y_coordinate - self.slope * start_point.x_coordinate

    def get_y_coordinate(self, x_coordinate):
        return x_coordinate * self.slope + self.y_intercept

    def get_x_coordinate(self, y_coordinate):
        return (y_coordinate - self.y_intercept) / self.slope

    def contains_x_coordinate(self, x_coordinate):
        smaller_x_coordinate = self.start_point.x_coordinate if self.start_point.x_coordinate < self.end_point.x_coordinate else self.end_point.x_coordinate
        bigger_x_coordinate = self.start_point.x_coordinate if self.start_point.x_coordinate > self.end_point.x_coordinate else self.end_point.x_coordinate

        return x_coordinate >= smaller_x_coordinate and x_coordinate <= bigger_x_coordinate

    def contains_y_coordinate(self, y_coordinate):
        smaller_y_coordinate = self.start_point.y_coordinate if self.start_point.y_coordinate < self.end_point.y_coordinate else self.end_point.y_coordinate
        bigger_y_coordinate = self.start_point.y_coordinate if self.start_point.y_coordinate > self.end_point.y_coordinate else self.end_point.y_coordinate

        return y_coordinate >= smaller_y_coordinate and y_coordinate <= bigger_y_coordinate

    def contains_point(self, point):
        contains_coordinates = self.contains_x_coordinate(point.x_coordinate) and self.contains_y_coordinate(point.y_coordinate)
        correct_y_coordinate = point.y_coordinate == self.get_y_coordinate(point.x_coordinate)

        return contains_coordinates and correct_y_coordinate

    def slope_is_positive(self):
        """returns: boolean; if the slope is >= 0"""

        return self.slope >= 0

    def render(self):
        """Renders the object"""

        line_height = 10
        pygame.draw.line(library_abstraction.window, self.color,
                         (int(self.start_point.x_coordinate), int(self.start_point.y_coordinate) - line_height),
                         (int(self.end_point.x_coordinate), int(self.end_point.y_coordinate) - line_height),
                         line_height)



