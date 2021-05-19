from flask                     import Flask
from flask                     import request
from flask                     import g
from flask                     import redirect
from flask                     import url_for
from flask                     import render_template

from staff.Engine              import engine
from staff.Security            import create_user, verify_session
from staff.Security            import verify_user
from staff.Security            import make_session
from staff.Security            import revoke_session

from staff.Permissons          import get_permission_list

from staff.Person              import create_person, edit_person, get_person
from staff.Person              import get_all_persons

from sqlalchemy.orm            import sessionmaker

app = Flask(__name__)
app.config["MY_NAME"] = "Inventory_it"
app.config['DBSession'] = sessionmaker(bind = engine)

def logged_in():
    key = request.cookies.get("hash_key", None)
    if not key:
        return None
    return verify_session(key)

def about_user(person_id):
    g.user_permissions = get_permission_list(person_id)
    g.user = get_person(person_id)

@app.route("/")
def index():
    g.DBSession = app.config["DBSession"]
    user = logged_in()
    if not user:
        return redirect(url_for("auth"))
    
    about_user(user.person_id)
    
    return render_template("main.html")

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
    g.DBSession = app.config["DBSession"]
    user = logged_in()
    response = redirect(url_for("auth"))
    
    if user:
        revoke_session(request.cookies.get("hash_key"))
    response.set_cookie("hash_key", "", 0)
    
    return response

@app.route("/directory/")
def directory():
    g.DBSession = app.config["DBSession"]
    user = logged_in()
    if not user:
        return redirect(url_for("auth"))
    
    about_user(user.person_id)
    
    return render_template("directory_root.html")
    
recomended = {
    "person": {
        "fields":[
                    {
                        "code": "last_name",
                        "compulsory": True,
                        "name": "Фамилия",
                    },
                    {
                        "code": "first_name",
                        "compulsory": True,
                        "name": "Имя",
                    },
                    {
                        "code": "middle_name",
                        "compulsory": True,
                        "name": "Отчество",
                    }
                ],
        "get_all_method": get_all_persons,
        "name": "Сотрудники",
        "creation_method": create_person,
        "get_one": get_person,
        "edit_one": edit_person,
    }
}

@app.route("/directory/<string:category>/", methods = ["GET", "POST"])
def directory_concrete(category = None):
    g.DBSession = app.config["DBSession"]
    user = logged_in()
    if not user:
        return redirect(url_for("auth"))
    
    about_user(user.person_id)
    if request.method == "GET":
        if category in recomended:
            g.data = recomended[category]["get_all_method"]()
            g.category = category
            g.recomended = recomended[category]
            g.getattr = getattr
            
            if "create" in request.args:
                g.create_window = True
            elif "element" in request.args:
                
                elem_id:str = request.args.get("element")
                    
                if not elem_id:
                    return redirect(url_for("directory_concrete", category = category))
                
                if not elem_id.isdigit():
                    return redirect(url_for("directory_concrete", category = category))
                
                element = recomended[category]["get_one"](int(elem_id))

                if not element:
                    return redirect(url_for("directory_concrete", category = category))
                
                g.create_window = True
                g.edit_window = True
                g.element = element
                
            else:
                g.toolbar = True
            
            return render_template("directory_persons.html")
        
        return render_template("directory_root.html")
    
    if request.method == "POST":
        
        if category not in recomended:
            return redirect(url_for("directory"))
        
        data = dict()
        for field in recomended[category]["fields"]:
            if field["code"] not in request.form.keys(): 
                return redirect(url_for("directory_concrete", category = category))
        print(*(request.form.get(item["code"]) for item in recomended[category]["fields"]))
        
        new_element = recomended[category]["creation_method"](
            *(request.form.get(item["code"]) for item in recomended[category]["fields"])
        )
        if not new_element:
            return redirect(url_for("directory_concrete", category = category))
        else:
            return redirect(url_for("directory_concrete", category = category)) 

@app.route("/directory/<string:category>/<int:ident>", methods = ["PATCH"])
def directory_edit(category = None, ident = None):
    g.DBSession = app.config["DBSession"]
    user = logged_in()
    if not user:
        return redirect(url_for("auth"))
    
    about_user(user.person_id)
    
    if request.method == "PATCH":
        if category not in recomended:
            return redirect(url_for("directory"))
        
        if ident == 0:
            return redirect(url_for("directory"))
        
        element = recomended[category]["get_one"](ident)
        
        if not element:
            return redirect(url_for("directory_concrete", category = category))
        
        query_data = dict()
        
        for field in recomended[category]["fields"]:
            query_data[field["code"]] = request.form.get(field["code"], None)
        
        result = recomended[category]["edit_one"](ident, **query_data)
        if not result:
            return redirect(url_for("directory_concrete", element = ident))
        
        return redirect(url_for("directory_concrete", element = ident))
        

if __name__ == "__main__":
    
    app.run(
        host = "0.0.0.0",
        port = 8001,
        debug = True,
    )