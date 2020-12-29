# metadata class that describes the status of the currently typed word
class string_data:
    def __init__(self, word, renders, width):
        self.current_string = word
        self.chars = list(self.current_string)
        self.char_screens = renders
        self.current_index = 0
        self.max_len = len(self.chars)
        self.width = width