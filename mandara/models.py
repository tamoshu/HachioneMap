class MandaraModel:
    def __init__(self):
        self.__SUB_THEME_NUM = 8
        self.__ITEM_NUM = 8
        self.__CHART_ROW_NUM = 9
        self.__CHART_COL_NUM = 9

        self.main_theme = ''
        self.sub_themes = [''] * self.__SUB_THEME_NUM
        self.items = [[''] * self.__ITEM_NUM for i in range(self.__SUB_THEME_NUM)]
        self.table = [[''] * self.__CHART_COL_NUM for i in range(self.__CHART_ROW_NUM)]


    def init(self):
        self.main_theme = ''
        self.sub_themes = [''] * self.__SUB_THEME_NUM
        self.items = [[''] * self.__ITEM_NUM for i in range(self.__SUB_THEME_NUM)]
        self.table = [[''] * self.__CHART_COL_NUM for i in range(self.__CHART_ROW_NUM)]

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

    def get_chart(self):
        # Row 1
        for col in range(self.__CHART_COL_NUM):
            self.table[0][col] = self.items[int(col/3)][col%3]

        # Row 2
        self.table[1][0] = self.items[0][3]
        self.table[1][1] = self.sub_themes[0]
        self.table[1][2] = self.items[0][4]
        self.table[1][3] = self.items[1][3]
        self.table[1][4] = self.sub_themes[1]
        self.table[1][5] = self.items[1][4]
        self.table[1][6] = self.items[2][3]
        self.table[1][7] = self.sub_themes[2]
        self.table[1][8] = self.items[2][4]

        # Row 3
        for col in range(self.__CHART_COL_NUM):
            self.table[2][col] = self.items[int(col/3)][col%3 + 5]

        # Row 4
        for col in range(3):
            self.table[3][col] = self.items[int(col/3) + 3][col%3]
        for col in range(3):
            self.table[3][col+3] = self.sub_themes[col]
        for col in range(3):
            self.table[3][col+6] = self.items[int(col/3) + 4][col%3]

        # Row 5
        self.table[4][0] = self.items[3][3]
        self.table[4][1] = self.sub_themes[3]
        self.table[4][2] = self.items[3][4]
        self.table[4][3] = self.sub_themes[3]
        self.table[4][4] = self.main_theme
        self.table[4][5] = self.sub_themes[4]
        self.table[4][6] = self.items[4][3]
        self.table[4][7] = self.sub_themes[4]
        self.table[4][8] = self.items[4][4]

        # Row 6
        for col in range(self.__CHART_COL_NUM):
            self.table[5][col] = self.items[int(col/3) + 3][col%3 + 5]
        for col in range(3):
            self.table[5][col+3] = self.sub_themes[col+5]
        for col in range(3):
            self.table[5][col+6] = self.items[int(col/3) + 4][col%3 + 5]

        # Row 7
        for col in range(self.__CHART_COL_NUM):
            self.table[6][col] = self.items[int(col/3) + 5][col%3]

        # Row 8
        self.table[7][0] = self.items[5][3]
        self.table[7][1] = self.sub_themes[5]
        self.table[7][2] = self.items[5][4]
        self.table[7][3] = self.items[6][3]
        self.table[7][4] = self.sub_themes[6]
        self.table[7][5] = self.items[6][4]
        self.table[7][6] = self.items[7][3]
        self.table[7][7] = self.sub_themes[7]
        self.table[7][8] = self.items[7][4]

        # Row 9
        for col in range(self.__CHART_COL_NUM):
            self.table[8][col] = self.items[int(col/3) + 5][col%3 + 5]

        return self.table
