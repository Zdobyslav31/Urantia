from src.assets import assets


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

    def image(self):
        raise NotImplementedError

    def position(self):
        raise NotImplementedError


class LevelIndicator(Device):
    HAND_X_LAMBDA = 25
    HAND_MAX_Y_LAMBDA = 25
    HAND_MIN_Y_LAMBDA = 769

    def __init__(self, values_range, coordinates, initial_value):
        super().__init__(values_range, coordinates, initial_value)
        
        # Load images
        self.bg_image = assets.load('indicator_background')
        self.hand_image = assets.load('indicator_hand')

        # Calculate position of the elements
        self.hand_x_pos = self.HAND_X_LAMBDA
        self.hand_y_max = self.HAND_MAX_Y_LAMBDA
        self.hand_y_min = self.HAND_MIN_Y_LAMBDA

    def hand_y_pos(self):
        """Return y coordinate of the hand, calculated from its value"""
        if self.value == self.min_value:
            return self.hand_y_min
        if self.value == self.max_value:
            return self.hand_y_max

        # The below calculation bases on proportion
        full_y_range = self.hand_y_max - self.hand_y_min
        full_value_range = self.max_value - self.min_value
        current_value_lambda = self.value - self.min_value

        # current_value_lambda / full_value_range = current_y_lambda / full_y_range
        return (full_y_range * current_value_lambda / full_value_range) + self.hand_y_min

    def hand_position(self):
        """Returns a tuple of (x, y) coordinates of the hand"""
        return self.hand_x_pos, self.hand_y_pos()

    @property
    def image(self):
        image = self.bg_image.copy()
        image.blit(self.hand_image, self.hand_position())
        return image

    @property
    def position(self):
        return self.coordinates


class GaugeIndicator(Device):
    def __init__(self, values_range, coordinates, initial_value):
        super().__init__(values_range, coordinates, initial_value)

        # Load images
        self.bg_image = assets.load('gauge_background')
        self.hand_image = assets.load('gauge_hand')
