import unittest
from main import app

from staff.Models import Base
from staff.Engine import test_engine
from staff.Person import create_person
from staff.Person import remove_person
from staff.Person import get_person
from staff.Person import edit_person

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
            

if __name__ == "__main__":
    
    unittest.main()