from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from programKecil import *
from levenshteinDistance import *

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     matkul = db.Column(db.String(200), nullable=False)
     jenis = db.Column(db.String(200), nullable=False)
     topik = db.Column(db.String(200), nullable=False)
     deadline = db.Column(db.String, default = "2021-04-27")
     status = db.Column(db.Integer, default = 0)

     def __init__(self,matkul,jenis,topik,deadline,status):
          self.matkul = matkul
          self.jenis = jenis
          self.topik = topik
          self.deadline = deadline
          self.status = status
          

def todoToList(todo):
     todoList = [[] for i in range(len(todo))]
     for count, todoObject in enumerate(todo):
          todoList[count].append(str(todoObject.id))
          todoList[count].append(str(todoObject.matkul))
          todoList[count].append(str(todoObject.jenis))
          todoList[count].append(str(todoObject.topik))
          todoList[count].append(str(todoObject.deadline))
          todoList[count].append(str(todoObject.status))
     return todoList


@app.route("/")
def index():
     return render_template("index.html") 
     # return "hello"
     
@app.route("/get")
def get_bot_response():
     jenisTaskDeadline = ["Tubes","Tucil"]
     jenisTaskNormal = ["Praktikum","Ujian","Kuis"]
     attributeTask = ["id","matkul","jenis","topik","deadline","status"]

     mainCommandList = ["Deadline", "Diundur", "Selesai"]
     additionalCommandList = ["Hari", "Minggu", "Hari Ini","Task"]

     query = request.args.get("msg") 


     mainCommand = parseCommand(query,mainCommandList, bm.stringMatching)
     additionalCommand = parseCommand(query,additionalCommandList, bm.stringMatching)
     tasks = extractTask(query,jenisTaskDeadline,jenisTaskNormal,bm.stringMatching)
     nHariPekan = extractNHariPekan(query)

     #Cek DB
     taskFromDB = Todo.query.order_by(Todo.deadline).all() 
     print("hello")
     print(todoToList(taskFromDB))

     checkMissmatch = [0,[]]
     MISS_THRESHOLD = 0.25 #ini maksudnya 75% match
     checkMissmatch = missWordRecc(query, mainCommandList, MISS_THRESHOLD,checkMissmatch)
     checkMissmatch = missWordRecc(" ".join(checkMissmatch[1]), additionalCommandList, MISS_THRESHOLD,checkMissmatch)

     if (checkMissmatch[0]):
          print("checkMisssmath", checkMissmatch[0])
          print(" ".join(checkMissmatch[1]))
          return "Mungkin maksud anda: <i>" + " ".join(checkMissmatch[1]) +"<i>?"

     
     
     return str(commandValidation(mainCommand, additionalCommand,mainCommandList,additionalCommandList, tasks, attributeTask,nHariPekan, bm.stringMatching,taskFromDB))
     # return "dududu"

if __name__ == "__main__":
     app.run(debug = True)


