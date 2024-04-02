from storage.sqlite_db import SqliteDB
import utility.utility as uti

pswd_adm, pswd_usr, db_name = uti.init_db_cfg()
Storage = SqliteDB(db_name)