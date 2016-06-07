from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField,ValidationError
from wtforms.validators import Required,Length,Regexp,EqualTo
from ..models import User

class LoginForm(Form):
    username = StringField('用户名',validators=[Required(),Length(1,64)])
    password = PasswordField('密码',validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')

class RegistrationForm(Form):
    username = StringField('用户名',validators=[Required(),Length(1,64),
                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                  '用户名只能有字母，数字，点和下划线')])
    password = PasswordField('密码',validators=[Required(),EqualTo('password2','密码必须一样')])
    password2 = PasswordField('确认密码',validators=[Required()])
    submit = SubmitField('注册')

    def validtae_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')

