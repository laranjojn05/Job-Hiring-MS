from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from forms import JobForm, ApplyForm
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

db = SQLAlchemy(app)

# Models
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    resume_filename = db.Column(db.String(100), nullable=False)

# Routes
@app.route('/')
def index():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    form = JobForm()
    if form.validate_on_submit():
        new_job = Job(title=form.title.data, description=form.description.data)
        db.session.add(new_job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('post_job.html', form=form)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    form = ApplyForm()
    if form.validate_on_submit():
        resume = form.resume.data
        resume.save(os.path.join(app.config['UPLOAD_FOLDER'], resume.filename))
        new_application = Application(job_id=job_id, resume_filename=resume.filename)
        db.session.add(new_application)
        db.session.commit()
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('apply_job.html', form=form)

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()  
    app.run(debug=True)