#!/bin/bash
export SW_DB_LOGIN=iit   # - env DataBase login
export SW_DB_PASS=iit    # - env DataBase password
export SW_DB_ADDR=localhost   # - env DataBase addres
export SW_TDB_LOGIN=iit  # - env testing DataBase login
export SW_TDB_PASS=iit   # - env testing DataBase password
export SW_TDB_ADDR=localhost  # - env testing DataBase addres

python3.9 /home/tjakalit/git/inventory_it/create_user.py