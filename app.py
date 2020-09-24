from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, Required
from flask_uploads import configure_uploads, UploadSet, patch_request_class
import os
import score

curr_path = os.path.abspath(os.path.dirname(__file__))

if not os.path.exists(os.path.join(curr_path, 'temp/')):
    os.makedirs(os.path.join(curr_path, 'temp/'))

app = Flask(__name__)
app.secret_key = 'development key'
app.config['UPLOADED_RESUME_DEST'] = os.path.join(curr_path, 'temp/')

DOCUMENTS = ('txt', 'pdf', 'docx', 'doc')
resumes = UploadSet('resume', DOCUMENTS)
configure_uploads(app, resumes)
patch_request_class(app)


class MyForm(FlaskForm):
    resume = FileField('resume', validators=[FileAllowed(resumes, "Only PDF, TXT, DOC, DOCX Files Allowed"),
                                             Required("Resume is Required")])
    description = TextAreaField('description', validators=[InputRequired("Job Description is required")])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        filename = resumes.save(form.resume.data)
        return "<h1>" + score.main(filename, form.description.data) + "</h1>"
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=False)
