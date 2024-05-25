import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from forms import PostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def init_db():
    with sqlite3.connect('blog.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS posts
                        (id INTEGER PRIMARY KEY,
                         title TEXT NOT NULL,
                         content TEXT NOT NULL,
                         date_created DATETIME DEFAULT CURRENT_TIMESTAMP)''')

init_db()

@app.route('/')
def index():
    with sqlite3.connect('blog.db') as conn:
        posts = conn.execute('SELECT id, title FROM posts').fetchall() 
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    with sqlite3.connect('blog.db') as conn:
        post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    return render_template('post_detail.html', post=post)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        with sqlite3.connect('blog.db') as conn:
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('new_post.html', form=form)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm()
    with sqlite3.connect('blog.db') as conn:
        post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
        if request.method == 'GET':
            form.title.data = post[1]
            form.content.data = post[2]
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
            conn.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('index'))
    return render_template('edit_post.html', form=form, post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    with sqlite3.connect('blog.db') as conn:
        conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
