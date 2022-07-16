from flask import *

app=Flask(__name__)
@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method=="POST":
        uname=request.form['uname']
        password=request.form['pass']
        if uname=="Ranjan" and password=="Ranjan":
            return  render_template("welcome.html", user=uname)
        else:
            return "<h3 style=color:red> invalid user</h3>"
    else:
        return render_template("login.html")
def home():
    return "hello man"
app.add_url_rule("/h","/h",home)
@app.route('/table/<int:num>')  
def ob(num):  
    return render_template("print-table.html",n=num)
if __name__=='__main__':
    app.run(debug=True)
