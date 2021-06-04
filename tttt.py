from staff.Models import Person
from staff.Models import Permission
from staff.Person import get_all_persons
from staff.Permissions import get_all_permission

class View():
    
    category = "default"
    model = None
    hidden_fields = list()
    
    def fields(self):
        
        r = dict()
        
        for item in self.model.__dict__["__table__"].__dict__["columns"]:
            
            if item.__dict__["key"] in self.hidden_fields: 
                continue
            
            r[item.__dict__["key"]] = item.__dict__["type"].__str__() if "VARCHAR" not in item.__dict__["type"].__str__() else "VARCHAR"
            
        return r
    
    def name(self):
        return self.naming
    
    def comments(self):
        
        r = dict()
        
        for item in self.model.__dict__["__table__"].__dict__["columns"]:
            
            if item.__dict__["key"] in self.hidden_fields: 
                continue
            
            r[item.__dict__["key"]] = item.__dict__["comment"].__str__()
            
        return r
    
    def get_all(self):
        
        return self.get_meth()

class Person_View(View):
    
    category = "person"
    model = Person
    hidden_fields = ["removed"]
    naming = u"Сотрудники"
    get_meth = lambda x: get_all_persons()
    
class Permission_View(View):
    
    category = "permission"
    model = Permission
    naming = u"Права доступа"
    get_meth = lambda x: get_all_permission()
