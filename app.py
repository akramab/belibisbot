from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import datetime, timedelta
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# from programKecil import *
# from levenshteinDistance import *

app = Flask(__name__) 
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///testa.db"
db = SQLAlchemy(app)

engine = create_engine('sqlite:///testa.db', echo = True)
meta = MetaData()

students = Table(
    'todo', meta, 
    Column('id', Integer, primary_key = True), 
    Column('matkul', String), 
    Column('jenis', String),
    Column('topik', String), 
    Column('deadline', String),
    Column('status', Integer)
)
meta.create_all(engine)

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


#Levensteihn Distance
def levenshteinDistance(stringA,stringB):
    distanceMatrix = [[0 for j in range(len(stringA)+1)] for i in range(len(stringB)+1)]
    for i in range(len(stringB)+1):
        for j in range(len(stringA)+1):
            if j == 0:
                distanceMatrix[i][j] = i
            if i == 0:
                distanceMatrix[i][j] = j
            if (j-1 >= 0 and i!= 0):
                distanceMatrix[i][j] = min(distanceMatrix[i][j-1], distanceMatrix[i-1][j-1],distanceMatrix[i-1][j])
                if (stringA[j-1] != stringB[i-1]):
                    distanceMatrix[i][j] += 1 
    return distanceMatrix[len(stringB)-1][len(stringA)-1]

def LD(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
       
    res = min([LD(s[:-1], t)+1,
               LD(s, t[:-1])+1, 
               LD(s[:-1], t[:-1]) + cost])

    return res

def missWordRecc(text, kataPenting, missThreshold, result):
    # result = [[0],[]]
    
    for count, mismatch in enumerate((text.split())):
        foundMismatch = False
        for keyword in kataPenting:
            editDistance = levenshteinDistance(mismatch.lower(),keyword.lower())
            mismatchPercentage = float(editDistance/max(len(keyword),len(mismatch)))
            if (mismatchPercentage < missThreshold and mismatchPercentage > 0):
                print("mismatch percentage",mismatchPercentage)
                print(keyword)
                print("editdistance: ", editDistance)
                result[1].append(keyword)
                foundMismatch = True
                result[0] = 1
                break
        if (not foundMismatch and mismatch not in result[1]):
            result[1].append(mismatch)
    if (result):
        return result
    return -1

#BM
def buildLast(patternInput):
    pattern = patternInput.lower().strip()
    #Jumlah karakter ASCII ada 128
    last = [-1 for i in range(128)]
    for index, char in enumerate(pattern):
        # ord = fungsi buat dapetin ASCII dari suatu char
        last[ord(char)] = index
    return last

def stringMatching(textInput, patternInput):
    text = textInput.lower().strip()
    pattern = patternInput.lower().strip()

    j = len(pattern)-1
    i = j
    n = len(text)
    m = len(pattern)
    lastO = buildLast(pattern)
    while (i < n):
        if (text[i] == pattern[j]):
            if (j == 0):
                #if found matching pattern
                return i
            #looking-glass
            i -= 1
            j -= 1
        else:
            #Geser i sesuai kasus (1, 2, atau 3)
            i = i + m - min(j, lastO[ord(text[i])]+1)

            #Balikin lagi j ke indeks akhir pattern
            j = m - 1
    #not found
    return -1

#Main Function
def convertDateFormat(date):
    temp = date.split()

    #Convert to lowercase if not already
    temp[1] = temp[1].lower()
    if (len(temp)> 1):
        if temp[1] == "januari":
            temp[1] = "01"
        if temp[1] == "februari":
            temp[1] = "02"
        if temp[1] == "maret":
            temp[1] = "03"
        if temp[1] == "april":
            temp[1] = "04"
        if temp[1] == "mei":
            temp[1] = "05"
        if temp[1] == "juni":
            temp[1] = "06"
        if temp[1] == "juli":
            temp[1] = "07"
        if temp[1] == "agustus":
            temp[1] = "08"
        if temp[1] == "september":
            temp[1] = "09"
        if temp[1] == "oktober":
            temp[1] = "10"
        if temp[1] == "november":
            temp[1] = "11"
        if temp[1] == "desember":
            temp[1] = "12"
    
    fixedDate = "/".join(temp)

    return fixedDate

def parseQuery(query, kataPenting, validCommand, additionalCommand,stringMatching):
    result = {"kataPenting": [],
                "validCommand": [],
                "additionalCommand": [],
                "task": [],
                "tanggal":[]}

    for kata in kataPenting:
        if(stringMatching(query,kata)+1):
            result["kataPenting"].append(kata)
    
    for keyword in validCommand:
        if(stringMatching(query,keyword)+1):
            result["validCommand"].append(keyword)
    
    for keyword in additionalCommand:
        if(stringMatching(query,keyword)+1):
            result["additionalCommand"].append(keyword)
    
    datePattern = re.compile(r'\d{2}.\d{2}.\d{4}')
    tempParse = datePattern.findall(query)

    for date in tempParse:
        result["tanggal"].append(date)
    
    return result


def commandRecognition(query, commandDB):
    validCommand = [0 for i in range(len(commandDB))]

    for keyword in query['validCommand']: #Kayanya ini perlu dibikin lebih dinamik
        for i, command in enumerate(commandDB):
            if keyword == command:
                validCommand[i] += 1
    if sum(validCommand) == 1:
        return True
    else:
        return False

def parseCommand(query,command, stringMatching):
    parsed = [[] for i in range(len(command))]

    for count, availableCommand in enumerate(command):
        if (stringMatching(query,availableCommand)+1):
            parsed[count].append(availableCommand)
    
    return parsed

def extractTask(query, deadlineTask,normalTask, stringMatching):
    task = {"id": [],
            "matkul":[],
            "jenis":[],
            "topik":[],
            "deadline":[],
            "status":[]}
    # kodeMatkulPattern = re.compile(r'[a-zA-Z]{2}\d{4}')

    #Referensi regex buat ambil consecutive capitalized word: https://stackoverflow.com/questions/31570699/regex-to-get-consecutive-capitalized-words-with-one-or-more-words-doesnt-work
    #matkulPattern = re.compile(r'((?:[Mm]atkul|[Mm]ata [Kk]uliah)|[a-zA-Z]{2}\d{4})\s?([A-Za-z\s]*)?\s?([Tt]opik)\s(\b(?:[A-Z][a-z]*\b\s*)+)')
    idPattern = re.compile(r'[Tt]ask\s\d+')
    matkulPattern = re.compile(r'(\b(?:[A-Z][a-z]*\b\s*\d?)+|[A-Z]{2}\d{4})')
    datePattern = re.compile(r'(\d{2}.\d{2}.\d{4}|\d{2}.(?:[Jj]anuari|[Ff]ebruari|[Mm]aret|[Aa]pril|[Mm]ei|[Jj]uni|[Jj]uli|[Aa]gustus|[Ss]eptember|[Oo]ktober|[Nn]ovember|[Dd]esember).\d{4})')
    # topikPattern = re.compile(r'\b(?:[A-Z][a-z]*\b\s*\d)+')
    topikPattern = re.compile(r'(\b(?:[A-Z][a-z]*\b\s*\d?)+|[A-Z]{2}\d{4})')
    # topikPattern = re.compile(r'^topik\s')


    #Add task from query

    #Add ID

    tempData = idPattern.findall(query)
    if(tempData):
        print("Ini temp data gaes",tempData)
        for id in tempData:
            print(id)
            task["id"].append(id.split()[1])
    
    #Add matkul/kode matkul
    #ALGO LAMA/KAYANYA UDAH OBSOLETE
    # tempData = matkulPattern.findall(query)
    # print(tempData)
    # if (tempData):
    #     if (tempData[0][0][3].isdigit()):
    #         task["matkul"] = tempData[0][0].strip()
    #     else:
    #         task["matkul"] = tempData[0][1].strip()

    index = -1
    for cariMatkul in ["matkul", "mata kuliah"]:
        if (stringMatching(query,cariMatkul)+1):
            print("Masuk sini")
            ejaMatkul = cariMatkul
            index = stringMatching(query,cariMatkul)
    
    #Pake metode stringMatching
    index2 = stringMatching(query,"topik") #Ini kepake juga buat topik
    if(index != -1):
        if (index2 != -1):
            task["matkul"].append(query[index+len(ejaMatkul)+1:index2-1].strip())

        #Pake metode regex
        else:
            tempData = matkulPattern.findall(query[index+len(ejaMatkul)+1:])
            if (tempData):
                task["matkul"].append(" ".join(tempData).strip())

    #Add topik
    if(index2 != -1):
        tempData = topikPattern.findall(query[index2+len("topik")+1:])
        if (tempData):
            task["topik"].append(" ".join(tempData).strip())


    #Add tanggal (deadline)
    #KAYANYA PERLU ADA VALIDASI LAGI, MUNGKIN JUGA ENGGAK. 
    tempData = datePattern.findall(query)
    if (tempData):
        for date in tempData:
            if (len(date) == 10):
                task["deadline"].append(date.strip())
            else:
                task["deadline"].append(convertDateFormat(date).strip())

    
    #Add jenis task
    #yang di sini mungkin perlu dikasih validasi kalau tasknya kebanyakan
    for macamTask in deadlineTask:
        if (stringMatching(query,macamTask)+1):
            task["jenis"].append(macamTask)
            #Add status to unfinished
            # task["status"].append("0")
    
    for macamTask in normalTask:
        if (stringMatching(query,macamTask)+1):
            task["jenis"].append(macamTask)
            #Add status to unfinished
            # task["status"].append("-1")
    
    #Ini bisi ga perlu sih

    

    return task

def extractNHariPekan(query):
    hariPekanPattern = re.compile(r'(\d*)\s([Hh]ari|[Mm]inggu)')
    result = []
    hasilPattern = hariPekanPattern.findall(query)

    if (hasilPattern):
        for N in hasilPattern[0]:
            if N.isdigit():
                result.append(int(N))
    return result

def isDate1GreaterEQ(date1,date2):
    year1 = int(date1[6:10])
    year2 = int(date2[6:10])

    month1 = int(date1[3:5])
    month2 = int(date2[3:5])

    day1 = int(date1[0:2])
    day2 = int(date2[0:2])

    if year1 > year2:
        return True
    if month1 > month2 and year1 == year2:
        return True
    if day1 >= day2 and year1 == year2 and month1 == month2:
        return True
    return False

def isDate1LowerEQ(date1,date2):
    year1 = int(date1[6:10])
    year2 = int(date2[6:10])

    month1 = int(date1[3:5])
    month2 = int(date2[3:5])

    day1 = int(date1[0:2])
    day2 = int(date2[0:2])

    if year1 < year2:
        return True
    if month1 < month2 and year1 == year2:
        return True
    if day1 <= day2 and month1 == month2 and year1 == year2:
        return True
    return False

def weekToDays(week):
    return week*7

def todayPlusN(nDays):
    resultDate = datetime.now() + timedelta(days=nDays)  
    return resultDate.strftime('%d/%m/%Y')


def isTaskInputComplete(task):
    return len(task["matkul"]) == len(task["jenis"]) and len(task["jenis"]) == len(task["topik"]) and len(task["topik"]) == len(task["deadline"]) and len(task["deadline"]) >= 1

def isTaskInputEmpty(task):
    return len(task["matkul"]) == len(task["jenis"]) and len(task["jenis"]) == len(task["topik"]) and len(task["topik"]) == len(task["deadline"]) and len(task["deadline"]) == 0

def isTaskOnlyX(task, taskX, attributeTask, stringMatching):
    if  len(task[taskX]) > 0:
        for taskAttribute in attributeTask:
            if stringMatching(taskX,taskAttribute) == -1 and len(task[taskAttribute]) != 0:
                if(taskAttribute != "deadline" and taskAttribute!= "jenis"):
                    return -1
        return len(task[taskX])
    return -1

def isTaskOnlyX2(task, taskX, attributeTask, stringMatching):
    if  len(task[taskX]) > 0:
        for taskAttribute in attributeTask:
            if stringMatching(taskX,taskAttribute) == -1 and len(task[taskAttribute]) != 0:
                if(taskAttribute != "deadline" and taskAttribute!= "jenis"):
                    return -1
        return len(task[taskX])
    return -1


def commandToIndex(command,commandDB, stringMatching):
    for index, availableCommand in enumerate(commandDB):
        if stringMatching(command,availableCommand)+1:
            return index
    return -1

def isCommandEmpty(command):
    for availableCommand in command:
        if (len(availableCommand) != 0):
            return False
    return True

def isCommandOnlyX(userCommand, commandX, commandDB, stringMatching):
    commandIndex = commandToIndex(commandX, commandDB, stringMatching)
    if  (commandIndex+1):
        for count, availableCommand in enumerate(userCommand):
            if count == commandIndex and len(availableCommand)!= 0:
                return True
            elif len(availableCommand) != 0:
                return False
    return False

def isCommandOnlyXandY(userCommand, commandX,commandY, commandDB, stringMatching):
    commandIndex1 = commandToIndex(commandX, commandDB, stringMatching)
    commandIndex2 = commandToIndex(commandY, commandDB, stringMatching)
    if  (commandIndex1+1 and commandIndex2+1):
        if len(userCommand[commandIndex1]) != len(userCommand[commandIndex2]):
            return False
        if len(userCommand[commandIndex1]) == 0 or len(userCommand[commandIndex2]) == 0:
            return False
        if (len(userCommand[commandIndex1]) == len(userCommand[commandIndex2]) and len(userCommand[commandIndex1]) != 0):
            for count, availableCommand in enumerate(userCommand):
                if len(availableCommand)!= 0:
                    if availableCommand[0] != commandX and availableCommand[0] != commandY:
                        return False
    return True


def taskDBToString(taskDB):
    result = "[Daftar Task Punya Kamu]<br>"
    for num, task in enumerate(taskDB):
        result += " "+ str(num+1)+". "
        result += "(ID: " + str(task.id) +") "
        result += task.deadline + " - "
        result += task.matkul + " - "
        result += task.jenis + " - "
        result += task.topik
        result += "<br>"
    return result

def filterDBTask(taskDB, filter, keyWord):
    result = []
    if filter == "id":
        for task in (taskDB):
            if (str(task.id) == keyWord):
                result.append(task)
    if filter == "matkul":
        for task in (taskDB):
            if (task.matkul == keyWord):
                result.append(task)
    if filter == "jenis":
        for task in (taskDB):
            if (task.jenis == keyWord):
                result.append(task)
    if filter == "deadline hari ini":
        for task in (taskDB):
            if (task.deadline == keyWord):
                result.append(task)
    if filter == "deadline antara":
        for task in (taskDB):
            if (isDate1LowerEQ(task.deadline,keyWord) and isDate1GreaterEQ(task.deadline,datetime.today().strftime('%d/%m/%Y'))):
                result.append(task)
    if filter == "status deadline":
        for task in (taskDB):
            if (task.status == keyWord):
                result.append(task)
    if filter == "normal":
        for task in (taskDB):
            if (isDate1GreaterEQ(task.deadline,keyWord)):
                result.append(task)

    return result

def filterDBTaskTwoDate(taskDB,date1,date2):
    result = []
    for task in (taskDB):
        if (isDate1LowerEQ(task.deadline,date2) and isDate1GreaterEQ(task.deadline,date1)):
            result.append(task)
    return result

def addNewTask(newTask):
    newT = Todo(newTask["matkul"][0],newTask["jenis"][0], newTask["topik"][0],newTask["deadline"][0],0) #param terakhirnya perlu diupdate
    db.session.add(newT)
    db.session.commit()

def isTaskExist(task, key):
    for t in task:
        if (t.matkul == key):
            return True
    return False


def commandValidation(mainCommand,additionalCommand,mainCommandList, additionalCommandList,task, attributeTask,nHariPekan, stringMatching, taskFromDB):
    taskFromDB = filterDBTask(taskFromDB, "normal",datetime.today().strftime('%d/%m/%Y'))
    taskFromDB = filterDBTask(taskFromDB, "status deadline",0)
    # print("Masuk validation")
    case2c = False
    print(task)
    # print("panjang char matkul:", len(task["matkul"][0]))

    #case 1 (kayanya ini nanti taruh bawah sih kalau udah kelar)
    if ((isCommandEmpty(mainCommand) or isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching)) and isCommandEmpty(additionalCommand)):
        if(isTaskInputComplete(task)):
            output = "[TASK BERHASIL DICATAT]<br>"+"(ID: " + str(len(taskFromDB)+1) +") " +str(task["deadline"][0]) +" - " +str(task["matkul"][0]) +" - " +str(task["jenis"][0]) +" - " +str(task["topik"][0])
            addNewTask(task)
            print("ini masuk case 1")
            return output
            #masih ngebug, sementara tanganin pake return
            #tambahin fungsi add task ke sini
        elif(isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching)):
            print("skip case 1")
        else:
            #tasknya kaga lengkap/invalid
            #tambahin pesan kesalahan di sini
            print("Maaf perintah kamu kurang tepat. Task kamu tidak lengkap!")
    #case 4 (ditaruh di sini karena suatu hal)
    if (isCommandOnlyXandY(mainCommand,"Deadline","Diundur",mainCommandList,stringMatching)):
        #belum disimpan tapi ya
        idx = int(task["id"][0])
        update = Todo.query.filter_by(id=idx).first()
        update.deadline = task["deadline"][0]
        db.session.commit()


        # temp = filterDBTask(taskFromDB,"id",task["id"][0])
        print("ini masuk case 4")
        return "Task "+ str(idx)+" berhasil diperbaharui"
        print("Case 4! Jalankan fungsi update deadline task!")

    #case 2
    elif(isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching)):
        #2.c harus di atas soalnya dia bisa digabung sama yang lain
        # print(isTaskOnlyX(task, "jenis", attributeTask,stringMatching))
        if (isTaskOnlyX(task, "jenis", attributeTask, stringMatching) != -1):
            print("Case 2.c! Jalankan fungsi tampilkan task dengan jenis tertentu!")
            case2c = True
            # return taskDBToString(filterDBTask(taskFromDB,"jenis",task["jenis"][0]))
            taskFromDB = (filterDBTask(taskFromDB,"jenis",task["jenis"][0]))
        #2.a
        # if isCommandEmpty(additionalCommand) and isTaskInputEmpty(task):
        if isTaskInputEmpty(task) and len(additionalCommand[0]) == 0 and len(additionalCommand[1]) == 0 and len(additionalCommand[2]) == 0:
            print("Case 2.a! Jalankan fungsi menampilkan seluruh task!")
            return taskDBToString(taskFromDB)
        #2.b1
        elif (isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching) and isTaskOnlyX(task,"deadline",attributeTask, stringMatching) == 2):
            print("Case 2.b1! Jalankan fungsi menampilkan task di antara dua buah tanggal!")
            filteredTask = (filterDBTaskTwoDate(taskFromDB, task["deadline"][0],task["deadline"][1]))
            if (filteredTask):
                return taskDBToString(filteredTask)
            else:
                return "Mantap pak bos, dari tanggal "+task["deadline"][0]+" sampai tanggal "+ task["deadline"][1]+" enggak ada deadline!"
        elif(isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching) and len(nHariPekan) == 1):
            #2.b2
            if(isCommandOnlyX(additionalCommand,"hari",additionalCommandList,stringMatching)):
                filteredTask = (filterDBTask(taskFromDB,"deadline antara",todayPlusN(nHariPekan[0])))
                if (filteredTask):
                    print("ini masuk case 2.b2")
                    return taskDBToString(filteredTask)
                else:
                    return "Mantap pak bos, "+str(nHariPekan[0])+" hari ke depan enggak ada deadline!"
                print("Case 2.b2! Jalankan fungsi menampilkan task N hari dari sekarang!")
            #2.b3
            if(isCommandOnlyX(additionalCommand,"minggu",additionalCommandList,stringMatching)):
                filteredTask = (filterDBTask(taskFromDB,"deadline antara",todayPlusN(weekToDays(nHariPekan[0]))))
                if (filteredTask):
                    print("ini masuk case 2.b3")
                    return taskDBToString(filteredTask)
                else:
                    return "Mantap pak bos, "+str(nHariPekan[0])+" minggu ke depan enggak ada deadline!"
                print("Case 2.b3! Jalankan fungsi menampilkan task N minggu dari sekarang!")
        #2.b4
        elif(isCommandOnlyX(additionalCommand,"hari ini",additionalCommandList,stringMatching)):
            filteredTask = (filterDBTask(taskFromDB,"deadline hari ini",todayPlusN(0)))
            if (filteredTask):
                print(nHariPekan)
                print("ini masuk case 2.b4")
                return taskDBToString(filteredTask)
            else:
                return "Mantap pak bos, hari ini enggak ada deadline!"
            print("Case 2.b4! Jalankan fungsi menampilkan task hari ini")
        
        #case 3
        #tambahin fungsi buat nyari ID sama validasi inputnya cm ada ID
        elif (isTaskOnlyX(task,"matkul",attributeTask,stringMatching)+1):
            # filterDBTask(taskFromDB,"matkul",task["matkul"][0])
            # masih kurang yang ID
            # print(task)
            print("Case 3! Jalankan fungsi search matkul by ID/Nama matkul")
            print("ini isi matkul",task["matkul"])
            print("ini task", task)
            if (isTaskExist(taskFromDB,task["matkul"][0])):
                return taskDBToString(filterDBTask(taskFromDB,"matkul",task["matkul"][0]))
            else:
                return "task yang kamu cari tidak ditemukan!"
        
        #kalau cuma case 2a doang
        if (case2c):
            return taskDBToString(filterDBTask(taskFromDB,"jenis",task["jenis"][0]))

        

    
        # elif
    
    #case 5
    elif(isCommandOnlyX(mainCommand,"selesai",mainCommandList,stringMatching) and len(task["id"]) != 0):
        print("Case 5! jalankan fungsi update task selesai")
        idx = int(task["id"][0])
        update = Todo.query.filter_by(id=idx).first()
        update.status = 1
        db.session.commit()
        return "Task "+ str(idx)+" telah ditandai selesai"
    
    elif(isCommandOnlyX(mainCommand,"help",mainCommandList,stringMatching)):
        return """  1. "(ID: #) dd/mm/yy - <matkul>- <jenis>- <topik>" untuk menambahkan agenda baru<br>
                    2. Menampilkan agenda yang sudah tercatat<br>
                        - DATE1 sampai DATE_2<br>
                        - N minggu ke depan<br>
                        - N hari ke depan<br>
                        - Hari ini<br>
                    3. <matkul> untuk menampilkan deadline dari matkul tersebut<br>
                    4. <ID> <tanggal> untuk mengubah tanggal deadline task<br>
                    5. selesai <ID> untuk menandai tugas sudah dikerjakan<br>
                    6. help untuk memunculkan opsi kata penting yang digunakan<br>
        """

    else:
        #perintah tidak dikenali
        print("Perintah kamu tidak dikenali!")
        # return str(isDate1GreaterEQ("12/03/2021", "13/03/2021"))
        return "waduh, botnya bingung bang. Coba ketik help deh!"
    print(task)
    print(additionalCommand)
    return "Botnya bingung bang :(, coba ketik help ya biar perintahnya bisa dikenali!"

@app.route("/")
def index():
    return render_template("index.html") 
    
@app.route("/get")
def get_bot_response():
    jenisTaskDeadline = ["Tubes","Tucil"]
    jenisTaskNormal = ["Praktikum","Ujian","Kuis"]
    attributeTask = ["id","matkul","jenis","topik","deadline","status"]

    mainCommandList = ["Deadline", "Diundur", "Selesai","Help"]
    additionalCommandList = ["Hari", "Minggu", "Hari Ini","Task"]

    query = request.args.get("msg") 


    mainCommand = parseCommand(query,mainCommandList, stringMatching)
    additionalCommand = parseCommand(query,additionalCommandList, stringMatching)
    tasks = extractTask(query,jenisTaskDeadline,jenisTaskNormal, stringMatching)
    nHariPekan = extractNHariPekan(query)

    #Cek DB
    taskFromDB = Todo.query.order_by(Todo.deadline).all() 
    #  print("hello")
    #  print(todoToList(taskFromDB))

    checkMissmatch = [0,[]]
    MISS_THRESHOLD = 0.25 #ini maksudnya 75% match
    checkMissmatch = missWordRecc(query, mainCommandList, MISS_THRESHOLD,checkMissmatch)
    checkMissmatch = missWordRecc(" ".join(checkMissmatch[1]), additionalCommandList, MISS_THRESHOLD,checkMissmatch)

    if (checkMissmatch[0]):
        return "Mungkin maksud anda: <i>" + " ".join(checkMissmatch[1]) +"<i>?"

    # return "deploynya susah bet :("
    return str(commandValidation(mainCommand, additionalCommand,mainCommandList,additionalCommandList, tasks, attributeTask,nHariPekan, stringMatching,taskFromDB))

if __name__ == "__main__":
    app.run(debug = True)


