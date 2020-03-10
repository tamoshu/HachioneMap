from flask import request, redirect, url_for, render_template, session
from mandara.models import MandaraModel
from mandara import app
import random, string

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
#from io import BytesIO
import io
import base64

models = {}

@app.route('/', methods=['GET','POST'])
def set_username():
    max_models_num = 20

    username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    app.logger.debug('username = ' + username)

    # username重複制限
    while username in models.keys():
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        app.logger.debug('username = ' + username)

    # model数制限
    if len(models) > max_models_num - 1:
        models.pop(0)

    model = MandaraModel()
    models[username] = model

    return redirect(url_for('show_chart', username=username))

@app.route('/<string:username>', methods=['GET','POST'])
def show_chart(username):
    #app.logger.debug(request.form)
    items = ['items0','items1','items2','items3','items4','items5','items6','items7','items8']
    items_existence = []
    for item in items:
        items_existence.append(item in request.form)

    if 'main_to_sub' in request.form:
        model = models[username]
        model.set_main_theme(request.form['main_theme'])

        main_theme = model.get_main_theme()
        sub_themes = model.get_sub_themes()
        return render_template('sub_theme.html',
                                username=username,
                                main_theme=main_theme,
                                sub_themes=sub_themes
                                )

    elif 'sub_to_main' in request.form:
        model = models[username]
        main_theme = model.get_main_theme()
        return render_template('main_theme.html',
                               username=username,
                               main_theme=main_theme
                               )

    elif 'sub_to_items_all' in request.form:
        model = models[username]
        main_theme = model.get_main_theme()

        sub_themes = [''] * 8
        sub_themes[0] = request.form['sub_theme0']
        sub_themes[1] = request.form['sub_theme1']
        sub_themes[2] = request.form['sub_theme2']
        sub_themes[3] = request.form['sub_theme3']
        sub_themes[4] = request.form['sub_theme4']
        sub_themes[5] = request.form['sub_theme5']
        sub_themes[6] = request.form['sub_theme6']
        sub_themes[7] = request.form['sub_theme7']
        model.set_sub_themes(sub_themes)

        items = model.get_items()

        return render_template('items_all.html',
                               username=username,
                               main_theme=main_theme,
                               sub_themes=sub_themes,
                               items=items
                               )

    elif 'items_all_to_sub' in request.form:
        model = models[username]
        main_theme = model.get_main_theme()
        sub_themes = model.get_sub_themes()
        items = model.get_items()

        for subtheme_index in range(8):
            for item_index in range(8):
                temp_string = 'item' + str(subtheme_index) + '_' + str(item_index)
                items[subtheme_index][item_index] = request.form[temp_string]

        model.set_items(items)

        return render_template('sub_theme.html',
                                username=username,
                                main_theme=main_theme,
                                sub_themes=sub_themes
                                )

        """
        elif 'sub_to_items_sel' in request.form:
            model = models[username]
            main_theme = model.get_main_theme()
    
            sub_themes = [''] * 8
            sub_themes[0] = request.form['sub_theme0']
            sub_themes[1] = request.form['sub_theme1']
            sub_themes[2] = request.form['sub_theme2']
            sub_themes[3] = request.form['sub_theme3']
            sub_themes[4] = request.form['sub_theme4']
            sub_themes[5] = request.form['sub_theme5']
            sub_themes[6] = request.form['sub_theme6']
            sub_themes[7] = request.form['sub_theme7']
            model.set_sub_themes(sub_themes)
    
            return render_template('subsub_sel.html',
                                   username=username,
                                   main_theme=main_theme,
                                   sub_themes=sub_themes
                                   )
    
        elif 'items_sel_to_sub' in request.form:
            model = models[username]
            main_theme = model.get_main_theme()
            sub_themes = model.get_sub_themes()
    
            return render_template('sub_theme.html',
                                   username=username,
                                   main_theme=main_theme,
                                   sub_themes=sub_themes
                                   )
    
        elif any(items_existence):  # items_sel to items
            model = models[username]
            sub_themes = model.get_sub_themes()
    
            sub_theme_no = items_existence.index(True)
            sub_theme = sub_themes[sub_theme_no]
    
            items = model.get_items()
    
            return render_template('items.html',
                                   username=username,
                                   sub_theme=sub_theme,
                                   sub_theme_no=sub_theme_no,
                                   items=items[sub_theme_no]
                                   )
    
        elif 'items_to_items_sel' in request.form:
            model = models[username]
            sub_items = [''] * 8
            sub_items[0] = request.form['item0']
            sub_items[1] = request.form['item1']
            sub_items[2] = request.form['item2']
            sub_items[3] = request.form['item3']
            sub_items[4] = request.form['item4']
            sub_items[5] = request.form['item5']
            sub_items[6] = request.form['item6']
            sub_items[7] = request.form['item7']
    
            main_theme = model.get_main_theme()
            sub_themes = model.get_sub_themes()
            sub_theme_no = sub_themes.index(request.form['sub_theme'])
    
            items = model.get_items()
            items[sub_theme_no] = sub_items
            model.set_items(items)
    
            return render_template('subsub_sel.html',
                                   username=username,
                                   main_theme=main_theme,
                                   sub_themes=sub_themes
                                   )
        """

    elif 'items_all_to_done' in request.form:
        import pandas.plotting as plotting
        model = models[username]

        items = model.get_items()

        ### Save items
        for subtheme_index in range(8):
            for item_index in range(8):
                temp_string = 'item' + str(subtheme_index) + '_' + str(item_index)
                items[subtheme_index][item_index] = request.form[temp_string]

        model.set_items(items)

        ### Get chart
        chart = model.get_chart()
        df_chart = pd.DataFrame(chart)

        fig, ax = plt.subplots(1, 1)
        plotting.table(ax, df_chart, loc='center')
        ax.axis('off')

        canvas = FigureCanvasAgg(fig)
        png_output = io.BytesIO()
        canvas.print_png(png_output)
        plt.savefig(png_output)

        img_data = base64.b64encode(png_output.getvalue())

        ''' # Using plotly
        import plotly.graph_objects as go

        fig_go = go.Figure(data=[go.Table(
            cells=dict(values=df_chart.values,
                       fill_color='lavender',
                       align='left'))
        ])
        png = fig_go.to_image(format="png")
        img_data = base64.b64encode(png)
        '''

        return render_template('done.html',
                               username=username,
                               img_data=img_data.decode("ascii")
                               )

    elif 'done_to_items_all' in request.form:
        model = models[username]
        main_theme = model.get_main_theme()
        sub_themes = model.get_sub_themes()
        items = model.get_items()

        """
        return render_template('subsub_sel.html',
                               username=username,
                               main_theme=main_theme,
                               sub_themes=sub_themes
                               )
        """
        return render_template('items_all.html',
                               username=username,
                               main_theme=main_theme,
                               sub_themes=sub_themes,
                               items=items
                               )

    else:
        model = models[username]
        model.init()
        main_theme = model.get_main_theme()
        return render_template('main_theme.html',
                               username=username,
                               main_theme=main_theme
                               )


