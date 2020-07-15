from flask_login import login_required, login_user, logout_user
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from flask import (render_template, flash, redirect,
                   url_for, request, Blueprint)


from services.promoter import check_promoter
from services.ticket import create_ticket
from services.event import (create_event, get_event,
                            update_event, remove_event,)

from forms import LoginForm, EventForm, TicketForm
from models import db
from utils import (view_event_dlc, upload_photo, ticket_already_added,)


web = Blueprint('web', __name__, template_folder='templates', url_prefix='/')
default_breadcrumb_root(web, '.')


@web.route('/', methods=['get'])
@register_breadcrumb(web, '.', 'Groovin')
def index():
    return redirect(url_for('web.events'))


@web.route('/events', methods=['get'])
@login_required
@register_breadcrumb(web, '.events', 'Os Meus Eventos')
def events():
    return render_template('events/index.html')


@web.route('/events/<int:event_id>', methods=['get'])
@login_required
@register_breadcrumb(web, '.events.details', '',
                     dynamic_list_constructor=view_event_dlc)
def event(event_id):
    return render_template('events/details.html',
                           event=get_event(event_id=event_id))


@db.atomic
@web.route('/events/new', methods=['get', 'post'])
@login_required
@register_breadcrumb(web, '.events.new_event', 'Novo')
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        created, event = create_event(name=form.name.data,
                                      category=form.category.data,
                                      date_time=form.date_time.data,
                                      address=form.address.data,
                                      description=form.description.data,
                                      image_url=upload_photo(form.image.data))
        if created:
            flash('Evento criado com sucesso', 'success')
            return redirect(url_for('web.index'))
        else:
            flash(event, 'danger')
    return render_template('events/form.html',
                           form=form,
                           title='Novo evento',
                           action='Criar')


@db.atomic
@web.route('/events/<int:event_id>/edit', methods=['get', 'post'])
@login_required
@register_breadcrumb(web, '.events.details.edit', 'Editar')
def edit_event(event_id):
    event = get_event(event_id=event_id)
    form = EventForm(obj=event)

    if form.validate_on_submit():
        updated, error = update_event(event, form.data)
        if updated:
            flash('Evento atualizado com sucesso', 'success')
            return redirect(url_for('web.index'))
        else:
            flash(error, 'danger')

    return render_template('events/form.html',
                           form=form, title='Editar evento',
                           action='Editar')


@web.route('/events/<int:event_id>/delete', methods=['post'])
@login_required
def delete_event(event_id):
    remove_event(get_event(event_id=event_id))
    flash('Evento removido com sucesso', 'success')
    return redirect(url_for('web.index'))


@db.atomic
@web.route('/events/<int:event_id>/tickets/new', methods=['get', 'post'])
@login_required
@register_breadcrumb(web, '.events.details.tickets', 'Novo Bilhete')
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
            return redirect(url_for('web.event', event_id=event.id))

    return render_template('tickets/form.html',
                           form=form,
                           title='Novo bilhete',
                           action='Criar')


@web.route('/login', methods=['get', 'post'])
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
            return redirect(url_for('web.index'))

    return render_template('accounts/login.html', form=form)


@web.route('/logout', methods=['get'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))
