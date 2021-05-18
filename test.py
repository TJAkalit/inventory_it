import unittest
from main import app

from staff.Models import Base
from staff.Engine import test_engine
from staff.Person import create_person
from staff.Person import remove_person
from staff.Person import get_person
from staff.Person import edit_person
from staff.Permissons import create_permission
from staff.Permissons import edit_permissions
from staff.Permissons import get_permissions
from staff.Permissons import delete_permissions
from staff.Permissons import add_person_to_permission
from staff.Permissons import remove_person_from_permission
from staff.Permissons import get_permission_list

from sqlalchemy.orm import sessionmaker

from flask import g

from time import sleep

class Test_PersonManupulate(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(test_engine)
    
    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(test_engine)
        
    def test_CreatePerson(self):
        with app.app_context():
            g.DBSession = sessionmaker(bind = test_engine)
            person = create_person(
                "Иван",
                "Иванов",
                "Иванович", 
            )
            with self.subTest(i = "Returning value"):
                self.assertIsNotNone(person)
            
            with self.subTest(i = "Can find person in database"):
                self.assertIsNotNone(get_person(person.id))
            
    def test_EditPerson(self):
        f_n = "Пётр"
        l_n = "Симонов"
        m_n = "Александрович"
        m_n_n = "Сергеевич"
        
        with app.app_context():
            g.DBSession = sessionmaker(bind = test_engine)
            person = create_person(
                f_n, l_n, m_n,
            )
            
            with self.subTest(i = "Wrong value"):
                self.assertFalse(edit_person(person.id, middle_name = "q"))
            with self.subTest(i = "Wrong param"):
                self.assertFalse(edit_person(person.id, main_name = "q1214qwqqfqwf"))
            with self.subTest(i = "Correct"):
                self.assertTrue(edit_person(person.id, middle_name = m_n_n))
                
    def test_RemovePerson(self):
        f_n = "Олег"
        l_n = "Игнатьев"
        m_n = "Александрович"
        
        with app.app_context():
            g.DBSession = sessionmaker(bind = test_engine)
            person = create_person(f_n, l_n, m_n)
            p_id = person.id
                        
            with self.subTest(i = "Create person"):
                self.assertIsNotNone(person)
                
            with self.subTest(i = "Removing"):
            
                self.assertTrue(remove_person(p_id))
            
            with self.subTest(i = "Removed person"):
                self.assertIsNone(get_person(p_id))
            
class Test_Permissions(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(test_engine)
        with app.app_context():
            g.DBSession = sessionmaker(bind = test_engine)
            person = create_person(
                "Иван",
                "Иванов",
                "Иванович", 
            )
            cls.person_id = person.id

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(test_engine)
    
    def test_CreatePermission(self):
        with app.app_context():
            g.DBSession = sessionmaker(bind = test_engine)
            new_perm = create_permission("codeasd", "nameasdasd")
            with self.subTest(i = "creation"):
                self.assertIsNotNone(new_perm)
            
            with self.subTest(i = "getting"):
                perm = get_permissions(new_perm.id)
                self.assertIsNotNone(perm)
                self.assertEqual(get_permissions(new_perm.id).id, new_perm.id)
    
    def test_EditPermission(self):
    
        with app.app_context():
    
            g.DBSession = sessionmaker(bind = test_engine)
            new_perm = create_permission("test_permissions", "Тестирование привилегий")
    
            with self.subTest(i = "creation"):
                self.assertIsNotNone(new_perm)
            
            with self.subTest(i = "getting"):
                perm = get_permissions(new_perm.id)
                self.assertIsNotNone(perm)
                self.assertEqual(get_permissions(new_perm.id).id, new_perm.id)
                
            with self.subTest(i = "editing"):
                perm = edit_permissions(new_perm.id, "Тестирование номер два")
                self.assertTrue(perm)
                self.assertEqual(get_permissions(new_perm.id).name, "Тестирование номер два")
            
    def test_DeletePermissions(self):
        
        with app.app_context():
            g.DBSession = sessionmaker(bind = test_engine)
            new_perm = create_permission("test2_permissions", "Тестовая привилегия")
    
            with self.subTest(i = "creation"):
                self.assertIsNotNone(new_perm)
            
            with self.subTest(i = "getting"):
                perm = get_permissions(new_perm.id)
                self.assertIsNotNone(perm)
                self.assertEqual(get_permissions(new_perm.id).id, new_perm.id)
            
            with self.subTest(i = "deleting with person"):
                self.assertFalse(add_person_to_permission(self.__class__.person_id, perm.id))
                
            with self.subTest(i = "Person permissions before"):
                self.assertEqual(type(get_permission_list(self.__class__.person_id)), list)
                
            with self.subTest(i = "deleting without person"):
                remove_person_from_permission(self.__class__.person_id, perm.id)
                self.assertTrue(delete_permissions(new_perm.id))

if __name__ == "__main__":
    
    unittest.main()