from ast import Return
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Database(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(600), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


#https://stackoverflow.com/questions/44941757/sqlalchemy-exc-operationalerror-sqlite3-operationalerror-no-such-table/44944205
@app.before_first_request
def create_tables():
    db.create_all()

    

@app.route('/', methods=['GET','POST'])
def hello_world():
  if request.method=='POST':
    title=request.form["title"]
    desc=request.form["desc"]
    todo = Database(title=title, desc=desc)
    db.session.add(todo)
    db.session.commit()
  allToDo = Database.query.all()
  return render_template("index.html", allToDo=allToDo)

@app.route('/delete/<int:sno>')
def delete(sno):
  allToDo = Database.query.filter_by(sno=sno).first()
  db.session.delete(allToDo)
  db.session.commit()
  return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
  if request.method=="POST":
    title=request.form["title"]
    desc=request.form["desc"]
    todo = Database.query.filter_by(sno=sno).first()
    todo.title = title
    todo.desc = desc
    db.session.add(todo)
    db.session.commit()
    return redirect('/')

  todo = Database.query.filter_by(sno=sno).first()
  return render_template('update.html', todo=todo)

@app.route('/about')
def about():
  return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)