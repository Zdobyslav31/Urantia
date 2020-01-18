import pygame

from src.assets import assets
from src.utils import rotate_vector


class Device:
    def __init__(self, values_range, coordinates, initial_value):
        # Set border values
        self.min_value = values_range[0]
        self.max_value = values_range[1]

        # Initialize value
        self.value = initial_value

        # Save background position
        self.coordinates = coordinates

    def update(self, value):
        if value > self.max_value:
            self.value = self.max_value
        elif value < self.min_value:
            self.value = self.min_value
        else:
            self.value = value

    @property
    def position(self):
        return self.coordinates

    @property
    def image(self):
        raise NotImplementedError


class LevelIndicator(Device):
    HAND_X_LAMBDA = 25
    HAND_MAX_Y_LAMBDA = 25
    HAND_MIN_Y_LAMBDA = 769

    def __init__(self, values_range, coordinates, initial_value):
        super().__init__(values_range, coordinates, initial_value)
        
        # Load images
        self.bg_image = assets.load_image('indicator_background')
        self.hand_image = assets.load_image('indicator_hand')

    def hand_y_pos(self):
        """Return y coordinate of the hand, calculated from its value"""
        if self.value == self.min_value:
            return self.HAND_MIN_Y_LAMBDA
        if self.value == self.max_value:
            return self.HAND_MAX_Y_LAMBDA

        # The below calculation bases on proportion
        full_y_range = self.HAND_MAX_Y_LAMBDA - self.HAND_MIN_Y_LAMBDA
        full_value_range = self.max_value - self.min_value
        current_value_lambda = self.value - self.min_value

        # current_value_lambda / full_value_range = current_y_lambda / full_y_range
        return (full_y_range * current_value_lambda / full_value_range) + self.HAND_MIN_Y_LAMBDA

    def hand_position(self):
        """Returns a tuple of (x, y) coordinates of the hand"""
        return self.HAND_X_LAMBDA, self.hand_y_pos()

    @property
    def image(self):
        image = self.bg_image.copy()
        image.blit(self.hand_image, self.hand_position())
        return image


class HorizontalSnapIndicator(Device):
    HAND_Y_LAMBDA = 25
    HAND_MAX_X_LAMBDA = 769
    HAND_MIN_X_LAMBDA = 27

    def __init__(self, values_range, coordinates, initial_value):
        super().__init__(values_range, coordinates, initial_value)

        # Load images
        self.bg_image = assets.load_image('horizontal_background')
        self.hand_image = assets.load_image('horizontal_hand')

    def hand_x_pos(self):
        """Return y coordinate of the hand, calculated from its value"""
        if self.value == self.min_value:
            return self.HAND_MIN_X_LAMBDA
        if self.value == self.max_value:
            return self.HAND_MAX_X_LAMBDA

        # The below calculation bases on proportion
        full_y_range = self.HAND_MAX_X_LAMBDA - self.HAND_MIN_X_LAMBDA
        full_value_range = self.max_value - self.min_value
        current_value_lambda = self.value - self.min_value

        # current_value_lambda / full_value_range = current_y_lambda / full_y_range
        return (full_y_range * current_value_lambda / full_value_range) + self.HAND_MIN_X_LAMBDA

    def hand_position(self):
        """Returns a tuple of (x, y) coordinates of the hand"""
        return self.hand_x_pos(), self.HAND_Y_LAMBDA

    @property
    def image(self):
        image = self.bg_image.copy()
        image.blit(self.hand_image, self.hand_position())
        return image


class TurnIndicator(LevelIndicator):
    HAND_X_LAMBDA = 19
    HAND_MAX_Y_LAMBDA = 21
    HAND_MIN_Y_LAMBDA = 322

    def __init__(self, values_range, coordinates, initial_value):
        super().__init__(values_range, coordinates, initial_value)

        # Load images
        self.bg_image = assets.load_image('turn_background')
        self.hand_image = assets.load_image('turn_hand')


class Gauge(Device):
    HAND_MAX_ANGLE = -120
    HAND_MIN_ANGLE = 120
    CENTRAL_POINT_X = 205
    CENTRAL_POINT_Y = 205
    PIVOT_VECTOR = 0, -79

    def __init__(self, values_range, coordinates, initial_value):
        super().__init__(values_range, coordinates, initial_value)

        # Load images
        self.bg_image = assets.load_image('gauge_background')
        self.hand_image = assets.load_image('gauge_hand')

    def hand_angle(self):
        """Return rotation angle of the hand, calculated from its value"""
        if self.value == self.min_value:
            return self.HAND_MIN_ANGLE
        if self.value == self.max_value:
            return self.HAND_MAX_ANGLE

        # The below calculation bases on proportion
        full_angle_range = self.HAND_MAX_ANGLE - self.HAND_MIN_ANGLE
        full_value_range = self.max_value - self.min_value
        current_value_lambda = self.value - self.min_value

        # current_value_lambda / full_value_range = current_angle_lambda / full_angle_range
        return (full_angle_range * current_value_lambda / full_value_range) + self.HAND_MIN_ANGLE

    def hand_image_rotated(self):
        angle = self.hand_angle()
        rotated_img = pygame.transform.rotate(self.hand_image, angle)
        rotated_rect_dimensions = rotated_img.get_rect().size
        central_point = rotated_rect_dimensions[0]/2, rotated_rect_dimensions[1]/2
        rotated_vector = rotate_vector(self.PIVOT_VECTOR, angle)
        coordinates = (
            self.CENTRAL_POINT_X - central_point[0] + rotated_vector[0],
            self.CENTRAL_POINT_Y - central_point[1] + rotated_vector[1]
        )
        return rotated_img, coordinates

    @property
    def image(self):
        image = self.bg_image.copy()
        hand_image_rotated, hand_image_coordinates = self.hand_image_rotated()
        image.blit(hand_image_rotated, hand_image_coordinates)
        return image


class Compass(Device):
    SHIELD_MAX_ANGLE = 360
    SHIELD_MIN_ANGLE = 0
    CENTRAL_POINT_X = 185
    CENTRAL_POINT_Y = 185

    def __init__(self, values_range, coordinates, initial_value):
        super().__init__(values_range, coordinates, initial_value)

        # Load images
        self.bg_image = assets.load_image('compass_background')
        self.hand_image = assets.load_image('compass_hand')

    def shield_angle(self):
        """Return rotation angle of the hand, calculated from its value"""
        if self.value == self.min_value:
            return self.SHIELD_MIN_ANGLE
        if self.value == self.max_value:
            return self.SHIELD_MAX_ANGLE

        # The below calculation bases on proportion
        full_angle_range = self.SHIELD_MAX_ANGLE - self.SHIELD_MIN_ANGLE
        full_value_range = self.max_value - self.min_value
        current_value_lambda = self.value - self.min_value

        # current_value_lambda / full_value_range = current_angle_lambda / full_angle_range
        return (full_angle_range * current_value_lambda / full_value_range) + self.SHIELD_MIN_ANGLE

    def hand_image_rotated(self):
        angle = self.shield_angle()
        rotated_img = pygame.transform.rotate(self.hand_image, angle)
        rotated_rect_dimensions = rotated_img.get_rect().size
        central_point = rotated_rect_dimensions[0]/2, rotated_rect_dimensions[1]/2
        coordinates = (
            self.CENTRAL_POINT_X - central_point[0],
            self.CENTRAL_POINT_Y - central_point[1]
        )
        return rotated_img, coordinates

    @property
    def image(self):
        image = self.bg_image.copy()
        hand_image_rotated, hand_image_coordinates = self.hand_image_rotated()
        image.blit(hand_image_rotated, hand_image_coordinates)
        return image
