import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Event, Receipt, Comment, User
from .forms import BookEventForm, AddCommentForm, AddEventForm, EditEventForm
import os

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def homePage():
    # find event list with types (if provided)
    list = db.session.query(Event)
    if request.args.get('type') is not None:
        list = list.filter(Event.type == request.args.get('type'))

    return render_template(
        'home.html',
        list=list,
        type=request.args.get('type'),
        user=current_user
    )


@bp.route('/eventDetail', methods=['GET', 'POST'])
def eventDetail():
    # find event detail by id
    eventDetail = Event.query.filter_by(id=request.args.get('id')).first()
    if eventDetail is None:
        return render_template('404.html', user=current_user)

    return render_template(
        'event.html',
        data=eventDetail,
        comments=db.session.query(Comment.content, Comment.created, User.name).join(User).filter(
            Comment.event == request.args.get('id')),
        user=current_user,
        datetime=datetime
    )


@bp.route('/bookEvent', methods=['GET', 'POST'])
@login_required
def bookEvent():
    form = BookEventForm()
    error = None
    # validate book form
    if form.validate_on_submit():
        ticket_number = int(request.form.get('ticket_number'))
        # find booked event detail
        eventDetail = Event.query.filter_by(id=request.args.get('id')).first()
        if eventDetail is None:
            # not found
            error = 'Event not found'
        elif eventDetail.ticket_all - eventDetail.ticket_sold < ticket_number:
            # ticket not enough
            error = 'ticket is not enough!'
        if error is not None:
            flash(error)
        else:
            # update event status
            newStatus = "Booked out" if eventDetail.ticket_sold + ticket_number == eventDetail.ticket_all else "Upcoming"
            db.session.query(Event).filter(Event.id == request.args.get('id')).update({
                "ticket_sold": eventDetail.ticket_sold + ticket_number,
                "status": newStatus
            })

            # create new receipt
            receipt = Receipt(
                ticket_number=ticket_number,
                event=request.args.get('id'),
                created_user=current_user.email
            )
            # insert receipt
            db.session.add(receipt)
            db.session.commit()

            return render_template(
                'receipt.html',
                data=receipt,
                event=eventDetail
            )
    return render_template(
        'renderforms.html',
        form=form,
        formTitle='Book Event',
        user=current_user
    )


@bp.route('/addComment', methods=['GET', 'POST'])
@login_required
def addComment():
    form = AddCommentForm()
    if form.validate_on_submit():
        # add comment
        db.session.add(Comment(
            content=request.form.get('content'),
            event=request.args.get('id'),
            created_user=current_user.email
        ))
        db.session.commit()
        return redirect(url_for('main.eventDetail') + "?id=" + request.args.get('id'))
    return render_template('renderforms.html', form=form, formTitle='Add Comment', user=current_user)


@bp.route('/addEvent', methods=['GET', 'POST'])
@login_required
def addEvent():
    form = AddEventForm()
    # validate event form
    if form.validate_on_submit():
        file = secure_filename(form.image_path.data.filename)
        # create new = event
        eventDetail = Event(
            image_path=file,
            title=request.form.get('title'),
            type=request.form.get('type'),
            desc=request.form.get('desc'),
            status=request.form.get('status'),
            date=datetime.datetime.strptime(request.form.get('date'), "%Y-%m-%d %H:%M:%S"),
            ticket_price=float(request.form.get('ticket_price')),
            ticket_all=int(request.form.get('ticket_all')),
            created=current_user.email
        )
        form.image_path.data.save(os.path.dirname(__file__) + '/static/img/' + file)
        # insert
        db.session.add(eventDetail)
        db.session.commit()

        return redirect(url_for('main.eventDetail') + "?id=" + str(eventDetail.id))
    return render_template('renderforms.html', form=form, formTitle='Add Event', user=current_user)


@bp.route('/updateEvent', methods=['GET', 'POST'])
@login_required
def updateEvent():
    eventDetail = Event.query.filter_by(id=request.args.get('id')).first()
    if eventDetail is None:
        return render_template('404.html', user=current_user)

    form = EditEventForm(eventDetail)
    # validate event form
    if form.validate_on_submit():
        # create updated event
        updated = {
            "type": request.form.get('type'),
            "title": request.form.get('title'),
            "desc": request.form.get('desc'),
            "status": request.form.get('status'),
            "date": datetime.datetime.strptime(request.form.get('date'), "%Y-%m-%d %H:%M:%S"),
            "ticket_price": float(request.form.get('ticket_price')),
            "ticket_all": int(request.form.get('ticket_all')),
            "image_path": eventDetail.image_path,
        }
        if form.image_path.data.filename != '':
            updated['image_path'] = secure_filename(form.image_path.data.filename)
            form.image_path.data.save(os.path.dirname(__file__) + '/static/img/' + updated['image_path'])
        # update into db
        db.session.query(Event).filter(Event.id == request.args.get('id')).update(updated)
        db.session.commit()
        return redirect(url_for('main.eventDetail') + "?id=" + request.args.get('id'))
    return render_template('renderforms.html', form=form, formTitle='Update Event', user=current_user)


@bp.route('/deleteEvent', methods=['GET', 'POST'])
@login_required
def deleteEvent():
    # delete event by id
    Event.query.filter_by(id=request.args.get('id')).delete()
    db.session.commit()
    return redirect(url_for('main.homePage'))
