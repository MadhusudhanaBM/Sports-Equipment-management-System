
from flask import *

app=Flask(__name__)

@app.route('/')
def stud():
    return render_template('studdet.html')

@app.route('/form',methods=['POST','GET'])
def form():
    if request.method=='POST':
        result=request.form
        return render_template('resultdata.html',result=result)


if __name__=='__main__':
    app.run(debug=True)
