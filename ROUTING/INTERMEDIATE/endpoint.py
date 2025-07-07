@app.route('/profile/<username>', endpoint='profile_page')
def profile(username):
    return f'Profile: {username}'
