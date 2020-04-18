from hachione import db
from graphviz import Graph, nohtml
from sqlalchemy.orm import synonym
from sqlalchemy.sql.functions import current_timestamp
from datetime import datetime
from werkzeug import check_password_hash, generate_password_hash
import base64

# ユーザクラス定義
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), primary_key=False, default='', nullable=False)
    create_date = db.Column(db.DateTime, primary_key=False, default=current_timestamp(), nullable=False)
    update_date = db.Column(db.DateTime, primary_key=False, default=current_timestamp(), onupdate=current_timestamp(), nullable=False)
    _password = db.Column('password', db.String(100), nullable=False)

    def init(self):
        db.create_all()

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor = password_descriptor)

    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, name, password):
        user = query(cls).filter(cls.username==name).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def __repr__(self):
        return u'<User id={self.id} username={self.username} create_data={self.create_date} update_data={self.update_date}>'.format(
                self=self)

# ハチワンマップとユーザの関連付けモデルクラス定義
class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), primary_key=False, default='', nullable=False)
    model = db.Column(db.PickleType, primary_key=False, nullable=False)

    def init(self):
        db.create_all()

    def get_model_from_db(self, username_in):
        entry = Entry.query.filter(self.username == username_in).first()
        return entry.model

    def set_model_to_db(self, username_in, model_in):
        entry = Entry.query.filter(self.username == username_in).first()
        entry.model = model_in
        db.session.add(entry)
        db.session.commit()

# ハチワンマップクラス定義
class HachioneModel:
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

# ハチワンマップ描画クラス定義
class ChartImageGenerator:
    def __init__(self):
        self.__CELL_W = 3
        self.__CELL_H = 3

    def get_cell_img(self, cell_text):
        cell = Graph('cell', engine='dot', format='png')
        cell.attr('node', shape='box', fontname='MS Gothic')
        cell.node(cell_text, **{'width': str(self.__CELL_W), 'height': str(self.__CELL_H)})
        return cell.pipe()

    def get_cell_img_base64(self, cell_text):
        img_byte = self.get_cell_img(cell_text)
        return base64.b64encode(img_byte).decode("ascii")

    def get_cell_label(self, cell_text, bgcolor_idx=-1):
        fontsize = str(12)

        if cell_text == '':
            cell_text = ' '

        # Cell string
        row_char_num = 6
        if len(cell_text) > row_char_num and len(cell_text) <= row_char_num*2:
            cell_text = cell_text[:row_char_num] + '''<br/>''' \
                        + cell_text[row_char_num:]
        elif len(cell_text) > row_char_num*2:
            cell_text = cell_text[:row_char_num] + '''<br/>''' \
                        + cell_text[row_char_num:row_char_num*2] + '''<br/>''' \
                        + cell_text[row_char_num*2:]

        # Cell background color setting
        # See https://www.tagindex.com/color/color_gradation.html
        if bgcolor_idx == 0:            # main_theme
            bgcolor = 'white'
            fontcolor = 'black'
        elif bgcolor_idx == 10:         # sub_theme0
            bgcolor = '#ffff80'
            fontcolor = 'black'
        elif bgcolor_idx == 11:         # sub_theme1
            bgcolor = '#ff8080'
            fontcolor = 'black'
        elif bgcolor_idx == 12:         # sub_theme2
            bgcolor = '#ff80bf'
            fontcolor = 'black'
        elif bgcolor_idx == 13:         # sub_theme3
            bgcolor = '#bfff80'
            fontcolor = 'black'
        elif bgcolor_idx == 14:         # sub_theme4
            bgcolor = '#bf80ff'
            fontcolor = 'black'
        elif bgcolor_idx == 15:         # sub_theme5
            bgcolor = '#80ff80'
            fontcolor = 'black'
        elif bgcolor_idx == 16:         # sub_theme6
            bgcolor = '#80ffff'
            fontcolor = 'black'
        elif bgcolor_idx == 17:         # sub_theme7
            bgcolor = '#8080ff'
            fontcolor = 'black'
        elif 100 <= bgcolor_idx < 110:  # sub_theme0_items
            bgcolor = '#ffffd5'
            fontcolor = 'black'
        elif 110 <= bgcolor_idx < 120:  # sub_theme1_items
            bgcolor = '#ffd5d5'
            fontcolor = 'black'
        elif 120 <= bgcolor_idx < 130:  # sub_theme2_items
            bgcolor = '#ffd5ea'
            fontcolor = 'black'
        elif 130 <= bgcolor_idx < 140:  # sub_theme3_items
            bgcolor = '#eaffd5'
            fontcolor = 'black'
        elif 140 <= bgcolor_idx < 150:  # sub_theme4_items
            bgcolor = '#ead5ff'
            fontcolor = 'black'
        elif 150 <= bgcolor_idx < 160:  # sub_theme5_items
            bgcolor = '#d5ffd5'
            fontcolor = 'black'
        elif 160 <= bgcolor_idx < 170:  # sub_theme6_items
            bgcolor = '#d5ffff'
            fontcolor = 'black'
        elif 170 <= bgcolor_idx < 180:  # sub_theme7_items
            bgcolor = '#d5d5ff'
            fontcolor = 'black'
        else:
            bgcolor = 'white'
            fontcolor = 'black'


        label = '''<TD FIXEDSIZE="TRUE" WIDTH="80" HEIGHT="80" BGCOLOR="
                    ''' + bgcolor +'''" style="font-size:
                    ''' + fontsize +'''; color=
                    ''' + fontcolor + ''';"><b>''' + cell_text + '''</b></TD>'''

        return label

    def get_chart3x3_img(self, model):
        main_theme = model.get_main_theme()
        sub_themes = model.get_sub_themes()

        chart3x3 = Graph('chart3x3', engine='dot', format='png')
        chart3x3.attr('node', shape='plaintext', fontname='Meiryo UI')

        label = '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                    <TR>
                        ''' + self.get_cell_label(sub_themes[0], 10) \
                        + self.get_cell_label(sub_themes[1], 11) \
                        + self.get_cell_label(sub_themes[2], 12) + '''
                    </TR>
                    <TR>
                        ''' + self.get_cell_label(sub_themes[3], 13) \
                        + self.get_cell_label(main_theme, 0) \
                        + self.get_cell_label(sub_themes[4], 14) + '''
                    </TR>
                    <TR>
                        ''' + self.get_cell_label(sub_themes[5], 15) \
                        + self.get_cell_label(sub_themes[6], 16) \
                        + self.get_cell_label(sub_themes[7], 17) + '''
                    </TR>
                </TABLE>>'''

        #print(label)
        chart3x3.node('chart3x3_html', label=label)

        return chart3x3.pipe()

    def get_chart9x9_img(self, model):
        main_theme = model.get_main_theme()
        sub_themes = model.get_sub_themes()
        items = model.get_items()

        chart9x9 = Graph('chart9x9', engine='dot', format='png')
        chart9x9.attr('node', shape='plaintext', fontname='Meiryo UI')

        label = '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                    <TR>
                        ''' + self.get_cell_label(items[0][0], 100) \
                        + self.get_cell_label(items[0][1], 101) \
                        + self.get_cell_label(items[0][2], 102) \
                        + self.get_cell_label(items[1][0], 110) \
                        + self.get_cell_label(items[1][1], 111) \
                        + self.get_cell_label(items[1][2], 112) \
                        + self.get_cell_label(items[2][0], 120) \
                        + self.get_cell_label(items[2][1], 121) \
                        + self.get_cell_label(items[2][2], 122) + '''
                    </TR>
                    <TR>
                        ''' + self.get_cell_label(items[0][3], 103) \
                        + self.get_cell_label(sub_themes[0], 10) \
                        + self.get_cell_label(items[0][4], 104) \
                        + self.get_cell_label(items[1][3], 113) \
                        + self.get_cell_label(sub_themes[1], 11) \
                        + self.get_cell_label(items[1][4], 114) \
                        + self.get_cell_label(items[2][3], 123) \
                        + self.get_cell_label(sub_themes[2], 12) \
                        + self.get_cell_label(items[2][4], 124) + '''
                    </TR>
                    <TR>
                        ''' + self.get_cell_label(items[0][5], 105) \
                        + self.get_cell_label(items[0][6], 106) \
                        + self.get_cell_label(items[0][7], 107) \
                        + self.get_cell_label(items[1][5], 115) \
                        + self.get_cell_label(items[1][6], 116) \
                        + self.get_cell_label(items[1][7], 117) \
                        + self.get_cell_label(items[2][5], 125) \
                        + self.get_cell_label(items[2][6], 126) \
                        + self.get_cell_label(items[2][7], 127) + '''
                    </TR>
                    <TR>
                        ''' + self.get_cell_label(items[3][0], 130) \
                        + self.get_cell_label(items[3][1], 131) \
                        + self.get_cell_label(items[3][2], 132) \
                        + self.get_cell_label(sub_themes[0], 10) \
                        + self.get_cell_label(sub_themes[1], 11) \
                        + self.get_cell_label(sub_themes[2], 12) \
                        + self.get_cell_label(items[4][0], 140) \
                        + self.get_cell_label(items[4][1], 141) \
                        + self.get_cell_label(items[4][2], 142) + '''
                    </TR>
                    <TR>
                        ''' + self.get_cell_label(items[3][3], 133) \
                        + self.get_cell_label(sub_themes[3], 13) \
                        + self.get_cell_label(items[3][4], 134) \
                        + self.get_cell_label(sub_themes[3], 13) \
                        + self.get_cell_label(main_theme, 0) \
                        + self.get_cell_label(sub_themes[4], 14) \
                        + self.get_cell_label(items[4][3], 143) \
                        + self.get_cell_label(sub_themes[4], 14) \
                        + self.get_cell_label(items[4][4], 144) + '''
                    </TR>
                    <TR>
                        ''' + self.get_cell_label(items[3][5], 135) \
                        + self.get_cell_label(items[3][6], 136) \
                        + self.get_cell_label(items[3][7], 137) \
                        + self.get_cell_label(sub_themes[5], 15) \
                        + self.get_cell_label(sub_themes[6], 16) \
                        + self.get_cell_label(sub_themes[7], 17) \
                        + self.get_cell_label(items[4][5], 145) \
                        + self.get_cell_label(items[4][6], 146) \
                        + self.get_cell_label(items[4][7], 147) + '''
                    </TR>
                    <TR>
                        ''' + self.get_cell_label(items[5][0], 150) \
                        + self.get_cell_label(items[5][1], 151) \
                        + self.get_cell_label(items[5][2], 152) \
                        + self.get_cell_label(items[6][0], 160) \
                        + self.get_cell_label(items[6][1], 161) \
                        + self.get_cell_label(items[6][2], 162) \
                        + self.get_cell_label(items[7][0], 170) \
                        + self.get_cell_label(items[7][1], 171) \
                        + self.get_cell_label(items[7][2], 172) + '''
                    </TR>
                    <TR>
                        ''' + self.get_cell_label(items[5][3], 153) \
                        + self.get_cell_label(sub_themes[5], 15) \
                        + self.get_cell_label(items[5][4], 154) \
                        + self.get_cell_label(items[6][3], 163) \
                        + self.get_cell_label(sub_themes[6], 16) \
                        + self.get_cell_label(items[6][4], 164) \
                        + self.get_cell_label(items[7][3], 173) \
                        + self.get_cell_label(sub_themes[7], 17) \
                        + self.get_cell_label(items[7][4], 174) + '''
                    </TR>
                    <TR>
                        ''' + self.get_cell_label(items[5][5], 155) \
                        + self.get_cell_label(items[5][6], 156) \
                        + self.get_cell_label(items[5][7], 157) \
                        + self.get_cell_label(items[6][5], 165) \
                        + self.get_cell_label(items[6][6], 166) \
                        + self.get_cell_label(items[6][7], 167) \
                        + self.get_cell_label(items[7][5], 175) \
                        + self.get_cell_label(items[7][6], 176) \
                        + self.get_cell_label(items[7][7], 177) + '''
                    </TR>
                </TABLE>>'''

        chart9x9.node('chart9x9_html', label=label)

        return chart9x9.pipe()


    def get_chart3x3_img_base64(self, model):
        img_byte = self.get_chart3x3_img(model)
        return base64.b64encode(img_byte).decode("ascii")

    def get_chart9x9_img_base64(self, model):
        img_byte = self.get_chart9x9_img(model)
        return base64.b64encode(img_byte).decode("ascii")
