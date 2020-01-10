from src.assets import assets


class LevelIndicator:
    INDICATOR_X_LAMBDA = 25
    INDICATOR_MAX_Y_LAMBDA = 25
    INDICATOR_MIN_Y_LAMBDA = 769

    def __init__(self, values_range, coordinates, initial_value):
        # Load images
        self.bg_image = assets.load('indicator_panel')
        self.indicator_image = assets.load('indicator_hand')

        # Set border values
        self.min_value = values_range[0]
        self.max_value = values_range[1]

        # Initialize value
        self.value = initial_value

        # Calculate position of the elements
        self.bg_position = coordinates
        self.indicator_x_pos = coordinates[0] + self.INDICATOR_X_LAMBDA
        self.indicator_y_max = coordinates[0] + self.INDICATOR_MAX_Y_LAMBDA
        self.indicator_y_min = coordinates[0] + self.INDICATOR_MIN_Y_LAMBDA

    def indicator_y_pos(self):
        """Return y coordinate of the indicator, calculated from its value"""
        if self.value == self.min_value:
            return self.indicator_y_min
        if self.value == self.max_value:
            return self.indicator_y_max

        # The below calculation bases on proportion
        full_y_range = self.indicator_y_max - self.indicator_y_min
        full_value_range = self.max_value - self.min_value
        current_value_lambda = self.value - self.min_value

        # current_value_lambda / full_value_range = current_y_lambda / full_y_range
        return (full_y_range * current_value_lambda / full_value_range) + self.indicator_y_min

    @property
    def indicator_position(self):
        """Returns a tuple of (x, y) coordinates of the indicator"""
        return self.indicator_x_pos, self.indicator_y_pos()

    def update(self, value):
        if value > self.max_value:
            self.value = self.max_value
        elif value < self.min_value:
            self.value = self.min_value
        else:
            self.value = value
