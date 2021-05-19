import logging

from flask         import g
from flask.globals import session

from staff.Models  import Person

logger = logging.getLogger("Person_backend")
logger.setLevel(0)

def create_person(last_name, first_name, middle_name, ):
    
    for item in [first_name, last_name, middle_name]:
        
        if not item:
            return None
        if type(item) is not str:
            return None    
        if item.__len__() < 2:
            return None
        
    with g.DBSession() as session:
        
        try:
        
            new_person = Person(
                first_name = first_name, last_name = last_name, 
                middle_name = middle_name, 
            )
            
            session.add(new_person)
            session.commit()
            return session.query(Person).filter_by(id = new_person.id).one()
            
        except Exception as ex:
            
            session.rollback()
            logger.error(("[create_person] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [first_name]=[{first_name}]" +
                         " [last_name]=[{last_name}]" + 
                         " [middle_name]=[{middle_name}]" + 
                         " [{ex}]").format(
                             first_name = first_name,
                             last_name = last_name,
                             middle_name = middle_name,
                         ))
            return None
        
def edit_person(id, **kwargs):
    
    if type(id) is not int:
        return False
    
    for name in kwargs:

        if name not in ["first_name", "last_name", "middle_name", ]:
            return False
    
    for name in kwargs:
        if not kwargs[name]:
            return False
        if type(kwargs[name]) is not str:
            return False   
        if kwargs[name].__len__() < 2 :
            return False           
    
    with g.DBSession() as session:
        
        try:
            person = session.query(Person).filter_by(id = id, removed = False).one()
            for name in kwargs:
                setattr(person, name, kwargs[name])
            session.commit()
        
        except Exception as ex:
            
            logger.error(("[edit_person] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [id]=[{id}] [data]=[{data}] [{ex}]").format(
                             data = kwargs, id = id, ex = ex,
                         ))
            return False

        else:
            return True
        
def remove_person(id):
    
    if type(id) is not int:
        return False
    
    with g.DBSession() as session:
        
        try:
            person = session.query(Person).filter_by(id = id, removed = False, ).one()
            person.removed = True
            session.commit()
            
        except Exception as ex:
            session.rollback()
            logger.error(("[remove_person] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [id]=[{id}] [{ex}]").format(
                             id = id, ex = ex, 
                         ))
            return False
        else:
            logger.info(("[remove_person] [Success!] [{id}][{person}] marked as removed!").format(
                             id = person.id, person = person,  
                         ))
            return True
            
def get_person(id):
    
    if type(id) is not int:
        return None
    
    with g.DBSession() as session:
        
        try:
            person = session.query(Person).filter_by(id = id, removed = False, ).one()

        except Exception as ex:
            logger.error(("[get_person] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [id]=[{id}] [{ex}]").format(
                             id = id, ex = ex,
                         ))
            return None
            
        else:
            return person
        
def get_all_persons(removed = False):
    
    with g.DBSession() as session:
        
        try:
            result = session.query(Person).filter_by(removed = removed, ).order_by(Person.id).all()
            return result
        
        except Exception as ex:
            logger.error(("[get_all_persons] [Exception] [{ex.__class__.__qualname__}]" + 
                         " [removed]=[{removed}] [{ex}]").format(
                             removed = removed, ex = ex,
                         ))
            return None
            