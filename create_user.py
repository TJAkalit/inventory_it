from main                    import app
from staff.Security          import create_user
from staff.Person            import create_person
from flask                   import g

if __name__ == "__main__":
    
    
    with app.app_context():
        
        g.DBSession = app.config["DBSession"]
        
        new_person = create_person("Антипов", "Иван", "Олегович")
        
        create_user("tjakalit", "123@QAZwsx", new_person.id)
        