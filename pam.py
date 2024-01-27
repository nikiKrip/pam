from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='"C:\\Users\\nikia\\Desktop\\Templates"')

class PrivilegedAccount:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def change_password(self, new_password):
        if self.is_admin:
            self.password = new_password
            return True
        else:
            return False

# Dummy data for user accounts
admin_account = PrivilegedAccount(username="admin", password="adminpass", is_admin=True)
regular_user_account = PrivilegedAccount(username="user", password="userpass")

# Session variable to keep track of the logged-in user
current_user = None

@app.route('/')
def home():
    return render_template('index.html', current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match any of the accounts
        if admin_account.username == username and admin_account.password == password:
            current_user = admin_account
        elif regular_user_account.username == username and regular_user_account.password == password:
            current_user = regular_user_account

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect(url_for('home'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        new_password = request.form['new_password']

        # Change the password for the logged-in user
        if current_user and current_user.change_password(new_password):
            return render_template('change_password.html', success=True)
        else:
            return render_template('change_password.html', success=False)

    return render_template('change_password.html', success=None)

if __name__ == '__main__':
    app.run(debug=True)



