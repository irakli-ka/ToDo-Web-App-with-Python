from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="Undone", nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def first_page():
    return render_template("index.html")


@app.route('/todos', methods=["GET", "POST"])
def todo_page():
    todos = db.session.execute(db.select(Todo).order_by(Todo.status)).scalars().all()
    return render_template('todos.html', todos=todos)


@app.route('/todos/add', methods=["POST", "GET"])
def add():
    if request.method == "POST":
        todo = Todo(description=request.form["description"])
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("todo_page"))
    return render_template("add.html")


@app.route('/todos/edit/<int:todo_id>', methods=['POST', 'GET'])
def edit_todo(todo_id):
    todo_desc = db.session.execute(db.select(Todo.description).where(Todo.id == todo_id)).scalars().all()[0]
    if request.method == "POST":
        todo = db.get_or_404(Todo, todo_id)
        todo.description = request.form["edit"]
        db.session.commit()
        return redirect(url_for("todo_page"))
    else:
        return render_template('edit.html', todo_id=todo_id, todo_desc=todo_desc)


@app.route("/todos/<int:todo_id>/delete", methods=["POST", "GET"])
def delete_todo(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    if request.method == "POST":
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("todo_page"))
    return redirect(url_for("todo_page"))


@app.route('/todos/mark-done/<int:todo_id>', methods=['POST'])
def mark_done(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    todo.status = "Done"
    db.session.commit()
    return redirect(url_for("todo_page"))


@app.route('/todos/mark-undone/<int:todo_id>', methods=['POST'])
def mark_undone(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    todo.status = "Undone"
    db.session.commit()
    return redirect(url_for("todo_page"))


if __name__ == '__main__':
    app.run()
