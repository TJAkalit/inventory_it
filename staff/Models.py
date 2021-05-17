from sqlalchemy.orm             import relationship
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql.expression import null
## # ## # ## # ## # ## # ## #   ## ## # ## # ## # ## # ##
from sqlalchemy.sql.schema      import Column
from sqlalchemy.sql.schema      import ForeignKey
## # ## # ## # ## # ## # ## #   ## ## # ## # ## # ## # ##
from sqlalchemy.sql.sqltypes    import Boolean
from sqlalchemy.sql.sqltypes    import Integer
from sqlalchemy.sql.sqltypes    import VARCHAR
from sqlalchemy.sql.sqltypes    import DateTime
## # ## # ## # ## # ## # ## #   ## ## # ## # ## # ## # ##
from sqlalchemy.ext.declarative import declarative_base
## # ## # ## # ## # ## # ## #   ## ## # ## # ## # ## # ##
Base = declarative_base()
## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ###
class Person(Base):
    __tablename__  = "person"
    __table_args__ = {"schema": "iit"}
    id             = Column("id"          , Integer            , primary_key = True, nullable = False, unique = True , autoincrement = True,                 )
    first_name     = Column("first_name"  , VARCHAR(64)        ,                     nullable = False, unique = False,                                       )
    last_name      = Column("last_name"   , VARCHAR(64)        ,                     nullable = True , unique = False,                                       )
    middle_name    = Column("middle_name" , VARCHAR(64)        ,                     nullable = False, unique = False,                                       )
    removed        = Column("removed"     , Boolean            ,                     nullable = False, unique = False,                      default = False, )
    
    def __str__(self):
        return "{0.last_name} {0.first_name} {0.middle_name}".format(self)
## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ###
class User(Base):
    
    __tablename__  = "user"
    __table_args__ = {'schema': 'iit'}
    id             = Column("id"          , Integer            , primary_key = True, nullable = False, unique = True , autoincrement = True,                 )
    login          = Column("login"       , VARCHAR(64)        ,                     nullable = False, unique = True ,                                       )
    pass_hash      = Column("pass_hash"   , VARCHAR(64)        ,                     nullable = False, unique = False,                                       )
    create_date    = Column("create_date" , DateTime           ,                     nullable = False, unique = False,                                       )
    update_date    = Column("update_date" , DateTime           ,                     nullable = True , unique = False,                                       )
    removed        = Column("removed"     , Boolean            ,                     nullable = False, unique = False,                      default = False, )
    person_id      = Column("person_id"   , ForeignKey(Person.id),                   nullable = False, unique = True ,                                       )
    person         = relationship("Person", backref = "user")
    
    def __repr__(self):
        return "[{0.id}][{0.login}]".format(self)
    
    def __str__(self):
        return "[{0.login}]".format(self)
## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ###
class Session(Base):
    __tablename__  = "session"
    __table_args__ = {'schema': 'iit'}
    id             = Column("id"          , Integer            , primary_key = True, nullable = False, unique = True , autoincrement = True,                 )
    session_hash   = Column("session_hash", VARCHAR(64)        ,                     nullable = False, unique = True ,                                       )
    user_id        = Column("user_id"     , ForeignKey(User.id),                     nullable = False, unique = False,                                       )
    user           = relationship(User    , backref = "session",                                                                                             )
    
    def __repr__(self):
        return "{0.session_hash}".format(self)
    
    def __str__(self):
        return "{0.session_hash}".format(self)
## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ###
class Setting(Base):
    __tablename__  = "settings"
    __table_args__ = {'schema': 'iit'}
    id             = Column("id"          , Integer            , primary_key = True, nullable = False, unique = True , autoincrement = True,                 )
    key            = Column("key"         , VARCHAR(50)        ,                     nullable = False, unique = True ,                                       )
    value          = Column("value"       , VARCHAR(100)       ,                     nullable = False, unique = False,                                       )
    value_type     = Column("value_type"  , Integer            ,                     nullable = False, unique = False,                                       )
    
    def __str__(self):
        return "[{0.key}]=[{0.value_type}][{0.value}]".format(self)
## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ###