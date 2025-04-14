from database import db

rows = db.fetch_all_matches()
for row in rows:
    print(row)
