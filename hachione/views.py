from flask import request, redirect, url_for, render_template, session, flash
from hachione.models import Entry, User
from hachione.models import HachioneModel
from hachione.models import ChartImageGenerator
from hachione.models import CellForm
from hachione import app, db
import pickle

#models = {}
cig = ChartImageGenerator()
cell_form = CellForm()

# 入力されたハチワンマップのマスのクラスタグを特定する関数
def get_cell_name(request_input):
    # key_listの作成（'main_theme', 'sub_theme*', 'item*_*'のリスト）
    key_list = ['main_theme']

    for ii in range(8):
        key = 'sub_theme' + str(ii)
        key_list.append(key)

    for ii in range(8):
        for jj in range(8):
            key = 'item' + str(ii) + '_' + str(jj)
            key_list.append(key)

    # key_listの要素で、リクエストのキーに含まれるものを検索し、返す（main_theme, sub_theme*, item*_*のいずれかが含まれる）
    for key in key_list:
        if key in request_input.form:
            if key == 'main_theme':
                cell_type = 'main_theme'
                index1 = 0
                index2 = 0

            elif 'sub_theme' in key:
                cell_type = 'sub_theme'
                index1 = int(key[-1])   # 'sub_theme*'の'*'を取り出す
                index2 = 0

            elif 'item' in key:
                cell_type = 'item'
                index1 = int(key[-3])   # 'item*_#*'の'*'を取り出す
                index2 = int(key[-1])   # 'item*_#*'の'#'を取り出す

            else:
                break

            return cell_type, index1, index2

    return None, -1, -1


@app.route('/')
def init():
    return redirect(url_for('show_index'))


@app.route('/index')
def show_index():
    # ユーザー画面への不正アクセスをブロック
    if 'user_name' in session:
        user = User.query.filter(User.username == session['user_name']).first()
        if user:
            return render_template('index.html', login=True)

    return render_template('index.html', login=False)


@app.route('/chart')
def goto_login():
    return redirect(url_for('login'))


@app.route('/chart/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user, authenticated = User.authenticate(db.session.query,
                request.form['name'], request.form['password'])

        if authenticated:
            session['user_id'] = user.id
            session['user_name'] = user.username
            flash('ログイン完了', 'logged_in')
            return redirect(url_for('show_chart', username=user.username))
        else:
            flash('ユーザー名かパスワードに誤りがあります（忘れた場合は、新しく作り直してください。。。）', 'login_error')

    if 'user_id' in session:
        if User.query.filter(User.id == session['user_id']).first():
            return redirect(url_for('show_chart', username=session['user_name']))

    return render_template('login.html', login=False)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('ログアウト完了', 'logged_out')
    return redirect(url_for('show_index'))


@app.route('/chart/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        if request.form['name'] == '':
            flash('ユーザー名をなにか入力してくださいませ', 'create_user_error')
            return redirect(url_for('login'))

        if request.form['password'] == '':
            flash('パスワードをなにか入力してくださいませ', 'create_user_error')
            return redirect(url_for('login'))

        if User.query.filter(User.username == request.form['name']).first():
            flash('そのユーザー名はすでに使われています。他のユーザー名を指定ください。', 'create_user_error')
            return redirect(url_for('login'))

        user = User(username=request.form['name'],
                    password=request.form['password'])
        db.session.add(user)
        db.session.commit()

        # create model
        model = HachioneModel()

        # models[username] = model
        model_pickled = pickle.dumps(model)

        entry = Entry(username=user.username, model=model_pickled)
        db.session.add(entry)
        db.session.commit()

        session['user_id'] = user.id
        session['user_name'] = user.username

        return redirect(url_for('show_chart', username=user.username))

    else:
        return redirect(url_for('login'))


@app.route('/chart/<string:username>', methods=['GET', 'POST'])
def show_chart(username):
    # ユーザー画面への不正アクセスをブロック
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if session['user_name'] != username:
            return redirect(url_for('login'))

        user = User.query.filter(User.username == username).first()
        if not user:
            return redirect(url_for('login'))

    user.update_update_date()
    entry = Entry.query.filter(Entry.username == username).first()
    model = pickle.loads(entry.model)

    # 画面遷移のパターンで分岐
    if 'main_to_sub' in request.form:
        if cell_form.validate_celltext(request.form['main_theme']) == False:    # Validation NG
            flash('ごめんなさい、「/」「\\」「&」「<」「>」「[」「]」の文字は使えません。','validation_error')
            return render_template('main_theme.html',
                                   username=username,
                                   login=True,
                                   main_theme=model.main_theme
                                   )

        else:
            model.main_theme = request.form['main_theme']

            model_pickled = pickle.dumps(model)
            entry.model = model_pickled
            db.session.commit()

            chart_img3x3 = cig.get_chart3x3_img_base64(model)

            return render_template('sub_theme.html',
                                   username=username,
                                   login=True,
                                   chart_img3x3=chart_img3x3
                                   )

    elif 'sub_to_main' in request.form:
        main_theme = model.get_main_theme()

        return render_template('main_theme.html',
                               username=username,
                               login=True,
                               main_theme=main_theme
                               )

    elif 'reload_sub' in request.form:
        sub_themes = model.get_sub_themes()

        cell_type, index1, _ = get_cell_name(request)
        if cell_type == 'main_theme':
            if cell_form.validate_celltext(request.form[cell_type]) == False:  # Validation NG
                flash('ごめんなさい、「/」「\\」「&」「<」「>」「[」「]」の文字は使えません。', 'validation_error')
            else:
                main_theme = request.form[cell_type]
                model.set_main_theme(main_theme)

        elif cell_type == 'sub_theme':
            if cell_form.validate_celltext(request.form[cell_type + str(index1)]) == False:  # Validation NG
                flash('ごめんなさい、「/」「\\」「&」「<」「>」「[」「]」の文字は使えません。', 'validation_error')
            else:
                sub_themes[index1] = request.form[cell_type + str(index1)]
                model.set_sub_themes(sub_themes)

        model_pickled = pickle.dumps(model)
        entry.model = model_pickled
        db.session.commit()

        chart_img3x3 = cig.get_chart3x3_img_base64(model)

        return render_template('sub_theme.html',
                               username=username,
                               login=True,
                               chart_img3x3=chart_img3x3
                               )

    elif 'sub_to_items_all' in request.form:
        chart_img9x9 = cig.get_chart9x9_img_base64(model)

        return render_template('items_all.html',
                               username=username,
                               login=True,
                               chart_img9x9=chart_img9x9
                               )

    elif 'items_all_to_sub' in request.form:
        chart_img3x3 = cig.get_chart3x3_img_base64(model)

        return render_template('sub_theme.html',
                               username=username,
                               login=True,
                               chart_img3x3=chart_img3x3
                               )

    elif 'reload_items_all' in request.form:
        sub_themes = model.get_sub_themes()
        items = model.get_items()

        cell_type, index1, index2 = get_cell_name(request)
        if cell_type == 'main_theme':
            if cell_form.validate_celltext(request.form[cell_type]) == False:  # Validation NG
                flash('ごめんなさい、「/」「\\」「&」「<」「>」「[」「]」の文字は使えません。', 'validation_error')
            else:
                main_theme = request.form[cell_type]
                model.set_main_theme(main_theme)

        elif cell_type == 'sub_theme':
            if cell_form.validate_celltext(request.form[cell_type + str(index1)]) == False:  # Validation NG
                flash('ごめんなさい、「/」「\\」「&」「<」「>」「[」「]」の文字は使えません。', 'validation_error')
            else:
                sub_themes[index1] = request.form[cell_type + str(index1)]
                model.set_sub_themes(sub_themes)

        elif cell_type == 'item':
            if cell_form.validate_celltext(request.form[cell_type + str(index1) + '_' + str(index2)]) == False:  # Validation NG
                flash('ごめんなさい、「/」「\\」「&」「<」「>」「[」「]」の文字は使えません。', 'validation_error')
            else:
                items[index1][index2] = request.form[cell_type + str(index1) + '_' + str(index2)]
                model.set_items(items)

        model_pickled = pickle.dumps(model)
        entry.model = model_pickled
        db.session.commit()

        chart_img9x9 = cig.get_chart9x9_img_base64(model)

        return render_template('items_all.html',
                               username=username,
                               login=True,
                               chart_img9x9=chart_img9x9
                               )

    elif 'items_all_to_done' in request.form:
        chart_img9x9 = cig.get_chart9x9_img_base64(model)

        return render_template('done.html',
                               username=username,
                               login=True,
                               chart_img9x9=chart_img9x9
                               )

    elif 'done_to_items_all' in request.form:
        chart_img9x9 = cig.get_chart9x9_img_base64(model)

        return render_template('items_all.html',
                               username=username,
                               login=True,
                               chart_img9x9=chart_img9x9
                               )

    elif 'restart' in request.form:
        model.init()
        main_theme = model.get_main_theme()

        model_pickled = pickle.dumps(model)
        entry.model = model_pickled
        db.session.commit()

        return render_template('main_theme.html',
                               username=username,
                               login=True,
                               main_theme=main_theme
                               )

    else:
        main_theme = model.get_main_theme()

        return render_template('main_theme.html',
                               username=username,
                               login=True,
                               main_theme=main_theme
                               )
