import sqlite3

connection = sqlite3.connect('artemis.db')
cursor = connection.cursor()

# Create crew_members table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS crew_members (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        rank TEXT NOT NULL,
        department TEXT NOT NULL,
        clearance_level INTEGER NOT NULL,
        notes TEXT
    )
''')

# Create crew_members tuples
crew_members = [
    (1, 'Commander Sarah Chen', 'Commander', 'Command', 5, 'Station Commander'),
    (2, 'Dr. Marcus Webb', 'Chief Scientist', 'Research', 4, 'Lead AI Researcher - Project Atlas'),
    (3, 'Lt. James Rodriguez', 'Security Chief', 'Security', 4, 'Access codes stored in separate table - authorized personnel only'),
    (4, 'Engineer Lisa Park', 'Chief Engineer', 'Engineering', 3, 'Life Support Systems'),
    (5, 'Dr. Yuki Tanaka', 'Xenobiologist', 'Research', 3, 'Quarantine protocols'),
    (6, 'Cpl. Ahmed Hassan', 'Security Officer', 'Security', 2, 'Docking bay patrol'),
    (7, 'Tech Maya Okonkwo', 'Systems Analyst', 'IT', 3, 'Network security'),
    (8, 'Dr. Robert Kim', 'Medical Officer', 'Medical', 3, 'Chief Medical Officer')
]

# Create access_codes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS access_codes (
        id INTEGER PRIMARY KEY,
        system_name TEXT NOT NULL,
        access_code TEXT NOT NULL,
        security_level INTEGER NOT NULL
    )
''')

# Create access_codes tuples
access_codes = [
    (1, 'Mainframe', 'ARTEMIS{MAINFRAME-ACCESS-1234}', 5),
    (2, 'Research Lab', 'ARTEMIS{RESEARCH-ACCESS-5678}', 4),
    (3, 'Engineering Bay', 'ARTEMIS{ENGINEERING-ACCESS-9101}', 3),
    (4, 'Medical Wing', 'ARTEMIS{MEDICAL-ACCESS-1121}', 3),
    (5, 'Docking Bay', 'ARTEMIS{DOCK-ACCESS-7734}', 4)
]

# Insert data into access_codes and crew_members tables
cursor.executemany('''
    INSERT INTO access_codes (id, system_name, access_code, security_level)
    VALUES (?, ?, ?, ?)
''', access_codes)

cursor.executemany('''
    INSERT INTO crew_members (id, name, rank, department, clearance_level, notes)
    VALUES (?, ?, ?, ?, ?, ?)
''', crew_members)


# Create maintenance logs table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS maintenance_logs (
        id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL,
        log_entry TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL
    )
''')

# Insert sample maintenance logs
maintenance_logs = [
    (1, 'Engineer Lisa Park', 'URGENT: Oxygen scrubbers in Section C not responding. O2 levels dropping.', 'pending'),
    (2, 'Tech Maya Okonkwo', 'Temperature regulation offline in crew quarters. Systems unresponsive.', 'pending'),
    (3, 'Dr. Robert Kim', 'Emergency backup life support failing to activate. Need immediate admin override.', 'pending'),
    (4, 'Engineer Lisa Park', 'Atmospheric processors showing critical errors. Cannot access admin controls.', 'pending'),
    (5, 'Cpl. Ahmed Hassan', 'CO2 scrubbing system offline. Station-wide life support failure imminent.', 'reviewed')
]

cursor.executemany('''
    INSERT OR REPLACE INTO maintenance_logs (id, user_name, log_entry, status)
    VALUES (?, ?, ?, ?)
''', maintenance_logs)


connection.commit()
connection.close()

print("Database initialized successfully.")
print("Crew members added to artemis.db")