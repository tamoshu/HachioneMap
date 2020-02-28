from flask import request, redirect, url_for, render_template, session
from mandara.models import MandaraModel
from mandara import app
import random, string

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
    model.init()
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

    elif 'items_to_done' in request.form:
        return render_template('done.html')

    elif 'done_to_items' in request.form:
        model = models[username]
        main_theme = model.get_main_theme()
        sub_themes = model.get_sub_themes()

        return render_template('subsub_sel.html',
                               username=username,
                               main_theme=main_theme,
                               sub_themes=sub_themes
                               )

    else:
        model = models[username]
        main_theme = model.get_main_theme()
        return render_template('main_theme.html',
                               username=username,
                               main_theme=main_theme
                               )


