from flask import Flask, render_template, request, redirect, url_for, flash, send_file ,send_from_directory
from captcha.image import ImageCaptcha
import random,string
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/publichub',methods=['POST'])
def publichub():
    if request.method=='POST':
        return render_template("public.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        if check_credentials(username, password):
            return render_template("publichub.html")
        else:
            flash("username or passwords is wrong")
    return render_template("login.html")

def check_credentials(username, password):
    with open('H:/pywebtest/credentials.txt', 'r') as f:
        for line in f:
            if ':' in line:
                user, pwd = line.strip().split(':')
                if user == username and pwd == password:
                    return True
    return False

@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        doublepassword = request.form['doublepassword']
        two_passwords=check_two_passwords(password,doublepassword)
        if two_passwords:

            if check_appearance(username):
                with open('H:/pywebtest/credentials.txt','a') as f:
                    f.write(str(username+':'+password+'\n'))
                return redirect(url_for('login'))
            else:
                flash("username exist, please change your username")
                return render_template("signin.html")
        else:
            flash("please enter the same passwords again")
        return render_template("signin.html")
    return render_template("signin.html")

def check_two_passwords(password,doublepassword):
    if password==doublepassword:
        return True
    return False

def check_appearance(username):
    with open('./credentials.txt','r') as f:
        for line in f:
            if ':' in line:
                user,pwd = line.strip().split(':')
                if user == username:
                    return False
    return True

@app.route('/public',methods=['GET','POST'])
def public():
    if request.method=='POST':
        return render_template('public.html')
    else:
        flash("please login first!")
    return redirect(url_for('login'))

@app.route('/reset',methods=['GET','POST'])
def reset():
    if request.method=='POST':
        wdcheck = request.form['passwords']
        if check_imgtxt(wdcheck):
            username = request.form['username']
            password = request.form['password']
            newpassword = request.form['newpassword']
            doublepassword = request.form['doublepassword']
            two_passwords=check_two_passwords(newpassword,doublepassword)
            if two_passwords:
                if not check_appearance(username):
                    if check_credentials(username, password):
                        with open('./credentials.txt','r') as f:
                            file_data=""
                            for line in f:
                                if username in line:
                                    line = line.replace(password,newpassword)
                                file_data += line
                        with open('./credentials.txt',"w") as f:
                            f.write(file_data)
                        flash("successfully reset the password,please login again")
                        return redirect(url_for('login'))
                    else:
                        flash("old-password is wrong, please enter again")
                        return render_template("reset.html")
                else:
                    flash("username not exist, please re-enter your username")
                    return render_template("reset.html")
            else:
                flash("please enter the same new passwords again")
            return render_template("reset.html")
        else:
            flash("图片验证码错误")
    return render_template("reset.html")

def check_imgtxt(wdcheck):
    with open('./static/txtcheck.txt', 'r') as f:
        for line in f:
                psw=line.strip()
                if wdcheck==psw:
                    return True
    return False

@app.route('/imgcheck.jpg',methods=['GET','POST'])
def randomimg():
    chr_all = string.ascii_letters + string.digits
    chr_4 = ''.join(random.sample(chr_all, 4))
    image = ImageCaptcha().generate_image(chr_4)
    image.save('./static/imgcheck.jpg')
    with open('./static/txtcheck.txt','w') as f:
        f.write(str(chr_4))
    return send_from_directory(os.path.join('static'),'imgcheck.jpg')

@app.errorhandler(404)
def not_found(e):
        return render_template("404.html")

@app.route('/users/<user_id>')
def users(user_id):
    if int(user_id)==1:
        return render_template("home.html")
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)