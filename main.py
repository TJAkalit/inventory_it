from staff.Person import get_person
from flask                     import Flask
from flask                     import request
from flask                     import g
from flask                     import redirect
from flask                     import url_for
from flask                     import render_template

from staff.Engine              import engine
from staff.Security            import verify_session
from staff.Security            import verify_user
from staff.Security            import make_session
from staff.Security            import revoke_session

from sqlalchemy.orm            import sessionmaker

app = Flask(__name__)
app.config["MY_NAME"] = "Inventory_it"
app.config['DBSession'] = sessionmaker(bind = engine)

def logged_in():
    key = request.cookies.get("hash_key", None)
    if not key:
        return None
    return verify_session(key)

@app.route("/")
def index():
    g.DBSession = app.config["DBSession"]
    user = logged_in()
    if not user:
        return redirect(url_for("auth"))
    g.user = get_person(user.person_id)
    
    return render_template("main.html")
    return "Hello, {}! from {}<br>Have a nice day!".format(
        get_person(user.person_id).first_name,
        app.config["MY_NAME"]
    )

@app.route("/auth/", methods = ["GET", "POST", ])
def auth():
    
    MAIN_TEMPLATE = "auth.html"
    
    g.DBSession = app.config["DBSession"]
    user = logged_in()
    
    if user:
        return redirect(url_for("index"))
    
    if request.method == "GET":
        return render_template(MAIN_TEMPLATE)    
        
    
    if request.method == "POST":
        login    = request.form.get("login")
        password = request.form.get("password")
        if not login or not password:
            return render_template(MAIN_TEMPLATE)
        
        user = verify_user(login, password)
        
        if not user:
            return render_template(MAIN_TEMPLATE)

        hash_key = make_session(user)
        
        response = redirect(url_for("index"))
        response.set_cookie("hash_key", hash_key)
        return response
    
@app.route("/auth/logout/")
def logout():
    
    user = logged_in()
    response = redirect(url_for("auth"))
    
    if user:
        revoke_session(request.cookies.get("hash_key"))
    response.set_cookie("hash_key", "", 0)
    
    return response
    
    
if __name__ == "__main__":
    
    app.run(
        host = "0.0.0.0",
        port = 8001,
        debug = True,
    )