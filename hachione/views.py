from flask import request, redirect, url_for, render_template
from hachione.models import HachioneModel
from hachione.models import ChartImageGenerator
from hachione import app
import random
import string

models = {}
CIG = ChartImageGenerator()


def get_cell_name(request_input):
    key_list = ['main_theme']

    for ii in range(8):
        key = 'sub_theme' + str(ii)
        key_list.append(key)

    for ii in range(8):
        for jj in range(8):
            key = 'item' + str(ii) + '_' + str(jj)
            key_list.append(key)

    for key in key_list:
        if key in request_input.form:
            if key == 'main_theme':
                cell_type = 'main_theme'
                index1 = 0
                index2 = 0

            elif 'sub_theme' in key:
                cell_type = 'sub_theme'
                index1 = int(key[-1])
                index2 = 0

            elif 'item' in key:
                cell_type = 'item'
                index1 = int(key[-3])
                index2 = int(key[-1])

            else:
                break

            return cell_type, index1, index2

    return None, -1, -1


@app.route('/')
def init():
    return redirect(url_for('show_index'))


@app.route('/index')
def show_index():
    return render_template('index.html')


@app.route('/chart')
def set_username():
    max_models_num = 20

    username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    # app.logger.debug('username = ' + username)

    # username重複制限
    while username in models.keys():
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        # app.logger.debug('username = ' + username)

    # model数制限
    if len(models) > max_models_num - 1:
        models.pop(next(iter(models)))  # 先頭のusername, modelを削除

    model = HachioneModel()

    # for heroku debug
    print(models.keys())
    app.logger.debug('model keys : ' + models.keys())

    models[username] = model

    return redirect(url_for('show_chart', username=username))


@app.route('/chart/<string:username>', methods=['GET', 'POST'])
def show_chart(username):

    # for heroku debug
    print(models.keys())
    app.logger.debug('model keys : ' + models.keys())

    items = ['items0', 'items1', 'items2', 'items3', 'items4', 'items5', 'items6', 'items7', 'items8']
    items_existence = []
    for item in items:
        items_existence.append(item in request.form)

    if 'main_to_sub' in request.form:
        model = models[username]
        model.set_main_theme(request.form['main_theme'])

        chart_img3x3 = CIG.get_chart3x3_img_base64(model)

        return render_template('sub_theme.html',
                               username=username,
                               chart_img3x3=chart_img3x3
                               )

    elif 'sub_to_main' in request.form:
        model = models[username]
        main_theme = model.get_main_theme()
        return render_template('main_theme.html',
                               username=username,
                               main_theme=main_theme
                               )

    elif 'reload_sub' in request.form:
        model = models[username]
        sub_themes = model.get_sub_themes()

        cell_type, index1, _ = get_cell_name(request)
        if cell_type == 'main_theme':
            main_theme = request.form[cell_type]
            model.set_main_theme(main_theme)

        elif cell_type == 'sub_theme':
            sub_themes[index1] = request.form[cell_type + str(index1)]
            model.set_sub_themes(sub_themes)

        chart_img3x3 = CIG.get_chart3x3_img_base64(model)

        return render_template('sub_theme.html',
                               username=username,
                               chart_img3x3=chart_img3x3
                               )

    elif 'sub_to_items_all' in request.form:
        model = models[username]
        chart_img9x9 = CIG.get_chart9x9_img_base64(model)

        return render_template('items_all.html',
                               username=username,
                               chart_img9x9=chart_img9x9
                               )

    elif 'items_all_to_sub' in request.form:
        model = models[username]

        chart_img3x3 = CIG.get_chart3x3_img_base64(model)

        return render_template('sub_theme.html',
                               username=username,
                               chart_img3x3=chart_img3x3
                               )

    elif 'reload_items_all' in request.form:
        model = models[username]
        sub_themes = model.get_sub_themes()
        items = model.get_items()

        cell_type, index1, index2 = get_cell_name(request)
        if cell_type == 'main_theme':
            main_theme = request.form[cell_type]
            model.set_main_theme(main_theme)

        elif cell_type == 'sub_theme':
            sub_themes[index1] = request.form[cell_type + str(index1)]
            model.set_sub_themes(sub_themes)

        elif cell_type == 'item':
            items[index1][index2] = request.form[cell_type + str(index1) + '_' + str(index2)]
            model.set_items(items)

        chart_img9x9 = CIG.get_chart9x9_img_base64(model)

        return render_template('items_all.html',
                               username=username,
                               chart_img9x9=chart_img9x9
                               )

    elif 'items_all_to_done' in request.form:
        model = models[username]
        chart_img9x9 = CIG.get_chart9x9_img_base64(model)

        return render_template('done.html',
                               username=username,
                               chart_img9x9=chart_img9x9
                               )

    elif 'done_to_items_all' in request.form:
        model = models[username]
        chart_img9x9 = CIG.get_chart9x9_img_base64(model)

        return render_template('items_all.html',
                               username=username,
                               chart_img9x9=chart_img9x9
                               )

    else:
        model = models[username]
        model.init()
        main_theme = model.get_main_theme()
        return render_template('main_theme.html',
                               username=username,
                               main_theme=main_theme
                               )
