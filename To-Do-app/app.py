from http.cookiejar import debug
from tkinter.messagebox import RETRY

from  flask import *

app = Flask(__name__)
tasks = []

@app.route('/')
def index():
    return render_template("index.html",tasks = tasks)


@app.route("/add",methods  = ['POST'])

def add_task():
    new_task = request.form.get("task")
    tasks.append(new_task)

    return redirect(url_for("index"))
@app.route("/delete/<int:task_id>")

def delete_task(task_id):
    if 0<=task_id and task_id <len(tasks):
        tasks.pop(task_id)

    return redirect(url_for("index"))

if __name__ =="__main__":
    app.run(debug = True)
