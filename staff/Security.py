import logging

from flask         import g
from flask.globals import session

from staff.Models  import User
from staff.Models  import Session

from random        import randint
from datetime      import datetime
from hashlib       import md5 as hash_meth

logger = logging.getLogger("SecurityBackFuncs")

class CONST:
    LOGIN_LEN = 4
    PASS_LEN  = 8


def do_smth():
    
    with g.DBSession() as session:
        
        return session.query(User).all()
    
def create_user(login, password, person_id, ):
    
    if type(login) != str:
        return None

    if login in ("", " ", "_"):
        return None
    
    if login.__len__() <= CONST.LOGIN_LEN:
        return None
    
    if type(password) != str:
        return None

    if password in ("", " ", "_"):
        return None
    
    if password.__len__() <= CONST.PASS_LEN:
        return None
            
    with g.DBSession() as session:
        try:
            new_user = User(
                login = login,
                pass_hash = hash_meth(password.encode("utf-8")).hexdigest(),
                create_date = datetime.now(),
                person_id = person_id,
            )
            session.add(new_user)
            session.commit()
            new_user = session.query(User).filter_by(id = new_user.id).one()
        except Exception as ex:
            logger.error("[create_user] [Exception] [{ex.__class__.__qualname__}] [login]=[{login}] [password]=[{password}] [{ex}]".format(
                ex = ex,
                password = password,
                login = login,
            ))
            session.rollback()
            return None
        else:
            return new_user
        
def verify_user(login, password, **kwargs):
    
    if type(login) != str:
        return None

    if login in ("", " ", "_") and login.__len__() <= CONST.LOGIN_LEN:
        return None
    
    if type(password) != str:
        return None

    if password in ("", " ", "_") and login.__len__() <= CONST.PASS_LEN:
        return None
    
    with g.DBSession() as session:
        try:
            user = session.query(User).filter_by(
                login = login,
                pass_hash = hash_meth(password.encode("utf-8")).hexdigest(),
            ).one()
        except Exception as ex:
            logger.error("[verify_user] [Exception] [{ex.__class__.__qualname__}] [login]=[{login}] [password]=[{password}] [{ex}]".format(
                ex = ex, password = password, login = login,
            ))
            return None
        else:
            return user

def make_session(user):
    
    if type(user) is not User:
        return None
    
    with g.DBSession() as session:
        try:
            hk = (datetime.now().strftime("%Y%m%d%H%M%S%f") + str(randint(1, 1000)) + str(randint(1, 1000))).encode()
            new_session = Session(
                session_hash = hash_meth(
                                    hk
                                ).hexdigest(),
                user_id = user.id,
            )
            session.add(new_session)
            session.commit()
                
        except Exception as ex:
            logger.error("[create_user] [Exception] [{ex.__class__.__qualname__}] [user]=[{user.login}] [{ex}]".format(
                user = user, ex = ex, 
                ))
            session.rollback()
            return None
        else:
            return str(new_session.session_hash)
    
def verify_session(session_hash):

    if type(session_hash) is not str:
        return None
    
    if session_hash in ("", " ", "_", ):
        return None
    
    with g.DBSession() as session:
        
        try:
            user_session = session.query(Session).filter_by(
                session_hash = session_hash,
            ).one()
        except Exception as ex:
            logger.error("[verify_session] [Exception] [{ex.__class__.__qualname__}] [session_hash]=[{session_hash}] [{ex}]".format(
                session_hash = session_hash, ex = ex, 
            ))
            return None
        else:
            return user_session.user
        
def revoke_session(session_hash):
    
    with g.DBSession() as session:
        
        try:
            user_session = session.query(Session).filter_by(
                session_hash = session_hash,
            ).one()
            session.delete(user_session)
            session.commit()
        except Exception as ex:
            logger.error("[revoke_session] [Exception] [{ex.__class__.__qualname__}] [session_has]=[{session_hash}] [{ex}]".format(
                session_hash = session_hash,
            ))
            session.rollback()
            return False
        else:
            return True