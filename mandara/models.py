class MandaraModel:

    def __init__(self):
        self.main_theme = ''
        self.sub_themes = [''] * 8
        self.items = [[''] * 8] * 8

    def init(self):
        self.main_theme = ''
        self.sub_themes = [''] * 8

    def get_main_theme(self):
        return self.main_theme

    def get_sub_themes(self):
        return self.sub_themes

    def get_items(self):
        return self.items

    def set_main_theme(self, main_theme):
        self.main_theme = main_theme

    def set_sub_themes(self, sub_themes):
        self.sub_themes = sub_themes

    def set_items(self, items):
        self.items = items
