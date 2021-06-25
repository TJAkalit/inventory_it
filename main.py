from flask                     import Flask
from flask                     import request
from flask                     import g
from flask                     import redirect
from flask                     import url_for
from flask                     import render_template
from flask.helpers import make_response

from staff.Engine              import engine
from staff.Security            import create_user, verify_session
from staff.Security            import verify_user
from staff.Security            import make_session
from staff.Security            import revoke_session

from staff.Permissions          import create_permission
from staff.Permissions          import get_permission_list
from staff.Permissions          import get_all_permission
from staff.Permissions          import get_permission
from staff.Permissions          import edit_permission

from staff.Person              import create_person, edit_person, get_person
from staff.Person              import get_all_persons

from sqlalchemy.orm            import sessionmaker


from staff.Views               import Permission_View, Person_View
# from staff.Views               import Permission_View


app = Flask(__name__)
app.config["MY_NAME"] = "Inventory_it"
app.config['DBSession'] = sessionmaker(bind = engine)

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
    },
    "permission": {
        "fields":[
                    {
                        "code": "name",
                        "compulsory": True,
                        "name": "Название",
                    },
                    {
                        "code": "code",
                        "compulsory": True,
                        "name": "Код",
                    },
        ],
        "get_all_method": get_all_permission,
        "name": "Разрешения",
        "creation_method": create_permission,
        "get_one": get_permission,
        "edit_one": edit_permission,
    },
}

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
    

@app.route("/directory/<string:category>/", methods = ["GET", "POST"])
def directory_concrete(category = None):
    g.DBSession = app.config["DBSession"]
    user = logged_in()
    if not user:
        return redirect(url_for("auth"))
    
    about_user(user.person_id)
    
    mapping = {
        "person": Person_View,
        "permission": Permission_View,
    }
            
    if request.method == "GET":
        if category in mapping:

            view = mapping[category]()
            g.category = category
            g.directory_name = view.naming
            
            g.all_fields = view.all_fields
            g.all_fields_types = view.all_fields_types
            g.all_fields_comments = view.all_fields_comments

            g.table_fields = view.table_fields()

            g.data = view.get_all()
            g.getattr = getattr

            g.toolbar = True
            
            return render_template("directory_persons.html")
        
        return render_template("directory_root.html") 

@app.route("/directory/<string:category>/create.html", methods = ["GET", "POST"], )
def directory_create(category = None,):

    g.DBSession = app.config["DBSession"]
    user = logged_in()
    if not user:
        return redirect(url_for("auth"))
    
    about_user(user.person_id)
    
    mapping = {
        "person": Person_View,
        "permission": Permission_View,
    }
            
    if request.method == "GET":
        if category in mapping:
            view = mapping[category]()

            g.category = category
            g.directory_name = view.naming
            
            g.all_fields = view.all_fields
            g.all_fields_types = view.all_fields_types
            g.all_fields_comments = view.all_fields_comments

            g.table_fields = view.table_fields()
            
            g.data = view.get_all()
            g.getattr = getattr

            g.edit_fields = view.edit_fields()
            g.required_fields = view.required_fields()

            g.toolbar = False
            g.createbar = True
            
            return render_template("directory_persons.html")
        
        return render_template("directory_root.html") 

    if request.method == "POST":
        if category in mapping:

            view = mapping[category]()

            income_keys = {x for x in request.form.keys()}
            req_fields = view.required_fields()


            if not req_fields.issubset(income_keys):

                return "Not enough required keys!"
                
            if income_keys.difference(view.edit_fields()).__len__() != 0:
                return "Can't accept fields that not in object model!"
            
            empty_fields = set()

            for field in req_fields:
                if not request.form.get(field):
                    empty_fields.add(field)

            if empty_fields.__len__() != 0:
                awnser = "Поля {"
                for field in empty_fields:
                    awnser += view.all_fields_comments[field]
                awnser += "} "
                awnser += "не могут быть пустыми."



            info = dict()
            for key in income_keys:
                info[key] = request.form.get(key)

            new_element = view.create_one(info)
            if not new_element:
                return "Can't create element on server side!"

            return make_response(redirect(url_for("directory_edit", category = category, ident = new_element.id)))

        else:
            return make_response("Wrong!", 500)


@app.route("/directory/<string:category>/<int:ident>.html", methods = ["GET", "POST", ])
def directory_edit(category = None, ident = None):
    
    g.DBSession = app.config["DBSession"]
    user = logged_in()
    if not user:
        return redirect(url_for("auth"))
    
    about_user(user.person_id)
    
    mapping = {
        "person": Person_View,
        "permission": Permission_View,
    }
    
    if category in mapping:
        
        if request.method == "GET":
            
            view = mapping[category]()
            g.category = category
            g.directory_name = view.naming
            
            g.all_fields = view.all_fields
            g.all_fields_types = view.all_fields_types
            g.all_fields_comments = view.all_fields_comments

            g.table_fields = view.table_fields()

            g.data = view.get_all()
            g.getattr = getattr

            g.view_fields = view.view_fields()
            g.auto_fields = view.auto_fields
            g.required_fields = view.required_fields()
            
            g.element = view.get_one(ident)

            g.toolbar = False
            
            g.viewbar = True
            
            return render_template("directory_persons.html")
        
        if request.method == "POST":

            view = mapping[category]()
            
            
            income_fields = set(field for field in request.form.keys())
            if not set(view.edit_fields()).issubset(income_fields):

                return "Not enough required keys!"

            if income_fields.difference(view.edit_fields()).__len__() != 0:
                return "Can't accept fields that not in object model!"
            
            empty_fields = set()
            for field in view.required_fields():
                if not request.form.get(field):
                    empty_fields.add(field)

            if empty_fields.__len__() != 0:
                awnser = "Поля {"
                for field in empty_fields:
                    awnser += view.all_fields_comments[field]
                awnser += "} "
                awnser += "не могут быть пустыми."

            info = dict()
            for key in income_fields:
                info[key] = request.form.get(key)
            info["id"] = ident

            edited_elem = view.edit_one(info)
            print(edited_elem)

            if not edited_elem:
                return "Server side failure"

            return make_response(redirect(url_for("directory_edit", category = category, ident = ident)))




            
        
    return "Я хз"
        
        
    
        

if __name__ == "__main__":
    
    app.run(
        host = "0.0.0.0",
        port = 8001,
        debug = True,
    )