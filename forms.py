from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField, IntegerField, FloatField, DateTimeField, FileField, \
    SelectField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange
import datetime


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email("email is not valid")])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login!")


class RegisterForm(FlaskForm):
    email = StringField("Email",
                        validators=[
                            InputRequired(),
                            Email("email is not valid")
                        ])
    name = StringField("Name",
                       validators=[
                           InputRequired()
                       ])
    password = PasswordField("Password",
                             validators=[
                                 InputRequired(),
                                 EqualTo('confirm', message="Passwords not match")
                             ])
    confirm = PasswordField("ConfirmPassword",
                            validators=[
                                InputRequired()
                            ])
    contact = StringField("Contact Number",
                          validators=[
                              InputRequired()
                          ])
    address = StringField("Address",
                          validators=[
                              InputRequired()
                          ])
    submit = SubmitField("Signup Now!")


class BookEventForm(FlaskForm):
    ticket_number = IntegerField("Ticket Number", validators=[NumberRange(min=1)], default=1)
    submit = SubmitField("Place Order")


class AddCommentForm(FlaskForm):
    content = StringField("Content", validators=[InputRequired()])
    submit = SubmitField("Post Comment")


class AddEventForm(FlaskForm):
    status = SelectField('Event Status', validators=[InputRequired()],
                         choices=[
                             ('Upcoming', 'Upcoming'),
                             ('Inactive', 'Inactive'),
                             ('Cancelled', 'Cancelled'),
                             ('Booked out', 'Booked out')
                         ])
    type = SelectField('Event Type', validators=[InputRequired()],
                       choices=[
                           ('Pop', 'Pop'),
                           ('Jazz', 'Jazz'),
                           ('Sport', 'Sport'),
                           ('R&B', 'R&B'),
                           ('Country', 'Country')
                       ])
    title = StringField("Event Title", validators=[InputRequired()])
    desc = StringField("Event Description", validators=[InputRequired()])
    ticket_price = FloatField("Event Ticket Price", validators=[InputRequired(), NumberRange(min=0)])
    ticket_all = IntegerField("Event Ticket Number", validators=[InputRequired(), NumberRange(min=0)])
    date = DateTimeField('Event starts at', validators=[InputRequired()], format="%Y-%m-%d %H:%M:%S",
                         default=datetime.datetime.now)
    image_path = FileField("Event Image", validators=[InputRequired()])
    submit = SubmitField("Submit")


class EditEventForm(AddEventForm):
    def __init__(self, data, *args, **kwargs):
        super(AddEventForm, self).__init__(*args, **kwargs)
        self.title.data = data.title
        self.desc.data = data.desc
        self.ticket_price.data = data.ticket_price
        self.ticket_all.data = data.ticket_all
        self.date.data = data.date
        self.type.data = data.type
        self.status.data = data.status

    image_path = FileField("Event Image")
    submit = SubmitField("Submit")
