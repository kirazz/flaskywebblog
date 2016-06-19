from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import Required,Length
from flask.ext.pagedown.fields import PageDownField

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class EditProfiledForm(Form):
    name =StringField('真名',validators=[Length(0,64)])
    location = StringField('地址',validators=[Length(0,64)])
    about_me = TextAreaField('自身情况')
    submit = SubmitField('提交')

class PostForm(Form):
    body = PageDownField('写点什么吧',validators=[Required()])
    submit = SubmitField('提交')

class CommentForm(Form):
    body = PageDownField('',validators=[Required()])
    submit = SubmitField('提交')