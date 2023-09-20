from flask import Flask, render_template, redirect, flash, session, request 
import web
import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(64).hex()

@app.route("/")

@app.route('/', methods=["GET"])
def Time_start():
    info = web.ReturnUserInfo()
    time = web.Time_start()
    flash(time)
    requests = web.ViewArrayRequests()

    unixToDatetime = datetime.datetime.fromtimestamp(int(time))
    faza = web.ReturnFaze()
    print(faza)
    return render_template('index.html', unixToDatetime=unixToDatetime, faza=faza, info=info, requests=requests) 

@app.route("/reg", methods=["GET", "POST"])
def reg():
    if session.get("user") == None:
        if request.method == "POST":
            acc = request.form.get("acc")
            key = request.form.get("key")
            name = request.form.get("name")
            password = request.form.get("password")
            result = web.Registration(acc,key,name,password)
            if type(result) == str:
                flash(result)
            return redirect("/login")
        return render_template("reg.html")
    return redirect("/lk")

# функция авторизации
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user") == None:
        if request.method == "POST":
            acc = request.form.get("acc")
            key = request.form.get("key")
            name = request.form.get("name")
            password = request.form.get("password")
            result = web.Authorization(acc, key, name, password)
            if type(result) == str:
                flash(result)
            session["user"] = result
            return redirect("/lk")
        return render_template("login.html")
    return redirect("/lk")
        
@app.route("/lk")
def lk():
    if session.get("user") != None:
        info = web.ReturnUserInfo()
        balance = web.returnBalanceEther()
        public = web.returnPublicTokenBalance()
        private = web.returnPrivateTokenBalance()
        seed = web.returnSeedTokenBalance()
        return render_template("lk.html", result = session["user"], info=info, balance=balance, public=public, private=private, seed=seed)
    return redirect("/login")

@app.route("/Privatetoken")
def Privatetoken():
    info = web.ReturnUserInfo()

    return render_template('privatetoken.html', info=info)

@app.route("/Privatetoken", methods=["GET", "POST"])
def PrivatetokenF():
    amount = request.form.get("amount")
    key = request.form.get("key")
    info = web.ReturnUserInfo()
    result = web.BuyPrivateToken(amount, key)
    if type(result) == str:
        flash(result)
    return render_template("privatetoken.html", info=info)

@app.route("/Publictoken")
def Publictoken():
    info = web.ReturnUserInfo()

    return render_template('publictoken.html', info=info)

@app.route("/Publictoken", methods=["GET", "POST"])
def PublictokenF():
    if request.method == "POST":
        amount = request.form.get("amount")
        acc = request.form.get("acc")
        key = request.form.get("key")
        info = web.ReturnUserInfo()

        print("huy")
        result = web.BuyPublicToken(amount, acc, key)
        print("huy2")
        if type(result) != str:
            flash("Успешно")
        else:
            flash(result)
        print("huy3")

    return render_template("publictoken.html", info=info)

@app.route('/changePrice')
def changePrice():
    info = web.ReturnUserInfo()
    return render_template('changePrice.html', info=info)
    # return redirect('/login')

@app.route('/changePrice', methods=["GET","POST"])
def changePriceF():
    if session.get("user") != None:
        if request.method == "POST":
            acc = request.form.get("acc")
            key = request.form.get("key")
            newPrice = request.form.get("newPrice")
            result = web.ChangePriceForPublicTokens(acc,key,newPrice)
            if type(result) != str:
                flash("Success!")
            else:
                flash(result)
            return redirect("/lk")
        return render_template("changePrice.html")
    return redirect("/lk")

@app.route('/SendPublicTokens')
def SendPublicTokens():
    info = web.ReturnUserInfo()
    return render_template('SendPublicTokens.html', info=info)
    # return redirect('/login')

@app.route('/SendPublicTokens', methods=["GET", "POST"])
def SendPublicTokensF():
    if session.get('user') != None:
        if request.method == "POST":
            acc = request.form.get("acc")
            key = request.form.get("key")
            amount = request.form.get("amount")
            account = request.form.get("account")
            result = web.SendPublicTokens(amount,account,acc,key)
            if type(result) != str:
                flash("Success!")
            else:
                flash(result)
            return redirect("/lk")
        return render_template("SendPublicTokens.html")
    return redirect("/lk")


@app.route("/addRequest")
def addRequest():
    info = web.ReturnUserInfo()

    return render_template('addRequest.html', info=info)

@app.route("/addRequest", methods=["GET", "POST"])
def addRequestF():
    if session.get("user") != None:
        if request.method == "POST":
            acc = request.form.get("acc")
            key = request.form.get("key")
            result = web.AddRequestInArray(acc, key)
            if type(result) == str:
                flash(result)
            session["user"] = result
            print(result)
            print("hey")

            return redirect("/login")
        print("hey1")
        return render_template("addRequest.html")
    # print("hey2")
    return redirect("/login")

@app.route("/getRequests")
def getRequests():
    # if session.get("user") != None:
    info = web.ReturnUserInfo()

    requests = web.ViewArrayRequests()
    print(requests)
    return render_template('getRequests.html', info=info, requests=requests)
    # return redirect('/login')


@app.route('/getRequests/<int:id>')
def approveRequest(id):
    info = web.ReturnUserInfo()
    return render_template('approveid.html', info=info)
    # return redirect('/login')

@app.route('/getRequests/<int:id>', methods=["GET", "POST"])
def approveRequestF(id):
    if session.get("user") != None:
        if request.method == "POST":
            acc = request.form.get("acc")
            key = request.form.get("key")
            info = web.ReturnUserInfo()
            result = web.AccessRequest(acc, key, id)
            print(result)
            if type(result) != str:
                flash("Success!")
            else:
                flash(result)
            return redirect("/lk")
        return render_template("getRequests.html", info=info)
    return  redirect("/login")


@app.route('/removeRequest/<int:id>')
def removeRequest(id):
    info = web.ReturnUserInfo()
    return render_template('removeRequest.html', info=info)
    # return redirect('/login')

@app.route('/removeRequest/<int:id>', methods=["GET", "POST"])
def removeRequestF(id):
    if session.get("user") != None:
        if request.method == "POST":
            acc = request.form.get("acc")
            key = request.form.get("key")
            info = web.ReturnUserInfo()
            result = web.RemoveRequestInArray(acc, key, id)
            print(result)
            if type(result) != str:
                flash("Success!")
            else:
                flash(result)
            return redirect("/lk")
        return render_template("removeRequest.html", info=info)
    return  redirect("/login")



        
@app.route('/logout')
def logout():
    if session.get('user') != None:
        session.pop('user', None)
    return redirect('/login')      



















































if __name__ == "__main__":
    app.run(debug=True, port=8080)