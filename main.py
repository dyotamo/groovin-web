from os import environ

from flask import Flask, render_template, flash, redirect, url_for, jsonify, request
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb


from services import get_promoter, check_promoter, create_event, get_event, remove_event, update_event, create_ticket
from forms import LoginForm, EventForm, TicketForm
from utils import view_event_dlc, upload_photo, is_valid_date_time, ticket_already_added
from models import db


app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY') or 'secret'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'É necessário autenticar-se para aceder ao sistema'
login_manager.login_message_category = "warning"

breadcrumbs = Breadcrumbs()
breadcrumbs.init_app(app)


@app.route('/', methods=['get'])
@register_breadcrumb(app, '.', 'Groovin')
def index():
    return redirect(url_for('events'))


@app.route('/events', methods=['get'])
@login_required
@register_breadcrumb(app, '.events', 'Os Meus Eventos')
def events():
    return render_template('events/index.html')


@app.route('/events/<int:event_id>', methods=['get'])
@login_required
@register_breadcrumb(app, '.events.details', '',
                     dynamic_list_constructor=view_event_dlc)
def event(event_id):
    return render_template('events/details.html', event=get_event(event_id=event_id))


@db.atomic
@app.route('/events/new', methods=['get', 'post'])
@login_required
@register_breadcrumb(app, '.events.new_event', 'Novo')
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        if is_valid_date_time(form.date_time.data):
            event = create_event(name=form.name.data, category=form.category.data, date_time=form.date_time.data,
                                 address=form.address.data, description=form.description.data, image_url=upload_photo(form.image.data))

            flash('Evento criado com sucesso', 'success')
            return redirect(url_for('index'))
        else:
            form.date_time.errors.append(
                'A data informada é superior a data actual.')
    return render_template('events/form.html', form=form, title='Novo evento', action='Criar')


@db.atomic
@app.route('/events/<int:event_id>/edit', methods=['get', 'post'])
@login_required
@register_breadcrumb(app, '.events.details.edit', 'Editar')
def edit_event(event_id):
    event = get_event(event_id=event_id)
    form = EventForm(obj=event)

    if form.validate_on_submit():
        if is_valid_date_time(form.date_time.data):
            update_event(event, form.data)
            flash('Evento actualizado com sucesso', 'success')
            return redirect(url_for('index'))
        else:
            form.date_time.errors.append(
                'A data informada é superior a data actual.')

    return render_template('events/form.html', form=form, title='Editar evento', action='Editar')


@app.route('/events/<int:event_id>/delete', methods=['post'])
@login_required
def delete_event(event_id):
    remove_event(get_event(event_id=event_id))
    flash('Evento removido com sucesso', 'success')
    return redirect(url_for('index'))


@db.atomic
@app.route('/events/<int:event_id>/tickets/new', methods=['get', 'post'])
@login_required
@register_breadcrumb(app, '.events.details.tickets', 'Novo Bilhete')
def new_ticket(event_id):
    event = get_event(event_id=event_id)
    form = TicketForm()
    if form.validate_on_submit():
        if ticket_already_added(event, form.kind.data):
            form.kind.errors.append(
                'O bilhete {} já foi adicionado'.format(form.kind.data))
        else:
            create_ticket(event=event.id, name=form.kind.data,
                          price=form.price.data, total=form.total.data)
            flash('Bilhete criado com sucesso', 'success')
            return redirect(url_for('event', event_id=event.id))

    return render_template('tickets/form.html', form=form, title='Novo bolhete', action='Criar')


@app.errorhandler(404)
def not_found(e):
    resp = jsonify(dict(error="Not Found"))
    resp.status_code = 404
    return resp


@login_manager.user_loader
def load_user(promoter_id):
    return get_promoter(promoter_id)


@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        promoter = check_promoter(
            email=form.email.data, password=form.password.data)

        if promoter is None:
            flash('Email e senha não combinam.', 'danger')
        else:
            login_user(promoter)
            flash('Entrou como {}.'.format(promoter.name), 'success')

            fwd = request.args.get('next')
            if fwd:
                return redirect(fwd)
            return redirect(url_for('index'))

    return render_template('accounts/login.html', form=form)


@app.route('/logout', methods=['get'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
