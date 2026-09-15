import sqlite3, json
DB = "gen_id.db"

def conn(): return sqlite3.connect(DB)

def init_db():
    c=conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS cases(case_id TEXT PRIMARY KEY, incident TEXT, date TEXT, location TEXT);
    CREATE TABLE IF NOT EXISTS unknowns(id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT, sample_id TEXT, quality TEXT, profile TEXT);
    CREATE TABLE IF NOT EXISTS refs(id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT, family_id TEXT, ref_id TEXT, relationship TEXT, profile TEXT);
    """)
    c.commit(); c.close()

def save_case(cid,incident,date,location):
    c=conn(); c.execute("INSERT OR REPLACE INTO cases VALUES(?,?,?,?)",(cid,incident,date,location)); c.commit(); c.close()

def save_unknown(case_id,sample_id,quality,profile):
    c=conn(); c.execute("INSERT INTO unknowns(case_id,sample_id,quality,profile) VALUES(?,?,?,?)",(case_id,sample_id,quality,json.dumps(profile))); c.commit(); c.close()

def save_reference(case_id,family_id,ref_id,relationship,profile):
    c=conn(); c.execute("INSERT INTO refs(case_id,family_id,ref_id,relationship,profile) VALUES(?,?,?,?,?)",(case_id,family_id,ref_id,relationship,json.dumps(profile))); c.commit(); c.close()

def get_cases():
    c=conn(); x=c.execute("SELECT * FROM cases").fetchall(); c.close(); return x

def get_unknowns():
    c=conn(); x=c.execute("SELECT id,sample_id,case_id,quality,profile FROM unknowns").fetchall(); c.close()
    return [(r[0],r[1],r[2],json.loads(r[4]),r[3]) for r in x]

def get_references():
    c=conn(); x=c.execute("SELECT id,family_id,ref_id,relationship,profile FROM refs").fetchall(); c.close()
    return [(r[0],r[1],r[2],r[3],json.loads(r[4])) for r in x]
