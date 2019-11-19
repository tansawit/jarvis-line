import sqlite3
from datetime import datetime

conn = sqlite3.connect("showing.db")
c = conn.cursor()
# Last Fetch + General Stats
try:
    c.execute("CREATE TABLE IF NOT EXISTS showingStats(lastChecked TEXT)")

    c.execute("CREATE INDEX IF NOT EXISTS fastlastChecked ON showingStats(lastChecked)")
    current_time = str(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    c.execute("INSERT INTO showingStats (lastChecked) VALUES (?)", (current_time,))
    conn.commit()
except Exception as e:
    print(str(e))

# Movie List + Info
try:
    c.execute("CREATE TABLE IF NOT EXISTS "
              "showing(name TEXT, movieUrl TEXT, posterUrl TEXT, releaseDate TEXT, desc TEXT, "
              "UNIQUE(name))")

    c.execute("CREATE INDEX IF NOT EXISTS fast_name ON showing(name)")
    c.execute("CREATE INDEX IF NOT EXISTS fast_movieUrl ON showing(movieUrl)")
    c.execute("CREATE INDEX IF NOT EXISTS fast_posterUrl ON showing(posterUrl)")
    c.execute("CREATE INDEX IF NOT EXISTS fast_releaseDate ON showing(releaseDate)")
    c.execute("CREATE INDEX IF NOT EXISTS fast_desc ON showing(desc)")

    conn.commit()
except Exception as e:
    print(str(e))
