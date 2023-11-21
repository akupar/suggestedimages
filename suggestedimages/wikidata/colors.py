from ..constants import *


class GetColorClass:
    current_index = 0
    colors = {}

    def __call__(self, id):
        if id not in self.colors:
            self.current_index += 1
            self.colors[id] = self.current_index
        return f'color-{self.colors[id] % NUM_COLORS}'
