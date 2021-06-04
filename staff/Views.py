from staff.Models import Person
from staff.Models import Permission
from staff.Person import get_all_persons, get_person
from staff.Permissions import get_all_permission, get_permission

class View():
    
    category = "default"
    model = None
    hidden_from_fields = list()
    hidden_from_table = list()
    
    def table_fields(self):
        
        r = dict()
        
        for item in self.model.__dict__["__table__"].__dict__["columns"]:
            
            if item.__dict__["key"] in self.hidden_from_table or item.__dict__["key"] in self.hidden_from_fields: 
                continue
            
            r[item.__dict__["key"]] = item.__dict__["type"].__str__() if "VARCHAR" not in item.__dict__["type"].__str__() else "VARCHAR"
            
        return r
    
    def name(self):
        return self.naming
    
    def comments(self):
        
        r = dict()
        
        for item in self.model.__dict__["__table__"].__dict__["columns"]:
            
            if item.__dict__["key"] in self.hidden_from_table or item.__dict__["key"] in self.hidden_from_fields: 
                continue
            
            r[item.__dict__["key"]] = item.__dict__["comment"].__str__()
            
        return r
    
    def get_all(self):
        
        return self.get_meth()
    
    def concrete_fields(self):
        
        return {item.__dict__["key"] for item in self.model.__dict__["__table__"].__dict__["columns"] if item.__dict__["key"] not in self.hidden_from_fields}

class Person_View(View):
    
    category = "person"
    model = Person
    hidden_from_table = []
    hidden_from_fields = ["removed"]
    naming = u"Сотрудники"
    get_meth = lambda x: get_all_persons()
    get_one = lambda x, y: get_person(y)
    
class Permission_View(View):
    
    category = "permission"
    model = Permission
    naming = u"Права доступа"
    get_meth = lambda x: get_all_permission()
    get_one = lambda x, y: get_permission(y)
# print(Person_View().fields())
# print(Permission_View().fields())