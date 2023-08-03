from flask_wtf import FlaskForm
from my_app.models import Users
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FileField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError

ALPHABET = {1: "الف", 2: "ب", 3: "پ", 4: "ت", 5: "ث", 6: "ج", 7: "چ", 8: "ح", 9: "خ", 10: "د", 11: "ذ", 12: "ر",
            13: "ز", 14: "ژ", 15: "س", 16: "ش", 17: "ص", 18: "ض", 19: "ط", 20: "ظ", 21: "ع", 22: "غ", 23: "ف", 24: "ق",
            25: "ک", 26: "گ", 27: "ل", 28: "م", 29: "ن", 30: "و", 31: "ه", 32: "ی", }



class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = Users.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exist, please choose another username.")

    def validate_phone_email(self, phone_email_to_check):
        user = Users.query.filter_by(phone_email=phone_email_to_check.data).first()
        if user:
            raise ValidationError("phone number or email already exist, please choose another phone.")

    name = StringField(label='نام کاربری', validators=[Length(min=1, max=50), DataRequired()])
    username = StringField(label='نام کاربری', validators=[Length(min=2, max=50), DataRequired()])
    phone_email = StringField(label='ایمیل یا شماره همراه', validators=[Length(min=2, max=50), DataRequired()])
    password_hash = PasswordField(label='رمز', validators=[DataRequired(),
                                                           EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField(label='تکرار رسم', validators=[DataRequired()])
    submit = SubmitField(label='ثبت نام')


class LoginForm(FlaskForm):
    username = StringField(label='نام کاربری', validators=[Length(min=2, max=50), DataRequired()])
    password = PasswordField(label='رمز', validators=[Length(min=1), DataRequired()])
    submit = SubmitField(label='ورود به اکانت')


class BeytForm(FlaskForm):
    mesra1 = StringField(label='مصراع اول', validators=[Length(min=2, max=80), DataRequired()])
    mesra2 = StringField(label='مصراع دوم', validators=[Length(min=2, max=80), DataRequired()])
    poet = StringField(label='شاعر', validators=[Length(min=2, max=50), DataRequired()])
    start = SelectField(u'حرف شروع', choices=ALPHABET_TUPLE_S)
    stop = SelectField(u'حرف پایانی', choices=ALPHABET_TUPLE_E)
    submit = SubmitField(label='ثبت بیت')


class PoemForm(FlaskForm):
    beyt1_1 = StringField(label='مصراع اول بیت اول', validators=[Length(min=5, max=80), DataRequired()])
    beyt1_2 = StringField(label='مصراع دوم بیت اول', validators=[Length(min=5, max=80), DataRequired()])
    beyt2_1 = StringField(label='مصراع اول بیت دوم', validators=[Length(min=5, max=80), DataRequired()])
    beyt2_2 = StringField(label='مصراع دوم بیت دوم', validators=[Length(min=5, max=80), DataRequired()])
    beyt3_1 = StringField(label='مصراع اول بیت سوم', validators=[Length(min=5, max=80)])
    beyt3_2 = StringField(label='مصراع دوم بیت سوم', validators=[Length(min=5, max=80)])
    beyt4_1 = StringField(label='مصراع اول بیت چهارم', validators=[Length(min=5, max=80)])
    beyt4_2 = StringField(label='مصراع دوم بیت چهازم', validators=[Length(min=5, max=80)])
    beyt5_1 = StringField(label='مصراع اول بیت پنجم', validators=[Length(min=5, max=80)])
    beyt5_2 = StringField(label='مصراع دوم بیت پنجم', validators=[Length(min=5, max=80)])
    beyt6_1 = StringField(label='مصراع اول بیت ششم', validators=[Length(min=5, max=80)])
    beyt6_2 = StringField(label='مصراع دوم بیت ششم', validators=[Length(min=5, max=80)])
    beyt7_1 = StringField(label='مصراع اول بیت هفتم', validators=[Length(min=5, max=80)])
    beyt7_2 = StringField(label='مصراع دوم بیت هفتم', validators=[Length(min=5, max=80)])
    beyt8_1 = StringField(label='مصراع اول بیت هشتم', validators=[Length(min=5, max=80)])
    beyt8_2 = StringField(label='مصراع دوم بیت هشتم', validators=[Length(min=5, max=80)])
    beyt9_1 = StringField(label='مصراع اول بیت نهم', validators=[Length(min=5, max=80)])
    beyt9_2 = StringField(label='مصراع دوم بیت نهم', validators=[Length(min=5, max=80)])
    beyt10_1 = StringField(label='مصراع اول بیت دهم', validators=[Length(min=5, max=80)])
    beyt10_2 = StringField(label='مصراع دوم بیت دهم', validators=[Length(min=5, max=80)])
    poet = StringField(label='شاعر', validators=[Length(max=50), DataRequired()])
    submit = SubmitField(label='ثبت شعر')


class SpeechForm(FlaskForm):
    speech = TextAreaField(label='سخن', validators=[Length(min=5, max=250), DataRequired()])
    wise = StringField(label='گوینده سخن', validators=[Length(min=2, max=50), DataRequired()])
    submit = SubmitField(label='ثبت سخن')


class StoryForm(FlaskForm):
    title = StringField(label="نام داستان", validators=[Length(min=2, max=80), DataRequired()])
    story = TextAreaField(label='داستان', validators=[Length(min=2, max=3000), DataRequired()])
    writer = StringField(label='نویسنده', validators=[Length(min=2, max=50), DataRequired()])
    submit = SubmitField(label='ثبت سخن')


class SearchBeytForm(FlaskForm):
    b_word = StringField(label='کلمه', default='')
    b_poet = StringField(label='شاهر', default='')
    b_start = SelectField(u'حرف شروع', choices=ALPHABET_TUPLE_S, default=0)
    b_stop = SelectField(u'حرف پایانی', choices=ALPHABET_TUPLE_E, default=0)
    b_submit = SubmitField(label='جستجوی بیت')


class SearchPoemForm(FlaskForm):
    p_word = StringField(label='کلمه', default='')
    p_poet = StringField(label='شاعر', default='')
    p_submit = SubmitField(label='جستجوی شعر')


class SearchSpeechForm(FlaskForm):
    sp_word = StringField(label='کلمه', default='')
    sp_wise = StringField(label='گوینده', default='')
    sp_submit = SubmitField(label='جستجوی سخن')


class SearchStoryForm(FlaskForm):
    st_title = StringField(label='نوسینده', default='')
    st_word = StringField(label='کلمه', default='')
    st_writer = StringField(label='نویسنده', default='')
    st_submit = SubmitField(label='جستجوی داستان')


class AddCommentForm(FlaskForm):
    comment = StringField(label='متن کامنت', validators=[Length(min=5, max=500), DataRequired()])
    submit = SubmitField(label='کامنت')


class UploadSound(FlaskForm):
    file = FileField(label="انتخاب صوت", validators=[DataRequired()])
    submit = SubmitField(label='اضافه کردن')
