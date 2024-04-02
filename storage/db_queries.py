CREATE_USER_TABLE = '''
CREATE TABLE IF NOT EXISTS Users 
(
    tg_id INTEGER PRIMARY KEY,
    tg_name TEXT NOT NULL,
    name TEXT NOT NULL,
    lvl  INTEGER NOT NULL
)
'''
CREATE_WORKSHIFTS_TABLE = '''
CREATE TABLE IF NOT EXISTS Workshifts 
(
    wshift_id INTEGER PRIMARY KEY,
    shift_start timestamp,
    shift_end timestamp,
    shift_workers BLOB
)
'''
LOAD_WSHIFT_ID_COUNT = '''SELECT count(wshift_id) FROM Workshifts'''
ADD_WEEKSHIFT = '''INSERT INTO Workshifts (shift_start, shift_end, shift_workers) VALUES (?,?,?)'''
ADD_USER = '''INSERT INTO Users (tg_id, tg_name, name,  lvl ) VALUES (?, ?, ?, ?)'''
LOAD_USERS_FROM_DB = '''SELECT * FROM Users'''
LOAD_SHIFT_BY_ID = '''SELECT * FROM Workshifts WHERE wshift_id =  (?)'''
LOAD_SHIFT_BY_DATE = '''SELECT * from Workshifts where shift_start <= (?) and shift_end >= (?) '''
LOAD_WEEK_ID_BY_DATE = '''SELECT wshift_id from Workshifts where shift_start <= (?) and shift_end >= (?) '''
UPDATE_SHIFT = '''UPDATE Workshifts set shift_workers = (?) where wshift_id = (?) '''
LOAD_LAST_WEEK_STARTDATE = '''SELECT shift_start from Workshifts ORDER by wshift_id DESC'''



