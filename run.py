from flask import Flask,Response,jsonify,request,flash,render_template,current_app,redirect
import sqlite3
import random

#db= sqlite3.connect("DB.db")
app=Flask(__name__)
app.secret_key = "UGABUGASTIKVALABLJAT"
#cursor=db.cursor()

api_test=[ {'suck':'my' , 'spaget':'gg'}]

prosliPredmet=None
sviPre=None
allQue=None
trueList=[]
currentQUestion=[]
user="false"


@app.route("/")
def startPage():
    return render_template("firstpage.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    global user
    if request.method =="POST":
        ime=request.form.get("ime")
        sifra=request.form.get("sifra")

        print(ime)
        print(sifra)
        with sqlite3.connect("DB.db") as db:
            info = db.execute("select Name, Password from User where Name='%s'"% ime).fetchone()

            print(info)
            
            if info == None:
                flash('User ne postoji')
            elif sifra != info[1]:
                flash('Kriva sifra')
            else:
                user = "true"
                return redirect("QQviz")


    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    
    if request.method =="POST":
        ime=request.form.get("ime")
        sifra=request.form.get("sifra")
        email=request.form.get("email")

        print(ime)
        print(sifra)
        print(email)

        with sqlite3.connect("DB.db") as db:
            

            usernameExists= db.execute("select count (*) from User where Name='%s'"% ime).fetchone()
            
            emailExists=  db.execute("select count (*) from User where Email='%s'"% email).fetchone()
            print(usernameExists)
            print(emailExists)
            
            if usernameExists[0] != 0:
                flash('Username vec postoji')
                flash("test flash")
                data='false'
                
                return render_template("register.html", working=data)
                #return render_template("register.html")
            elif emailExists[0] != 0:
                flash('Email vec postoji')
                data='false'
                return render_template("register.html", working=data)
                #return render_template("register.html")
            else:
                cursor=db.cursor()
                cursor.execute("insert into User(Name, Password, Email) values(:ime,:password,:email)",{"ime":ime,"password":sifra,"email":email})
                db.commit()
                data='true'
                flash('Registracija uspjela YEEY. Klikni na ovo za login')
                return render_template("register.html", working=data)

            
    
    return render_template("register.html")


@app.route("/QQviz", methods=["GET", "POST"])
def QQviz():
    
    global prosliPredmet
    global sviPre
    global allQue
    global trueList
    global currentQUestion
    global user
    print(user)
    if request.method =="POST":
        ime=None
        odgovor=None
        ime=request.form.get("ime")
        odgovor = request.form.get("answer")
        nextQ = request.form.get("nextQuestion")
        print("==================")
        print(ime)
        print(odgovor)
        print(nextQ)
        
        with sqlite3.connect("DB.db") as db:
            cursor = db.cursor()
            if odgovor !=None:
                print(trueList)
                if odgovor== trueList[1]:
                    flash('odgovori je točan')
                    return render_template("QQviz.html",trenutnoPitanje=currentQUestion, sviPredmeti=sviPre, odgovoreno="true", tocno="true",User=user)
                else: 
                    flash('odgovor je netočan, točan odgovor je '+ trueList[1])
                    return render_template("QQviz.html",trenutnoPitanje=currentQUestion, sviPredmeti=sviPre, odgovoreno="true", tocno="false", User=user)

            else:
                
                def nextQuestion():
                    index = random.randint(0,len(allQue)-1)
                    print("pop index")
                    
                    thisQuestion = list(allQue[index])
                    allQue.pop(index)
                    
                    print(" linija 137 ================================")
                    print(len(thisQuestion))


                    while trueList:
                        trueList.pop(0)

                    while currentQUestion:
                        currentQUestion.pop(0)

                    trueList.append(thisQuestion[0])
                    trueList.append(thisQuestion[1])
                    currentQUestion.append(thisQuestion[0])
                    thisQuestion.pop(0)
                    
                    
                    print(len(thisQuestion))
                    while thisQuestion:
                        index=random.randrange(len(thisQuestion))
                        currentQUestion.append(thisQuestion[index])
                        thisQuestion.pop(index)

                    

                    print(trueList)
                    print(currentQUestion)

                    return currentQUestion

                if nextQ:

                    if not allQue :
                        allQue =cursor.execute("select pitanje,tocanodgovor,netocan1,netocan2,netocan3 from Pitanja where PredmetID=%s"%prosliPredmet).fetchall()
                        test =nextQuestion()
                        print("Allque is empty filing up")
                        press="true"
                        return render_template("QQviz.html",trenutnoPitanje=list(test), sviPredmeti=sviPre, odgovoreno="false",User=user)


                    print("next question")
                    test=nextQuestion()
                    press="true"
                    return render_template("QQviz.html",trenutnoPitanje=list(test), sviPredmeti=sviPre, odgovoreno="false",User=user)

                
                if prosliPredmet == None:
                    allQue =cursor.execute("select pitanje,tocanodgovor,netocan1,netocan2,netocan3 from Pitanja where PredmetID=%s"%ime).fetchall()
                    print("ako je psli predmet null")
                    prosliPredmet = ime
                    test =nextQuestion()
                    return render_template("QQviz.html",trenutnoPitanje=list(test), sviPredmeti=sviPre, odgovoreno="false",User=user)

                if ime == prosliPredmet and allQue != None :
                    return render_template("QQviz.html",trenutnoPitanje=currentQUestion, sviPredmeti=sviPre, odgovoreno="false",User=user)

                elif ime != prosliPredmet:
                    allQue =cursor.execute("select pitanje,tocanodgovor,netocan1,netocan2,netocan3 from Pitanja where PredmetID=%s"%ime).fetchall()
                    test =nextQuestion()
                    prosliPredmet=ime
                    print("182")
                    return render_template("QQviz.html",trenutnoPitanje=list(test), sviPredmeti=sviPre, odgovoreno="false",User=user)


    else:
        
        with sqlite3.connect("DB.db") as db:
            cursor = db.cursor()
            sviPre =cursor.execute("select * from Predmet").fetchall()
            print("test")
            print(sviPre)
            return render_template("QQviz.html",sviPredmeti=sviPre, trenutnoPitanje=[],User=user)


@app.route("/novoPitanje", methods=["GET", "POST"])
def novoPitanje():
    global sviPre

    if request.method =="POST":
        
        noviPredmet = request.form.get("novi")
        predmetID = request.form.get("predmetID")
        novoPitanje = request.form.get("pitanje")
        tOdgovor = request.form.get("tOdgovor")
        n1Odgovor = request.form.get("n1Odgovor")
        n2Odgovor = request.form.get("n2Odgovor")
        n3Odgovor = request.form.get("n3Odgovor")


        

        print("================")
        print(noviPredmet)
        print(predmetID)
        print(novoPitanje)
        print(tOdgovor)
        print(n1Odgovor)
        print(n2Odgovor)
        print(n3Odgovor)
        with sqlite3.connect("DB.db") as db:
            cursor=db.cursor()
            if noviPredmet != None:
                predmetExists= db.execute("select count (*) from Predmet where Name='%s'"% noviPredmet).fetchone()
                if predmetExists[0] != 0:
                    flash("Predmet postoji")
                    return render_template("novoPitanje.html",sviPredmeti=sviPre)
                else:
                    cursor.execute("insert into Predmet(Name) values(:name)",{"name":noviPredmet})
                    db.commit()
                    flash("YEY Predmet uspjesno dodan ")
                    cursor = db.cursor()
                    sviPre =cursor.execute("select * from Predmet").fetchall()
                    return render_template("novoPitanje.html",sviPredmeti=sviPre)


            else:
                cursor.execute("insert into Pitanja(Pitanje, TocanOdgovor,Netocan1,Netocan2,Netocan3,PredmetID) values(:pitanje,:tocanodgovor,:netocan1,:netocan2,:netocan3,:predmetID)",{"pitanje":novoPitanje,"tocanodgovor":tOdgovor,"netocan1":n1Odgovor,"netocan2":n2Odgovor,"netocan3":n3Odgovor,"predmetID":predmetID})
                db.commit()
                flash("YEY Pitanje uspjesno dodano!!!!!! LETS GO PARTY!! ")
                



    if not sviPre:
        with sqlite3.connect("DB.db") as db:
            cursor = db.cursor()
            sviPre =cursor.execute("select * from Predmet").fetchall()
            print("test")
            print(sviPre)
    return render_template("novoPitanje.html",sviPredmeti=sviPre)

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)



