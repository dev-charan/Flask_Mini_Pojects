from flask import Flask

app = Flask(__name__)

@app.route('/about/<id>')
def home(id):
    return f'got the id{id}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post number: {post_id}'

if __name__ == '__main__':
    app.run(debug=True)
