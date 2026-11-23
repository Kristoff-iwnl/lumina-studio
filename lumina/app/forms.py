"""
WTForms for enquiry, login, and admin CRUD operations.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from app.models import Admin

class LoginForm(FlaskForm):
    """Admin login form."""
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")

class EnquiryForm(FlaskForm):
    """Customer enquiry form."""
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField("Email", validators=[Optional(), Email()])
    phone = StringField("Phone", validators=[Optional(), Length(min=10)])
    service = SelectField("Service", coerce=str, validators=[Optional()], choices=[])
    preferred_date = StringField("Preferred Date", validators=[Optional()])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=10, max=2000)])
    submit = SubmitField("Send Inquiry")

    def __init__(self, *args, **kwargs):
        """Populate service choices dynamically."""
        super().__init__(*args, **kwargs)
        from app.models import Service
        self.service.choices = [("", "— Select a service —")] + [
            (str(s.id), s.name) for s in Service.query.all()
        ]

    def validate_contact(self):
        """Ensure at least email or phone is provided."""
        if not self.email.data and not self.phone.data:
            raise ValidationError("Please provide either an email or phone number.")

class ServiceForm(FlaskForm):
    """Service CRUD form."""
    name = StringField("Service Name", validators=[DataRequired(), Length(min=3, max=120)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=10)])
    price = StringField("Price", validators=[DataRequired(), Length(max=50)])
    icon = StringField("Icon", validators=[Optional()])
    submit = SubmitField("Save Service")

class FAQForm(FlaskForm):
    """FAQ CRUD form."""
    question = StringField("Question", validators=[DataRequired(), Length(min=5, max=255)])
    answer = TextAreaField("Answer", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Save FAQ")

class TestimonialForm(FlaskForm):
    """Testimonial CRUD form."""
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    role = StringField("Role/Title", validators=[DataRequired(), Length(min=2, max=120)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=10)])
    approved = BooleanField("Approved")
    submit = SubmitField("Save Testimonial")

class SettingsForm(FlaskForm):
    """Site settings form."""
    submit = SubmitField("Save Settings")
