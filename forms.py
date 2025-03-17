from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Ingat Saya')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Konfirmasi Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Daftar')

class ChapterForm(FlaskForm):
    title = StringField('Judul', validators=[DataRequired()])
    description = TextAreaField('Deskripsi')
    order = IntegerField('Urutan', validators=[DataRequired()])
    is_pro = BooleanField('Konten Pro')
    submit = SubmitField('Simpan')

class SubChapterForm(FlaskForm):
    title = StringField('Judul', validators=[DataRequired()])
    content = TextAreaField('Konten')
    order = IntegerField('Urutan', validators=[DataRequired()])
    is_pro = BooleanField('Konten Pro')
    submit = SubmitField('Simpan')

class PaymentForm(FlaskForm):
    submit = SubmitField('Bayar Sekarang') 