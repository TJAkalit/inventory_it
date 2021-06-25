from main                    import app
from staff.Security          import create_user
from staff.Person            import create_person
from staff.Permissions        import create_permission
from staff.Permissions        import add_person_to_permission
from flask                   import g

permissions = {
    "permissions_r": {
        "name": "Разрешения - чтение",
        "obj": None,
    },
    "permissions_rw": {
        "name": "Разрещения - запись",
        "obj": None,
    },
    "users_r": {
        "name": "Пользователи - чтение",
        "obj": None,
    },
    "users_rw": {
        "name": "Пользователи - запись",
        "obj": None,
    },
}

last_name   = "Антипов"
first_name  = "Иван"
middle_name = "Олегович"
login       = "tjakalit"
password    = "123@QAZwsx"

if __name__ == "__main__":
        
    with app.app_context():
        
        g.DBSession = app.config["DBSession"]
        
        new_person = create_person(first_name, last_name, middle_name)
        create_user(login, password, new_person.id)
        
        for perm in permissions:
            
            temp = create_permission(perm, permissions[perm]["name"])
            
            add_person_to_permission(new_person.id, temp.id)
            
        