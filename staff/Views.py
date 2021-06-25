from staff.Models import Person
from staff.Models import Permission
from staff.Person import get_all_persons, get_person, create_person, edit_person
from staff.Permissions import get_all_permission, get_permission, create_permission, edit_permission




class View():
    
    category = "default"
    model = None
# Все поля
    all_fields = list()
    all_fields_types = dict()
    all_fields_comments = dict()
# Полностью скрытые поля
    full_hidden = set()
# Поля, которые не отображаются в таблице
    table_hidden = set()
# Поля, которые нельзя изменить
    auto_fields = set()

    def __init__(self):

        self.all_fields = [item.__dict__["key"] for item in self.model.__dict__["__table__"].__dict__["columns"]]
        temp = dict()
        for item in self.model.__dict__["__table__"].__dict__["columns"]:
            temp[item.__dict__["key"]] = item.__dict__["type"].__str__()
        self.all_fields_types = temp

        temp = dict()
        for item in self.model.__dict__["__table__"].__dict__["columns"]:
            temp[item.__dict__["key"]] = item.__dict__["comment"].__str__()

        self.all_fields_comments = temp 

        

    def name(self):
        return self.naming

    def table_fields(self):

        return [item for item in self.all_fields if item not in self.table_hidden and item not in self.full_hidden]
    
    def view_fields(self):
        return [item for item in self.all_fields if item not in self.full_hidden]

    def edit_fields(self):

        return [item for item in self.all_fields if item not in self.full_hidden and item not in self.auto_fields]

    def get_all(self):
        
        return self.get_meth()

    def required_fields(self):

        temp = set()

        for item in self.model.__dict__["__table__"].__dict__["columns"]:

            if item.__dict__["key"] in self.auto_fields or item.__dict__["key"] in self.full_hidden:
                continue

            if item.__dict__["nullable"] == True:
                continue
            else:
                temp.add(item.__dict__["key"])
        return temp

class Person_View(View):
    
    category = "person"
    model = Person
    hidden_from_table = [""]
    hidden_from_fields = ["removed"]
    naming = u"Сотрудники"
    get_meth = lambda x: get_all_persons()
    get_one = lambda x, y: get_person(y)
    create_one = lambda x, y: create_person(y)
    edit_one = lambda x, y: edit_person(y)


    # Полностью скрытые поля
    full_hidden = {"removed"}
    # Поля, которые не отображаются в таблице
    table_hidden = {}
    # Поля, которые нельзя изменить
    auto_fields = {"id"}

class Permission_View(View):

    category = "permission"
    model = Permission
    hidden_from_table = {}
    hidden_from_fields = {}
    naming = u"Права доступа"
    get_meth = lambda x: get_all_permission()
    get_one = lambda x, y: get_permission(y)
    create_one = lambda x, y: create_permission(y)
    edit_one = lambda x, y: edit_permission(y)

    # Полностью скрытые поля
    full_hidden = {}
    # Поля, которые не отображаются в таблице
    table_hidden = {}
    # Поля, которые нельзя изменить
    auto_fields = {"id"}