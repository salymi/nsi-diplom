# main.py
# -*- coding: utf-8 -*-
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from db_setup import init_db, db_session
from forms import TurnSearchForm, TurnForm, LinksFrom, LinkSearch, NodeFrom, NodeSearch, SituatFrom, SituatSearch, \
                    GroupSearch, GroupFrom, AuditSearch, AuditForm, FTsitSearch, FTsitForm, IcmpSearch, IcmpForm, \
                    TcpportSearch, TcpportForm, WeblSearch, WeblForm
from flask import flash, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
from models import Turn, User, Links, Node, Situat, Group, GRLink, GRNode, Audit, FTsit, Icmp, Tcpport, Webl
from tables import Results, ResultsLinks, ResultsNode, ResultsSituat, ResultsGroup, ResultAudit, ResultFTsit, ResultIcmp, \
                    ResultTcpport, ResultWebl

init_db()


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    if login and password:
        user = db_session.query(User).filter_by(LOGIN=login).first()
        if not user or not check_password_hash(user.PASSWORD, password):
            flash('Неверный логин или пароль')
            return redirect(url_for('login_page'))
        login_user(user, remember=remember)
        return redirect(url_for('turn'))
    else:
        flash('Пожалуйста, заполните поля для логина и пароля')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('turn'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста, заполните все поля')
        elif password != password2:
            flash('Пароли не равны')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(LOGIN=login, PASSWORD=hash_pwd)
            db_session.add(new_user)
            db_session.commit()

            return redirect(url_for('login_page'))
    return render_template('register.html')


# Опепрации с таблицой TURN_OFF_NODE
@app.route('/turn', methods=['GET', 'POST'])
@login_required
def turn():
    """
    начальная страница
    """
    search = TurnSearchForm(request.form)
    select = TurnSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search, select)

    # вывод полной информации с таблицы
    qry = db_session.query(Turn)
    results = qry.all()
    table = Results(results)
    table.border = True
    return render_template('turn.html', form=search, table=table)


@app.route('/results')
@login_required
def search_results(search, select):
    """
    Поиск
    """
    results = []
    search_string = search.data['search']
    select_string = select.data['select']

    if search_string == '':
        qry = db_session.query(Turn)
        results = qry.all()
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)
    # Поиск по таблицам
    else:
        if select_string == 'NAME':
            results = db_session.query(Turn).filter(Turn.NAME.like(f'%{search_string}%')).all()

        elif select_string == 'IP_NODE':
            results = db_session.query(Turn).filter(Turn.IP_NODE.like(f'%{search_string}%')).all()

        elif select_string == 'COMMENT':
            results = db_session.query(Turn).filter(Turn.COMMENT.like(f'%{search_string}%')).all()
        # сообщение если нет данных
        if not results:
            flash('Записей не найдено')
            return redirect('/turn')
        else:
            table = Results(results)
            table.border = True
            return render_template('results.html', table=table)


@app.route('/turn/turnadd', methods=['GET', 'POST'])
@login_required
def turnadd():
    """
    Добавление
    """
    form = TurnForm(request.form)
    if request.method == 'POST' and form.validate():
        if len(form.COMMENT.data) > 0:
            # сохранение записей
            turn = Turn()
            save_changes(turn, form, new=True)
            flash('Новая запись добавлена')
            return redirect('/turn')
        else:
            flash('Некорректный ввод данных')
            return redirect('/turn')
    return render_template('turnadd.html', form=form)


def save_changes(turn, form, new=False):
    """
    Сохранение записей в базу данных
    """
    # Получение данных и присвоение им атрибутов
    # обьекты таблицы SQLAlchemy
    turn.NAME = form.NAME.data
    turn.IP_NODE = form.IP_NODE.data
    turn.COMMENT = form.COMMENT.data
    if new:
        # Добавление записей в базу данных
        db_session.add(turn)
    # Сохранение в базе данных
    db_session.commit()


@app.route('/turn/item/<string:NAME>', methods=['GET', 'POST']) # Редактирование
@login_required
def turnedit(NAME):
    qry = db_session.query(Turn).filter(
        Turn.NAME == NAME)
    turn = qry.first()
    if turn:
        form = TurnForm(formdata=request.form, obj=turn)
        if request.method == 'POST' and form.validate():
            if len(form.COMMENT.data) > 0:
                # сохранение изменеий
                save_changes(turn, form)
                flash('Данные изменены')
                return redirect('/turn')
            else:
                flash('Некорректный ввод данных')
                return redirect('/turn')
        return render_template('turnedit.html', form=form)
    else:
        return 'Error loading #{NAME}'.format(NAME=NAME)

@app.route('/turn/deleteturn/<string:NAME>', methods=['GET', 'POST']) # удаление
@login_required
def deleteturn(NAME):
    qry = db_session.query(Turn).filter(
        Turn.NAME == NAME)
    turn = qry.first()
    if turn:
        form = TurnForm(formdata=request.form, obj=turn)
        if request.method == 'POST' and form.validate():
            # Удаление из баззы данных
            db_session.delete(turn)
            db_session.commit()
            flash('Данные удалены')
            return redirect('/turn')
        return render_template('deleteturn.html', form=form)
    else:
        return 'Error deleting #{NAME}'.format(NAME=NAME)


# Опепрации с таблицой LINKS
@app.route('/links', methods=['GET', 'POST'])
@login_required
def links():
    search = LinkSearch(request.form)
    select = LinkSearch(request.form)
    if request.method == 'POST':
        return search_links(search, select)

    qry = db_session.query(Links)
    results = qry.all()
    table = ResultsLinks(results)
    table.border = True
    return render_template('links.html', form=search, table=table)


@app.route('/resultslinks')
@login_required
def search_links(search, select):
    results = []
    search_string = search.data['search']
    select_string = select.data['select']

    if search_string == '':
        qry = db_session.query(Links)
        results = qry.all()
        table = ResultsLinks(results)
        table.border = True
        return render_template('resultslinks.html', table=table)
    else:
        if select_string == 'LINK':
            results = db_session.query(Links).filter(Links.LINK.like(f'%{search_string}%')).all()

        if not results:
            flash('Записей не найдено')
            return redirect('/links')
        else:
            table = ResultsLinks(results)
            table.border = True
            return render_template('resultslinks.html', table=table)


@app.route('/links/linksadd', methods=['GET', 'POST'])
@login_required
def linksadd():
    form = LinksFrom(request.form)
    if request.method == 'POST' and form.validate():
        if len(form.LINK.data) > 0:
            links = Links()
            save_links(links, form, new=True)
            flash('Новая запись добавлена')
            return redirect('/links')
        else:
            flash('Некорректный ввод данных')
            return redirect('/links')
    return render_template('linksadd.html', form=form)


def save_links(links, form, new=False):
    links.ID_GROUP = form.ID_GROUP.data
    links.LINK = form.LINK.data
    if new:
        db_session.add(links)
    db_session.commit()

def save_links1(links, form, new=False):
    link = GRLink()
    link.ID_GROUP = form.ID_GROUP.data
    link.ID_LINK = form.ID_LINK.data

    links.ID_GROUP = form.ID_GROUP.data
    links.LINK = form.LINK.data
    try:
        if new:
            db_session.add(links)
            db_session.add(link)
        db_session.commit()
    except:
        flash('Неверный id руппы')
        return redirect('/links')

@app.route('/links/item/<int:ID_LINK>', methods=['GET', 'POST'])
@login_required
def linksedit(ID_LINK):
    qry = db_session.query(Links).filter(
        Links.ID_LINK == ID_LINK)
    links = qry.first()
    qry1 = db_session.query(GRLink).filter(
        GRLink.ID_LINK == ID_LINK)
    link = qry1.first()
    if links:
        form = LinksFrom(formdata=request.form, obj=links)
        if request.method == 'POST' and form.validate():
            if len(form.LINK.data) > 0:
                if not link:
                    save_links1(links, form, new=True)
                    flash('Данные изменены')
                    return redirect('/links')
                else:
                    save_links1(links, form)
                    save_links1(link, form)
                    flash('Данные изменены')
                    return redirect('/links')
            else:
                flash('Некорректный ввод данных')
                return redirect('/links')
        return render_template('linksedit.html', form=form)
    else:
        return 'Error loading #{ID_LINK}'.format(ID_LINK=ID_LINK)


@app.route('/links/<int:ID_LINK>', methods=['GET', 'POST'])
@login_required
def deletelinks(ID_LINK):
    qry = db_session.query(Links).filter(
        Links.ID_LINK == ID_LINK)
    links = qry.first()
    qry1 = db_session.query(GRLink).filter(
        GRLink.ID_LINK == ID_LINK)
    link = qry1.first()
    if links:
        form = LinksFrom(formdata=request.form, obj=links)
        if request.method == 'POST' and form.validate():
            db_session.delete(links)
            db_session.delete(link)
            db_session.commit()
            flash('Данные удалены')
            return redirect('/links')
        return render_template('deletelinks.html', form=form)
    else:
        return 'Error deleting #{ID_LINK}'.format(ID_LINK=ID_LINK)

# Опепрации с таблицой NODE
@app.route('/node', methods=['GET', 'POST'])
@login_required
def node():
    search = NodeSearch(request.form)
    select = NodeSearch(request.form)
    if request.method == 'POST':
        return search_node(search, select)

    qry = db_session.query(Node)
    results = qry.all()
    table = ResultsNode(results)
    table.border = True
    return render_template('node.html', form=search, table=table)


@app.route('/resultsnode')
@login_required
def search_node(search, select):
    results = []
    search_string = search.data['search']
    select_string = select.data['select']

    if search_string == '':
        qry = db_session.query(Node)
        results = qry.all()
        table = ResultsNode(results)
        table.border = True
        return render_template('resultsnode.html', table=table)
    else:
        if select_string == 'NODE_NAME':
            results = db_session.query(Node).filter(Node.NODE_NAME.like(f'%{search_string}%')).all()

        elif select_string == 'IP':
            results = db_session.query(Node).filter(Node.IP.like(f'%{search_string}%')).all()
        if not results:
            flash('Записей не найдено')
            return redirect('/node')
        else:
            table = ResultsNode(results)
            table.border = True
            return render_template('resultsnode.html', table=table)


@app.route('/node/nodeadd', methods=['GET', 'POST'])
@login_required
def nodeadd():
    form = NodeFrom(request.form)
    if request.method == 'POST' and form.validate():
        if len(form.NODE_NAME.data) > 0:
            node = Node()
            save_node(node, form, new=True)
            flash('Новая запись добавлена')
            return redirect('/node')
        else:
            flash('Некорректный ввод данных')
            return redirect('/node')
    return render_template('nodeadd.html', form=form)


def save_node(node, form, new=False):
    node.NODE_NAME = form.NODE_NAME.data
    node.IP = form.IP.data
    node.ID_GROUP = form.ID_GROUP.data
    if new:
        db_session.add(node)
    db_session.commit()

def save_node1(node, form, new=False):
    nod = GRNode()
    nod.ID_GROUP = form.ID_GROUP.data
    nod.ID_NODE = form.ID_NODE.data

    node.IP = form.IP.data
    node.NODE_NAME = form.NODE_NAME.data
    node.ID_GROUP = form.ID_GROUP.data
    try:
        if new:
            db_session.add(node)
            db_session.add(nod)
        db_session.commit()
    except:
        flash('Неверный id группы')
        return redirect('/node')

@app.route('/node/item/<int:ID_NODE>', methods=['GET', 'POST'])
@login_required
def nodeedit(ID_NODE):
    qry = db_session.query(Node).filter(
        Node.ID_NODE == ID_NODE)
    node = qry.first()
    qry1 = db_session.query(GRNode).filter(
        GRNode.ID_NODE == ID_NODE)
    nod = qry1.first()
    if node:
        form = NodeFrom(formdata=request.form, obj=node)
        if request.method == 'POST' and form.validate():
            if len(form.NODE_NAME.data) > 0:
                if not nod:
                    save_node1(node, form, new=True)
                    flash('Данные изменены')
                    return redirect('/node')
                else:
                     save_node1(node, form)
                     save_node1(nod, form)
                     flash('Данные изменены')
                     return redirect('/node')
            else:
                flash('Некорректный ввод данных')
                return redirect('/node')
        return render_template('nodeedit.html', form=form)
    else:
        return 'Error loading #{ID_NODE}'.format(ID_NODE=ID_NODE)


@app.route('/node/<int:ID_NODE>', methods=['GET', 'POST'])
@login_required
def deletenode(ID_NODE):
    qry = db_session.query(Node).filter(
        Node.ID_NODE == ID_NODE)
    node = qry.first()
    qry1 = db_session.query(GRNode).filter(
        GRNode.ID_NODE == ID_NODE)
    nod = qry1.first()
    if node:
        form = NodeFrom(formdata=request.form, obj=node)
        if request.method == 'POST' and form.validate():
            db_session.delete(nod)
            db_session.delete(node)
            db_session.commit()
            flash('Данные удалены')
            return redirect('/node')
        return render_template('deletenode.html', form=form)
    else:
        return 'Error deleting #{ID_NODE}'.format(ID_NODE=ID_NODE)


# Опепрации с таблицой EVENTMAP
@app.route('/situat', methods=['GET', 'POST'])
@login_required
def situat():
    search = SituatSearch(request.form)
    select = SituatSearch(request.form)
    if request.method == 'POST':
        return search_situat(search, select)

    qry = db_session.query(Situat)
    results = qry.all()
    table = ResultsSituat(results)
    table.border = True
    return render_template('situat.html', form=search, table=table)


@app.route('/resultsituat')
@login_required
def search_situat(search, select):
    results = []
    search_string = search.data['search']
    select_string = select.data['select']

    if search_string == '':
        qry = db_session.query(Situat)
        results = qry.all()
        table = ResultsSituat(results)
        table.border = True
        return render_template('resultsituat.html', table=table)
    else:
        if select_string == 'SITUATION_ID':
            results = db_session.query(Situat).filter(Situat.SITUATION_ID.like(f'%{search_string}%')).all()

        elif select_string == 'MSG':
            results = db_session.query(Situat).filter(Situat.MSG.like(f'%{search_string}%')).all()

        elif select_string == 'APP_LABLE':
            results = db_session.query(Situat).filter(Situat.APP_LABLE.like(f'%{search_string}%')).all()
        if not results:
            flash('Записей не найдено')
            return redirect('/situat')
        else:
            table = ResultsSituat(results)
            table.border = True
            return render_template('resultsituat.html', table=table)


@app.route('/situat/situatadd', methods=['GET', 'POST'])
@login_required
def situatadd():
    form = SituatFrom(request.form)
    if request.method == 'POST' and form.validate():
        if len(form.SITUATION_ID.data) > 0:
            situat = Situat()
            save_situat(situat, form, new=True)
            flash('Новая запись добавлена')
            return redirect('/situat')
        else:
            flash('Некорректный ввод данных')
            return redirect('/situat')
    return render_template('situatadd.html', form=form)


def save_situat(situat, form, new=False):
    situat.SITUATION_ID = form.SITUATION_ID.data
    situat.MSG = form.MSG.data
    situat.APP_LABLE = form.APP_LABLE.data
    if new:
        db_session.add(situat)
    db_session.commit()


@app.route('/situat/item/<string:SITUATION_ID>', methods=['GET', 'POST'])
@login_required
def situatedit(SITUATION_ID):
    qry = db_session.query(Situat).filter(
        Situat.SITUATION_ID == SITUATION_ID)
    situat = qry.first()
    if situat:
        form = SituatFrom(formdata=request.form, obj=situat)
        if request.method == 'POST' and form.validate():
            if len(form.SITUATION_ID.data) > 0:
                save_situat(situat, form)
                flash('Данные изменены')
                return redirect('/situat')
            else:
                flash('Некорректный ввод данных')
                return redirect('/situat')
        return render_template('situatedit.html', form=form)
    else:
        return 'Error loading #{SITUATION_ID}'.format(SITUATION_ID=SITUATION_ID)


@app.route('/situat/<string:SITUATION_ID>', methods=['GET', 'POST'])
@login_required
def deletesituat(SITUATION_ID):
    qry = db_session.query(Situat).filter(
        Situat.SITUATION_ID == SITUATION_ID)
    situat = qry.first()
    if situat:
        form = SituatFrom(formdata=request.form, obj=situat)
        if request.method == 'POST' and form.validate():
            db_session.delete(situat)
            db_session.commit()
            flash('Данные удалены')
            return redirect('/situat')
        return render_template('deletesituat.html', form=form)
    else:
        return 'Error deleting #{SITUATION_ID}'.format(SITUATION_ID=SITUATION_ID)


# Опепрации с таблицой GROUP
@app.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    search = GroupSearch(request.form)
    select = GroupSearch(request.form)
    if request.method == 'POST':
        return search_group(search, select)

    qry = db_session.query(Group)
    results = qry.all()
    table = ResultsGroup(results)
    table.border = True
    return render_template('group.html', form=search, table=table)


@app.route('/resultsgroup')
@login_required
def search_group(search, select):
    results = []
    search_string = search.data['search']
    select_string = select.data['select']

    if search_string == '':
        qry = db_session.query(Group)
        results = qry.all()
        table = ResultsGroup(results)
        table.border = True
        return render_template('resultsgroup.html', table=table)
    else:
        if select_string == 'NAME_GROUP':
            results = db_session.query(Group).filter(Group.NAME_GROUP.like(f'%{search_string}%')).all()

        elif select_string == 'FLAG' and select_string == int:
            results = db_session.query(Group).filter(Group.FLAG == search_string).all()

        elif select_string == 'NOTES':
            results = db_session.query(Group).filter(Group.NOTES.like(f'%{search_string}%')).all()
        if not results:
            flash('Записей не найдено')
            return redirect('/group')
        else:
            table = ResultsGroup(results)
            table.border = True
            return render_template('resultsgroup.html', table=table)


@app.route('/group/groupadd', methods=['GET', 'POST'])
@login_required
def groupadd():
    form = GroupFrom(request.form)
    if request.method == 'POST' and form.validate():
        if len(form.NAME_GROUP.data) > 0 and len(form.FLAG.data) > 0:
            group = Group()
            save_group(group, form, new=True)
            flash('Новая запись добавлена')
            return redirect('/group')
        else:
            flash('Некорректный ввод данных')
            return redirect('/group')
    return render_template('groupadd.html', form=form)


def save_group(group, form, new=False):
    group.NAME_GROUP = form.NAME_GROUP.data
    group.FLAG = form.FLAG.data
    group.NOTES = form.NOTES.data
    if new:
        db_session.add(group)
    db_session.commit()


@app.route('/group/item/<int:ID_GROUP>', methods=['GET', 'POST'])
@login_required
def groupedit(ID_GROUP):
    qry = db_session.query(Group).filter(
        Group.ID_GROUP == ID_GROUP)
    group = qry.first()
    if group:
        form = GroupFrom(formdata=request.form, obj=group)
        if request.method == 'POST' and form.validate():
            if len(form.NAME_GROUP.data) > 0 and len(form.FLAG.data) > 0:
                save_group(group, form)
                flash('Данные изменены')
                return redirect('/group')
            else:
                flash('Некорректный ввод данных')
                return redirect('/group')
        return render_template('groupedit.html', form=form)
    else:
        return 'Error loading #{ID_GROUP}'.format(ID_GROUP=ID_GROUP)


@app.route('/group/<int:ID_GROUP>', methods=['GET', 'POST'])
@login_required
def deletegroup(ID_GROUP):
    qry = db_session.query(Group).filter(
        Group.ID_GROUP == ID_GROUP)
    group = qry.first()
    if group:
        form = GroupFrom(formdata=request.form, obj=group)
        if request.method == 'POST' and form.validate():
            db_session.delete(group)
            db_session.commit()
            flash('Данные удалены')
            return redirect('/group')
        return render_template('deletegroup.html', form=form)
    else:
        return 'Error deleting #{ID_GROUP}'.format(ID_GROUP=ID_GROUP)


# Опепрации с таблицой SERV_AUD
@app.route('/audit', methods=['GET', 'POST'])
@login_required
def audit():
    search = AuditSearch(request.form)
    select = AuditSearch(request.form)
    if request.method == 'POST':
        return search_audit(search, select)

    qry = db_session.query(Audit)
    results = qry.all()
    table = ResultAudit(results)
    table.border = True
    return render_template('audit.html', form=search, table=table)


@app.route('/resultsaudit')
@login_required
def search_audit(search, select):
    results = []
    search_string = search.data['search']
    select_string = select.data['select']

    if search_string == '':
        qry = db_session.query(Audit)
        results = qry.all()
        table = ResultAudit(results)
        table.border = True
        return render_template('resultsaudit.html', table=table)
    else:
        if select_string == 'AGENT_NAME':
            results = db_session.query(Audit).filter(Audit.AGENT_NAME.like(f'%{search_string}%')).all()

        elif select_string == 'NODE_NAME':
            results = db_session.query(Audit).filter(Audit.NODE_NAME.like(f'%{search_string}%')).all()

        elif select_string == 'IP':
            results = db_session.query(Audit).filter(Audit.IP.like(f'%{search_string}%')).all()

        elif select_string == 'EMAIL':
            results = db_session.query(Audit).filter(Audit.EMAIL.like(f'%{search_string}%')).all()

        elif select_string == 'TELEPHONE':
            results = db_session.query(Audit).filter(Audit.TELEPHONE.like(f'%{search_string}%')).all()

        elif select_string == 'DEPART':
            results = db_session.query(Audit).filter(Audit.DEPART.like(f'%{search_string}%')).all()

        elif select_string == 'INCIDENT_FLAG' and select_string == int:
            results = db_session.query(Group).filter(Group.INCIDENT_FLAG == search_string).all()

        elif select_string == 'TELEGRAM':
            results = db_session.query(Audit).filter(Audit.TELEGRAM.like(f'%{search_string}%')).all()
        if not results:
            flash('Записей не найдено')
            return redirect('/audit')
        else:
            table = ResultsGroup(results)
            table.border = True
            return render_template('resultsaudit.html', table=table)


@app.route('/audit/auditadd', methods=['GET', 'POST'])
@login_required
def auditadd():
    form = AuditForm(request.form)
    if request.method == 'POST' and form.validate():
        if len(form.AGENT_NAME.data) > 0 and len(form.NODE_NAME.data) > 0:
            audit = Audit()
            save_audit(audit, form, new=True)
            flash('Новая запись добавлена')
            return redirect('/audit')
        else:
            flash('Некорректный ввод данных')
            return redirect('/audit')
    return render_template('auditadd.html', form=form)


def save_audit(audit, form, new=False):
    audit.AGENT_NAME = form.AGENT_NAME.data
    audit.NODE_NAME = form.NODE_NAME.data
    audit.IP = form.IP.data
    audit.HOST_INFO = form.HOST_INFO.data
    audit.PRODUCT = form.PRODUCT.data
    audit.THRUNODE = form.THRUNODE.data
    audit.VERSION = form.VERSION.data
    audit.STATUS = form.STATUS.data
    audit.EMAIL = form.EMAIL.data
    audit.TELEPHONE = form.TELEPHONE.data
    audit.EMAIL_VID_ENG = form.EMAIL_VID_ENG.data
    audit.TELEP_VID_ENG = form.TELEP_VID_ENG.data
    audit.DEPART = form.DEPART.data
    audit.SERVICE_KE = form.SERVICE_KE.data
    audit.WORGROUP = form.WORGROUP.data
    audit.INCIDENT_FLAG = form.INCIDENT_FLAG.data
    audit.TELEGRAM = form.TELEGRAM.data
    audit.TELEG_VID_ENG = form.TELEG_VID_ENG.data
    if new:
        db_session.add(audit)
    db_session.commit()


@app.route('/audit/item/<string:AGENT_NAME>', methods=['GET', 'POST'])
@login_required
def auditedit(AGENT_NAME):
    qry = db_session.query(Audit).filter(
        Audit.AGENT_NAME == AGENT_NAME)
    audit = qry.first()
    if audit:
        form = AuditForm(formdata=request.form, obj=audit)
        if request.method == 'POST' and form.validate():
            if len(form.AGENT_NAME.data) > 0 and len(form.NODE_NAME.data) > 0:
                save_audit(audit, form)
                flash('Данные изменены')
                return redirect('/audit')
            else:
                flash('Некорректный ввод данных')
                return redirect('/audit')
        return render_template('auditedit.html', form=form)
    else:
        return 'Error loading #{AGENT_NAME}'.format(AGENT_NAME=AGENT_NAME)


@app.route('/audit/<string:AGENT_NAME>', methods=['GET', 'POST'])
@login_required
def deleteaudit(AGENT_NAME):
    qry = db_session.query(Audit).filter(
        Audit.AGENT_NAME == AGENT_NAME)
    audit = qry.first()
    if audit:
        form = AuditForm(formdata=request.form, obj=audit)
        if request.method == 'POST' and form.validate():
            db_session.delete(audit)
            db_session.commit()
            flash('Данные удалены')
            return redirect('/audit')
        return render_template('deleteaudit.html', form=form)
    else:
        return 'Error deleting #{AGENT_NAME}'.format(AGENT_NAME=AGENT_NAME)


# Опепрации с таблицой SERV_SIT
@app.route('/ftsit', methods=['GET', 'POST'])
@login_required
def ftsit():
    search = FTsitSearch(request.form)
    select = FTsitSearch(request.form)
    if request.method == 'POST':
        return search_ftsit(search, select)

    qry = db_session.query(FTsit)
    results = qry.all()
    table = ResultFTsit(results)
    table.border = True
    return render_template('ftsit.html', form=search, table=table)


@app.route('/resultsftsit')
@login_required
def search_ftsit(search, select):
    results = []
    search_string = search.data['search']
    select_string = select.data['select']

    if search_string == '':
        qry = db_session.query(FTsit)
        results = qry.all()
        table = ResultFTsit(results)
        table.border = True
        return render_template('resultsftsit.html', table=table)
    else:
        if select_string == 'AGENT_NAME':
            results = db_session.query(FTsit).filter(FTsit.AGENT_NAME.like(f'%{search_string}%')).all()

        elif select_string == 'SITUATION_ID':
            results = db_session.query(FTsit).filter(FTsit.SITUATION_ID.like(f'%{search_string}%')).all()

        elif select_string == 'EMAIL':
            results = db_session.query(FTsit).filter(FTsit.EMAIL.like(f'%{search_string}%')).all()

        elif select_string == 'TELEPHONE':
            results = db_session.query(FTsit).filter(FTsit.TELEPHONE.like(f'%{search_string}%')).all()

        elif select_string == 'DEPART':
            results = db_session.query(FTsit).filter(FTsit.DEPART.like(f'%{search_string}%')).all()

        elif select_string == 'FLAG_GRAFANA' and select_string == int:
            results = db_session.query(FTsit).filter(FTsit.FLAG_GRAFANA == search_string).all()

        elif select_string == 'TELEGRAM':
            results = db_session.query(FTsit).filter(FTsit.TELEGRAM.like(f'%{search_string}%')).all()

        elif select_string == 'DEPART_GRAF':
            results = db_session.query(FTsit).filter(FTsit.DEPART_GRAF.like(f'%{search_string}%')).all()
        if not results:
            flash('Записей не найдено')
            return redirect('/ftsit')
        else:
            table = ResultFTsit(results)
            table.border = True
            return render_template('resultsftsit.html', table=table)


@app.route('/ftsit/ftsitadd', methods=['GET', 'POST'])
@login_required
def ftsitadd():
    form = FTsitForm(request.form)
    if request.method == 'POST' and form.validate():
        if len(form.AGENT_NAME.data) > 0 and len(form.SITUATION_ID.data) > 0:
            ftsit = FTsit()
            save_ftsit(ftsit, form, new=True)
            flash('Новая запись добавлена')
            return redirect('/ftsit')
        else:
            flash('Некорректный ввод данных')
            return redirect('/ftsit')
    return render_template('ftsitadd.html', form=form)


def save_ftsit(ftsit, form, new=False):
    ftsit.AGENT_NAME = form.AGENT_NAME.data
    ftsit.SITUATION_ID = form.SITUATION_ID.data
    ftsit.EMAIL = form.EMAIL.data
    ftsit.TELEPHONE = form.TELEPHONE.data
    ftsit.EMAIL_VID_ENG = form.EMAIL_VID_ENG.data
    ftsit.TELEP_VID_ENG = form.TELEP_VID_ENG.data
    ftsit.DEPART = form.DEPART.data
    ftsit.SERVICE_KE = form.SERVICE_KE.data
    ftsit.WORGROUP = form.WORGROUP.data
    ftsit.FLAG_GRAFANA = form.FLAG_GRAFANA.data
    ftsit.TELEGRAM = form.TELEGRAM.data
    ftsit.TELEG_VID_ENG = form.TELEG_VID_ENG.data
    ftsit.DEPART_GRAF = form.DEPART_GRAF.data
    if new:
        db_session.add(ftsit)
    db_session.commit()


@app.route('/ftsit/item/<int:ID>', methods=['GET', 'POST'])
@login_required
def ftsitedit(ID):
    qry = db_session.query(FTsit).filter(
        FTsit.ID == ID)
    ftsit = qry.first()
    if ftsit:
        form = FTsitForm(formdata=request.form, obj=ftsit)
        if request.method == 'POST' and form.validate():
            if len(form.AGENT_NAME.data) > 0 and len(form.SITUATION_ID.data) > 0:
                save_ftsit(ftsit, form)
                flash('Данные изменены')
                return redirect('/ftsit')
            else:
                flash('Некорректный ввод данных')
                return redirect('/ftsit')
        return render_template('ftsitedit.html', form=form)
    else:
        return 'Error loading #{ID}'.format(ID=ID)


@app.route('/ftsit/<int:ID>', methods=['GET', 'POST'])
@login_required
def deleteftsit(ID):
    qry = db_session.query(FTsit).filter(
        FTsit.ID == ID)
    ftsit = qry.first()
    if ftsit:
        form = FTsitForm(formdata=request.form, obj=ftsit)
        if request.method == 'POST' and form.validate():
            db_session.delete(ftsit)
            db_session.commit()
            flash('Данные удалены')
            return redirect('/ftsit')
        return render_template('deleteftsit.html', form=form)
    else:
        return 'Error deleting #{ID}'.format(ID=ID)

# Опепрации с таблицой ICMP
@app.route('/icmp', methods=['GET', 'POST'])
@login_required
def icmp():
    search = IcmpSearch(request.form)
    select = IcmpSearch(request.form)
    if request.method == 'POST':
        return search_icmp(search, select)

    qry = db_session.query(Icmp)
    results = qry.all()
    table = ResultIcmp(results)
    table.border = True
    return render_template('icmp.html', form=search, table=table)


@app.route('/resultsicmp')
@login_required
def search_icmp(search, select):
    results = []
    search_string = search.data['search']
    select_string = select.data['select']

    if search_string == '':
        qry = db_session.query(Icmp)
        results = qry.all()
        table = ResultIcmp(results)
        table.border = True
        return render_template('resultsicmp.html', table=table)
    else:
        if select_string == 'SERVER':
            results = db_session.query(Icmp).filter(Icmp.SERVER.like(f'%{search_string}%')).all()

        elif select_string == 'DESCRIPTION':
            results = db_session.query(Icmp).filter(Icmp.DESCRIPTION.like(f'%{search_string}%')).all()

        elif select_string == 'EMAIL':
            results = db_session.query(Icmp).filter(Icmp.EMAIL.like(f'%{search_string}%')).all()

        elif select_string == 'TELEPHONE':
            results = db_session.query(Icmp).filter(Icmp.TELEPHONE.like(f'%{search_string}%')).all()

        elif select_string == 'DEPART':
            results = db_session.query(Icmp).filter(Icmp.DEPART.like(f'%{search_string}%')).all()

        elif select_string == 'INCIDENT_FLAG' and select_string == int:
            results = db_session.query(Icmp).filter(Icmp.INCIDENT_FLAG == search_string).all()

        elif select_string == 'PROFILE':
            results = db_session.query(Icmp).filter(Icmp.PROFILE.like(f'%{search_string}%')).all()

        elif select_string == 'FLAG_GRAFANA' and select_string == int:
            results = db_session.query(Icmp).filter(Icmp.FLAG_GRAFANA == search_string).all()

        elif select_string == 'DEPART_GRAF':
            results = db_session.query(Icmp).filter(Icmp.DEPART_GRAF.like(f'%{search_string}%')).all()
        if not results:
            flash('Записей не найдено')
            return redirect('/icmp')
        else:
            table = ResultIcmp(results)
            table.border = True
            return render_template('resultsicmp.html', table=table)


@app.route('/icmp/icmpadd', methods=['GET', 'POST'])
@login_required
def icmpadd():
    form = IcmpForm(request.form)
    if request.method == 'POST' and form.validate():
        if len(form.SERVER.data) > 0 and len(form.DESCRIPTION.data) > 0:
            icmp = Icmp()
            save_icmp(icmp, form, new=True)
            flash('Новая запись добавлена')
            return redirect('/icmp')
        else:
            flash('Некорректный ввод данных')
            return redirect('/icmp')
    return render_template('icmpadd.html', form=form)


def save_icmp(icmp, form, new=False):
    icmp.SERVER = form.SERVER.data
    icmp.DESCRIPTION = form.DESCRIPTION.data
    icmp.EMAIL = form.EMAIL.data
    icmp.TELEPHONE = form.TELEPHONE.data
    icmp.EMAIL_VID_ENG = form.EMAIL_VID_ENG.data
    icmp.TELEP_VID_ENG = form.TELEP_VID_ENG.data
    icmp.DEPART = form.DEPART.data
    icmp.SERVICE_KE = form.SERVICE_KE.data
    icmp.WORGROUP = form.WORGROUP.data
    icmp.INCIDENT_FLAG = form.INCIDENT_FLAG.data
    icmp.TELEGRAM = form.TELEGRAM.data
    icmp.TELEG_VID_ENG = form.TELEG_VID_ENG.data
    icmp.PROFILE = form.PROFILE.data
    icmp.FLAG_GRAFANA = form.FLAG_GRAFANA.data
    icmp.DEPART_GRAF = form.DEPART_GRAF.data
    if new:
        db_session.add(icmp)
    db_session.commit()


@app.route('/icmp/item/<int:ID>', methods=['GET', 'POST'])
@login_required
def icmpedit(ID):
    qry = db_session.query(Icmp).filter(
        Icmp.ID == ID)
    icmp = qry.first()
    if icmp:
        form = IcmpForm(formdata=request.form, obj=icmp)
        if request.method == 'POST' and form.validate():
            if len(form.SERVER.data) > 0 and len(form.DESCRIPTION.data) > 0:
                save_icmp(icmp, form)
                flash('Данные изменены')
                return redirect('/icmp')
            else:
                flash('Некорректный ввод данных')
                return redirect('/icmp')
        return render_template('icmpedit.html', form=form)
    else:
        return 'Error loading #{ID}'.format(ID=ID)


@app.route('/icmp/<int:ID>', methods=['GET', 'POST'])
@login_required
def deleteicmp(ID):
    qry = db_session.query(Icmp).filter(
        Icmp.ID == ID)
    icmp = qry.first()
    if icmp:
        form = IcmpForm(formdata=request.form, obj=icmp)
        if request.method == 'POST' and form.validate():
            db_session.delete(icmp)
            db_session.commit()
            flash('Данные удалены')
            return redirect('/icmp')
        return render_template('deleteicmp.html', form=form)
    else:
        return 'Error deleting #{ID}'.format(ID=ID)


# Опепрации с таблицой TCPPORT
@app.route('/tcpport', methods=['GET', 'POST'])
@login_required
def tcpport():
    search = TcpportSearch(request.form)
    select = TcpportSearch(request.form)
    if request.method == 'POST':
        return search_tcpport(search, select)

    qry = db_session.query(Tcpport)
    results = qry.all()
    table = ResultTcpport(results)
    table.border = True
    return render_template('tcpport.html', form=search, table=table)


@app.route('/resultstcpport')
@login_required
def search_tcpport(search, select):
    results = []
    search_string = search.data['search']
    select_string = select.data['select']

    if search_string == '':
        qry = db_session.query(Tcpport)
        results = qry.all()
        table = ResultTcpport(results)
        table.border = True
        return render_template('resultstcpport.html', table=table)
    else:
        if select_string == 'SERVER':
            results = db_session.query(Tcpport).filter(Tcpport.SERVER.like(f'%{search_string}%')).all()

        elif select_string == 'PORT':
            results = db_session.query(Tcpport).filter(Tcpport.PORT.like(f'%{search_string}%')).all()

        elif select_string == 'PROFILE':
            results = db_session.query(Tcpport).filter(Tcpport.PROFILE.like(f'%{search_string}%')).all()

        elif select_string == 'DESCRIPTION':
            results = db_session.query(Tcpport).filter(Tcpport.DESCRIPTION.like(f'%{search_string}%')).all()

        elif select_string == 'EMAIL':
            results = db_session.query(Tcpport).filter(Tcpport.EMAIL.like(f'%{search_string}%')).all()

        elif select_string == 'TELEPHONE':
            results = db_session.query(Tcpport).filter(Tcpport.TELEPHONE.like(f'%{search_string}%')).all()

        elif select_string == 'DEPART':
            results = db_session.query(Tcpport).filter(Tcpport.DEPART.like(f'%{search_string}%')).all()

        elif select_string == 'TELEGRAM':
            results = db_session.query(Tcpport).filter(Tcpport.TELEGRAM.like(f'%{search_string}%')).all()

        elif select_string == 'INCIDENT_FLAG' and select_string == int:
            results = db_session.query(Tcpport).filter(Tcpport.INCIDENT_FLAG == search_string).all()

        elif select_string == 'FLAG_GRAFANA' and select_string == int:
            results = db_session.query(Tcpport).filter(Tcpport.FLAG_GRAFANA == search_string).all()

        elif select_string == 'DEPART_GRAF':
            results = db_session.query(Tcpport).filter(Tcpport.DEPART_GRAF.like(f'%{search_string}%')).all()
        if not results:
            flash('Записей не найдено')
            return redirect('/tcpport')
        else:
            table = ResultTcpport(results)
            table.border = True
            return render_template('resultstcpport.html', table=table)


@app.route('/tcpport/tcpportadd', methods=['GET', 'POST'])
@login_required
def tcpportadd():
    form = TcpportForm(request.form)
    if request.method == 'POST' and form.validate():
        if len(form.SERVER.data) > 0 and len(form.PORT.data) > 0 and len(form.PORT.data) < 10 :
            tcpport = Tcpport()
            save_tcpport(tcpport, form, new=True)
            flash('Новая запись добавлена')
            return redirect('/tcpport')
        else:
            flash('Некорректный ввод данных')
            return redirect('/tcpport')
    return render_template('tcpportadd.html', form=form)


def save_tcpport(tcpport, form, new=False):
    tcpport.SERVER = form.SERVER.data
    tcpport.PORT = form.PORT.data
    tcpport.PROFILE = form.PROFILE.data
    tcpport.DESCRIPTION = form.DESCRIPTION.data
    tcpport.EMAIL = form.EMAIL.data
    tcpport.TELEPHONE = form.TELEPHONE.data
    tcpport.EMAIL_VID_ENG = form.EMAIL_VID_ENG.data
    tcpport.TELEP_VID_ENG = form.TELEP_VID_ENG.data
    tcpport.DEPART = form.DEPART.data
    tcpport.SERVICE_KE = form.SERVICE_KE.data
    tcpport.WORGROUP = form.WORGROUP.data
    tcpport.INCIDENT_FLAG = form.INCIDENT_FLAG.data
    tcpport.TELEGRAM = form.TELEGRAM.data
    tcpport.TELEG_VID_ENG = form.TELEG_VID_ENG.data
    tcpport.FLAG_GRAFANA = form.FLAG_GRAFANA.data
    tcpport.DEPART_GRAF = form.DEPART_GRAF.data
    if new:
        db_session.add(tcpport)
    db_session.commit()


@app.route('/tcpport/tcpport/<int:ID>', methods=['GET', 'POST'])
@login_required
def tcpportedit(ID):
    qry = db_session.query(Tcpport).filter(
        Tcpport.ID == ID)
    tcpport = qry.first()
    if tcpport:
        form = TcpportForm(formdata=request.form, obj=tcpport)
        if request.method == 'POST' and form.validate():
            if len(form.SERVER.data) > 0 and len(form.PORT.data) > 0 and len(form.PORT.data) < 10:
                save_tcpport(tcpport, form)
                flash('Данные изменены')
                return redirect('/tcpport')
            else:
                flash('Некорректный ввод данных')
                return redirect('/tcpport')
        return render_template('tcpportedit.html', form=form)
    else:
        return 'Error loading #{ID}'.format(ID=ID)

@app.route('/tcpport/<int:ID>', methods=['GET', 'POST'])
@login_required
def deletetcpport(ID):
    qry = db_session.query(Tcpport).filter(
        Tcpport.ID == ID)
    tcpport = qry.first()
    if tcpport:
        form = TcpportForm(formdata=request.form, obj=tcpport)
        if request.method == 'POST' and form.validate():
            db_session.delete(tcpport)
            db_session.commit()
            flash('Данные удалены')
            return redirect('/tcpport')
        return render_template('deletetcpport.html', form=form)
    else:
        return 'Error deleting #{ID}'.format(ID=ID)

# Опепрации с таблицой WEBLIN
@app.route('/webl', methods=['GET', 'POST'])
@login_required
def webl():
    search = WeblSearch(request.form)
    select = WeblSearch(request.form)
    if request.method == 'POST':
        return search_webl(search, select)

    qry = db_session.query(Webl)
    results = qry.all()
    table = ResultWebl(results)
    table.border = True
    return render_template('webl.html', form=search, table=table)


@app.route('/resultswebl')
@login_required
def search_webl(search, select):
    results = []
    search_string = search.data['search']
    select_string = select.data['select']

    if search_string == '':
        qry = db_session.query(Webl)
        results = qry.all()
        table = ResultWebl(results)
        table.border = True
        return render_template('resultswebl.html', table=table)
    else:
        if select_string == 'URL':
            results = db_session.query(Webl).filter(Webl.URL.like(f'%{search_string}%')).all()

        elif select_string == 'PROFILE':
            results = db_session.query(Webl).filter(Webl.PROFILE.like(f'%{search_string}%')).all()

        elif select_string == 'DESCRIPTION':
            results = db_session.query(Webl).filter(Webl.DESCRIPTION.like(f'%{search_string}%')).all()

        elif select_string == 'TABLE':
            results = db_session.query(Webl).filter(Webl.TABLE.like(f'%{search_string}%')).all()

        elif select_string == 'EMAIL':
            results = db_session.query(Webl).filter(Webl.EMAIL.like(f'%{search_string}%')).all()

        elif select_string == 'TELEPHONE':
            results = db_session.query(Webl).filter(Webl.TELEPHONE.like(f'%{search_string}%')).all()

        elif select_string == 'DEPART':
            results = db_session.query(Webl).filter(Webl.DEPART.like(f'%{search_string}%')).all()

        elif select_string == 'INCIDENT_FLAG' and select_string == int:
            results = db_session.query(Webl).filter(Webl.INCIDENT_FLAG == search_string).all()

        elif select_string == 'TELEGRAM':
            results = db_session.query(Webl).filter(Webl.TELEGRAM.like(f'%{search_string}%')).all()

        elif select_string == 'FLAG_GRAFANA' and select_string == int:
            results = db_session.query(Webl).filter(Webl.FLAG_GRAFANA == search_string).all()

        elif select_string == 'DEPART_GRAF':
            results = db_session.query(Webl).filter(Webl.DEPART_GRAF.like(f'%{search_string}%')).all()
        if not results:
            flash('Записей не найдено')
            return redirect('/webl')
        else:
            table = ResultWebl(results)
            table.border = True
            return render_template('resultswebl.html', table=table)


@app.route('/webl/webladd', methods=['GET', 'POST'])
@login_required
def webladd():
    form = WeblForm(request.form)
    if request.method == 'POST' and form.validate():
        if len(form.URL.data) > 0:
            webl = Webl()
            save_webl(webl, form, new=True)
            flash('Новая запись добавлена')
            return redirect('/webl')
        else:
            flash('Некорректный ввод данных')
            return redirect('/webl')
    return render_template('webladd.html', form=form)


def save_webl(webl, form, new=False):
    webl.URL = form.URL.data
    webl.PROFILE = form.PROFILE.data
    webl.DESCRIPTION = form.DESCRIPTION.data
    webl.TABLE = form.TABLE.data
    webl.EMAIL = form.EMAIL.data
    webl.TELEPHONE = form.TELEPHONE.data
    webl.SERVICE_KE = form.SERVICE_KE.data
    webl.DEPART = form.DEPART.data
    webl.INCIDENT_FLAG = form.INCIDENT_FLAG.data
    webl.EMAIL_VID_ENG = form.EMAIL_VID_ENG.data
    webl.TELEP_VID_ENG = form.TELEP_VID_ENG.data
    webl.TELEGRAM = form.TELEGRAM.data
    webl.TELEG_VID_ENG = form.TELEG_VID_ENG.data
    webl.FLAG_GRAFANA = form.FLAG_GRAFANA.data
    webl.DEPART_GRAF = form.DEPART_GRAF.data
    if new:
        db_session.add(webl)
    db_session.commit()


@app.route('/webl/webl/<int:ID>', methods=['GET', 'POST'])
@login_required
def webledit(ID):
    qry = db_session.query(Webl).filter(
        Webl.ID == ID)
    webl = qry.first()
    if webl:
        form = WeblForm(formdata=request.form, obj=webl)
        if request.method == 'POST' and form.validate():
            if len(form.URL.data) > 0:
                save_webl(webl, form)
                flash('Данные изменены')
                return redirect('/webl')
            else:
                flash('Некорректный ввод данных')
                return redirect('/webl')
        return render_template('webledit.html', form=form)
    else:
        return 'Error loading #{ID}'.format(ID=ID)

@app.route('/webl/<int:ID>', methods=['GET', 'POST'])
@login_required
def deletewebl(ID):
    qry = db_session.query(Webl).filter(
        Webl.ID == ID)
    webl = qry.first()
    if webl:
        form = WeblForm(formdata=request.form, obj=webl)
        if request.method == 'POST' and form.validate():
            db_session.delete(webl)
            db_session.commit()
            flash('Данные удалены')
            return redirect('/webl')
        return render_template('deletewebl.html', form=form)
    else:
        return 'Error deleting #{ID}'.format(ID=ID)

if __name__ == '__main__':
    import os

    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    app.run(port=5001)
