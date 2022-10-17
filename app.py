# importing flask module fro
from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import requests  # for API example
import urllib.parse  # for API example

mysql = MySQL()

# initializing a variable of Flask
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Example'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# decorating index function with the app.route with url as /login
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/enternew')
def new_user():
    return render_template('new.html')


@app.route('/view')
def view_user():
    return render_template('search.html')


@app.route('/updatenew')
def update_user():
    return render_template('update.html')


@app.route('/remove')
def remove_user():
    return render_template('remove.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    date_time = ""
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['pass']

            # API for date and time ---------------------------------------------------------------------------
            url = "http://worldtimeapi.org/api/timezone/Europe/London"
            response = requests.get(url).json()
            print("" + str(response))  # response details
            date_time = response["datetime"]  # retrieve response details form the attribute, datetime
            # -------------------------------------------------------------------------------------------------

            con = mysql.connect()
            cur = con.cursor()

            cur.execute('INSERT INTO user (username, email, password)VALUES( %s,  %s, %s)',
                        (username, email, password))

            con.commit()
            msg = "You have signed up today (UK Time)"

        except:
            con.rollback()
            msg = "The sign up operation failed."

        finally:
            # return render_template("result.html", msg=msg, date_time=date_time)
            return render_template("result.html", msg=msg, date_time=date_time)
            con.close()


@app.route('/viewrec', methods=['POST', 'GET'])
def viewrec():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['pass']
            con = mysql.connect()
            cur = con.cursor()
            cur.execute('SELECT username, email FROM User WHERE username=%s AND password=%s',
                        (username, password))
            rows = cur.fetchall()
            con.commit()

        except:
            con.rollback()

        finally:
            return render_template("view.html", rows=rows)
            con.close()


@app.route('/randomrec')
def view_random():
    return render_template('randomr.html')

@app.route('/specific')
def view_specific():
    return render_template('spec.html')

@app.route('/location')
def view_location():
    return render_template('loc.html')

@app.route('/updaterec', methods=['POST', 'GET'])
def updaterec():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['pass']
            email = request.form['email']

            con = mysql.connect()
            cur = con.cursor()
            cur.execute('UPDATE User SET email=%s WHERE username=%s AND password=%s',
                        (email, username, password))
            con.commit()

            cur.execute('SELECT username, email FROM User WHERE username=%s', username)
            rows = cur.fetchall()
            con.commit()

        except:
            con.rollback()

        finally:
            return render_template("view.html", rows=rows)
            con.close()


@app.route('/removerec', methods=['POST', 'GET'])
def removerec():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['pass']
            con = mysql.connect()
            cur = con.cursor()
            cur.execute('DELETE FROM User WHERE username=%s AND password=%s',
                        (username, password))
            con.commit()

            cur.execute('SELECT username, email FROM User WHERE username=%s', username)
            rows = cur.fetchall()
            con.commit()

        except:
            con.rollback()

        finally:
            return render_template("view.html", rows=rows)
            con.close()


if __name__ == "__main__":
    app.run()
