from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")

todos = [{"task": "Sample Todo", "done": False, "priority":"low"}]


priority_colors = {
    "low": "green",
    "medium": "yellow",
    "high": "red"
}

@app.route("/")
def index():
    return render_template("index.html", todos=todos, priority_colors=priority_colors)


@app.route("/add", methods=["POST"])
def add():
    todo = request.form['todo']
    priority = request.form['priority']
    todos.append({"task": todo, "done": False, "priority": priority, "color": priority_colors[priority]})
    return redirect(url_for("index"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    todo = todos[index]
    if request.method == "POST":
        old_priority = todo['priority']
        todo['task'] = request.form["todo"]
        todo['priority'] = request.form["priority"]
        if old_priority != todo['priority']:
            # If priority has changed, update the color
            todo['color'] = priority_colors[todo['priority']]
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo, index=index)


@app.route("/check/<int:index>")
def check(index):
    todos[index]['done'] = not todos[index]['done']
    return redirect(url_for("index"))



@app.route("/delete/<int:index>")
def delete(index):
    del todos[index]
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)