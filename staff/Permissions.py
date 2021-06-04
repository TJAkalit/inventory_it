import logging

from flask         import g
from flask.globals import session

from staff.Models  import Permission
from staff.Models  import Person

logger = logging.getLogger("Permissons_backend")
logger.setLevel(100)

class LinkedPermissions(Exception):
    
    __qualname__ = "LinkedPermissions"
    def __str__(self):
        return "Permission is still linked to the persons."    

def create_permission(code, name):
    
    for item in [code, name]:
        if type(item) != str:
            return None
        if item.__len__() <= 4:
            return None
    
    with g.DBSession() as session:
        
        try:
        
            new_permission = Permission(
                name = name,
                code = code,
            )
            session.add(new_permission)
            session.commit()
            return session.query(Permission).filter_by(id = new_permission.id).one()
            
        except Exception as ex:
            
            session.rollback()
            logger.error(("[create_permission] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [code]=[{code}]" +
                         " [name]=[{name}]" +
                         " [{ex}]").format(
                             name = name, code = code, ex = ex,
                         ))
            return None
        
def get_permission(id):
    
    if type(id) != int:
        return None
    
    if id == 0:
        return None
    
    with g.DBSession() as session:
        
        try:
            
            return session.query(Permission).filter_by(id = id).one()
        
        except Exception as ex:
            
            logger.error(("[get_permission] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [id]=[{id}]" +
                         " [{ex}]").format(
                             id = id, ex = ex,
                         ))
            return None
         
def edit_permission(id, name):
    
    if type(id) != int:
        return False
    
    if id == 0:
        return False
    
    if type(name) != str:
        return False
    
    if name.__len__() <= 4:
        return False
    
    with g.DBSession() as session:
        
        try:
            permission = session.query(Permission).filter_by(id = id).one()
            permission.name = name
            session.commit()
            return True
            
        except Exception as ex:
            session.rollback()
            logger.error(("[edit_permission] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [id]=[{id}]" +
                         " [name]=[{name}]" +
                         " [{ex}]").format(
                             id = id, name = name, ex = ex,
                         ))
            return False
            
def delete_permissions(id):
    
    if type(id) != int:
        return False
    
    if id == 0:
        return False
    
    with g.DBSession() as session:
        
        try:
            permission = session.query(Permission).filter_by(id = id).one()
            
            if permission.persons.__len__() != 0:
                raise LinkedPermissions
            session.delete(permission)
            session.commit()
            return True
            
        except Exception as ex:
            session.rollback()
            logger.error(("[delete_permission] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [id]=[{id}]" +
                         " [{ex}]").format(
                             id = id, ex = ex,
                         ))
            return False
        
def add_person_to_permission(person_id, permission_id):
    
    if type(person_id) != int:
        return False
    
    if person_id == 0:
        return False
    
    if type(permission_id) != int:
        return False
    
    if permission_id == 0:
        return False
    
    with g.DBSession() as session:
        
        try:
            
            person = session.query(Person).filter_by(id = person_id).one()
            permission = session.query(Permission).filter_by(id = permission_id).one()
            
            person.permissions.append(permission)
            session.commit()
            return True
        
        except Exception as ex:
                        
            session.rollback()
            logger.error(("[add_person_to_permission] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [person_id]=[{person_id}]" +
                         " [permission_id]=[{permission_id}]" +
                         " [{ex}]").format(
                             person_id = person_id,
                             permission_id = permission_id,
                             ex = ex,
                         ))
            return False
            
def remove_person_from_permission(person_id, permission_id):
    
    if type(person_id) != int:
        return False
    
    if person_id == 0:
        return False
    
    if type(permission_id) != int:
        return False
    
    if permission_id == 0:
        return False
    
    with g.DBSession() as session:
        
        try:
            
            person = session.query(Person).filter_by(id = person_id).one()
            permission = session.query(Permission).filter_by(id = permission_id).one()
            
            person.permissions.remove(permission)
            session.commit()
            return True
        
        except Exception as ex:
                        
            session.rollback()
            logger.error(("[remove_person_from_permission] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [person_id]=[{person_id}]" +
                         " [permission_id]=[{permission_id}]" +
                         " [{ex}]").format(
                             person_id = person_id,
                             permission_id = permission_id,
                             ex = ex,
                         ))
            return False
        
        
def get_permission_list(person_id):

    if type(person_id) != int:
        return None
    
    if person_id == 0:
        return None
    
    with g.DBSession() as session:
        
        try:
            
            person = session.query(Person).filter_by(id = person_id).one()
            return [str(x) for x in person.permissions]
        
        except Exception as ex:
            
            logger.error(("[get_permission_list] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [person_id]=[{person_id}]" +
                         " [{ex}]").format(
                             person_id = person_id,
                             ex = ex,
                         ))
            return None
        
def get_all_permission():
    
    with g.DBSession() as session:
        
        try:
            
            permissions = session.query(Permission).filter_by().all()
            return permissions
        
        except Exception as ex:
            logger.error(("[get_all_permission] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [removed]=[{removed}]" +
                         " [{ex}]").format(
                             ex = ex,
                         ))
            return None