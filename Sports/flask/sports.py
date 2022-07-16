import json
from django.shortcuts import render
from flask import Flask, request, jsonify,render_template
from flask.scaffold import F
from flask_mongoengine import MongoEngine
import requests 
app = Flask(__name__)

DB_URI = "mongodb+srv://madhubm:8861122380@cluster0.qxgty.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine()
db.init_app(app)


 
class sports(db.Document):
    s_usn = db.StringField()
    s_name = db.StringField()
    s_equipment = db.StringField()
    s_quantity=db.IntField()
    s_department=db.StringField()
    s_taken=db.StringField()
    s_return=db.StringField()
    s_costrent=db.IntField()
    def to_json(self):
        return {"s_usn": self.s_usn,
                "s_name": self.s_name,
                "s_equipment":self.s_equipment,
                "s_quantity":self.s_quantity,
                "s_department":self.s_department,
                "s_taken":self.s_taken,
                "s_return":self.s_return,
                "s_costrent":self.s_costrent}
 

   
@app.route('/',methods=["GET"])
def query_records():
    s_usn = request.args.get('s_usn')
    if(s_usn is None):
    
        s_taken=request.args.get('s_taken')
        if(s_taken is None):
            c = sports.objects()
        else:
            c = sports.objects(s_taken=s_taken)
    else:
        c = sports.objects(s_usn=s_usn)

    
    if not c:
        return render_template("front.html")
    else:
        return jsonify(c.to_json())

 


@app.route('/', methods=['POST'])
def create_record():
   
    record = json.loads(request.data)
    c = sports( 
                s_usn=record['s_usn'],
                s_name=record['s_name'],
                s_equipment=record['s_equipment'],
                s_quantity=record['s_quantity'],
                s_department=record['s_department'],
                s_taken=record['s_taken'],
                s_return=record['s_return'],
                s_costrent=record['s_costrent'],
                )
    c.save()
    #return jsonify(c.to_json)
    return render_template("add.html",success=200)
 
@app.route('/', methods=['PUT'])
def update_record():
    record = json.loads(request.data)
    c = sports.objects(s_usn=record['s_usn']).first()
    if not c:
        return jsonify({'error': 'data not found'})
    else:
        c.update(s_name=record['s_name'])
        c.update(s_department=record['s_department'])
        c.update(s_equipment=record['s_equipment'])
        c.update(s_quantity=record['s_quantity'])
        c.update(s_taken=record['s_taken'])
        c.update(s_return=record['s_return'])
        c.update(s_costrent=record['s_costrent'])
    c = sports.objects(s_usn=record['s_usn']).first()
    return render_template("update.html")
 
@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    c = sports.objects(s_usn=record['s_usn']).first()
    if not c:
        return "M"
    else:
        c.delete()
        return "None"
 
@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=="GET":
        return render_template("add.html")
    else:
        x={
    
        "s_usn":request.form['s_usn'],
        "s_name":request.form['s_name'],
        "s_equipment":request.form['s_equipment'],
        "s_quantity":request.form['s_quantity'],
        "s_department":request.form['s_department'],
        "s_taken":request.form['s_taken'],
        "s_return":request.form['s_return'],
        "s_costrent":request.form['s_costrent'],
        }
        x=json.dumps(x)
        response = requests.post(url="http://127.0.0.1:5000/",data=x)
        return response.text
 
@app.route('/find',methods=['GET','POST'])
def find():
    if request.method=="GET":
        return render_template("find.html",r=0)
    else:
        s_usn=request.form['s_usn']
        response = requests.get(url="http://127.0.0.1:5000/",params={"s_usn":s_usn})
        #print(response.json)
        try:
            loaded_json = json.loads(response.json())
            return render_template("find.html",r=100,result=loaded_json)
            
        except:
            return render_template("find.html",r=200,error="No such records related to given ID")

       
        
@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method=="GET":
        return render_template("del.html",show=100)
    else:
        x={
        "s_usn":request.form['s_usn'],
        }
        x=json.dumps(x)
        response = requests.delete(url="http://127.0.0.1:5000/",data=x)
        if(response.text=="None"):
            return render_template("del.html",show=200)
        else:
            return render_template("del.html",show=300)

@app.route('/home',methods=['GET'])
def home():
    return render_template("front.html")
 
@app.route('/update',methods=['GET','POST'])
def update():
    if request.method=="GET":
        return render_template("update.html")
    else:
        x={
          "s_usn":request.form['s_usn'],
        "s_name":request.form['s_name'],
        "s_equipment":request.form['s_equipment'],
        "s_quantity":request.form['s_quantity'],
        "s_department":request.form['s_department'],
        "s_taken":request.form['s_taken'],
        "s_return":request.form['s_return'],
        "s_costrent":request.form['s_costrent'],
        }
        x=json.dumps(x)
        response = requests.put(url="http://127.0.0.1:5000/",data=x)
        return response.text

@app.route('/record',methods=['GET','POST'])
def record():
    if request.method=="GET":
        return render_template("record.html",r=0)
    else:
        s_taken=request.form['s_taken']
        response = requests.get(url="http://127.0.0.1:5000/",params={"s_taken":s_taken})
         #print(response.json)
        try:
            loaded_json = json.loads(response.json())
            return render_template("record.html",r=400,result=loaded_json)
            
        except:
            return render_template("record.html",r=300,error="No such records related to given ID")

@app.route('/recordall')
def recordall():
    
    response = requests.get(url="http://127.0.0.1:5000/",params={"s_taken":None})
         
    
    loaded_json = json.loads(response.json())
    return render_template("record.html",r=400,result=loaded_json)
            
    
if __name__ == "__main__":
    app.run(debug=True)

