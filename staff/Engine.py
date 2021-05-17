from sqlalchemy     import create_engine
import os

# SW_DB_LOGIN  - env DataBase login
# SW_DB_PASS   - env DataBase password
# SW_DB_ADDR   - env DataBase addres
# SW_TDB_LOGIN - env testing DataBase login
# SW_TDB_PASS  - env testing DataBase password
# SW_TDB_ADDR  - env testing DataBase addres

engine = create_engine("postgresql+pg8000://{USER}:{PASS}@{ADDR}/{DB}"\
    .format(
        USER = os.environ["SW_DB_LOGIN"],
        PASS = os.environ["SW_DB_PASS"],
        ADDR = os.environ["SW_DB_ADDR"],
        DB   = "iit"
    ))

test_engine = create_engine("postgresql+pg8000://{USER}:{PASS}@{ADDR}/{DB}"\
    .format(
        USER = os.environ["SW_TDB_LOGIN"],
        PASS = os.environ["SW_TDB_PASS"],
        ADDR = os.environ["SW_TDB_ADDR"],
        DB   = "iit_test"
    ))
