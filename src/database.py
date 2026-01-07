import sqlite3
from pathlib import Path

class Database:
    def __init__(self, db_path:  str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def initialize_schema(self, schema_path: str = "schema.sql"):
        """Execute schema SQL file"""
        # Drop existing tables if they exist
        self.conn.execute("DROP TABLE IF EXISTS task_tags")
        self.conn.execute("DROP TABLE IF EXISTS attachments")
        self.conn.execute("DROP TABLE IF EXISTS custom_field_values")
        self.conn.execute("DROP TABLE IF EXISTS custom_field_definitions")
        self.conn.execute("DROP TABLE IF EXISTS comments")
        self.conn.execute("DROP TABLE IF EXISTS tasks")
        self.conn.execute("DROP TABLE IF EXISTS sections")
        self.conn.execute("DROP TABLE IF EXISTS projects")
        self.conn.execute("DROP TABLE IF EXISTS team_memberships")
        self.conn.execute("DROP TABLE IF EXISTS teams")
        self.conn.execute("DROP TABLE IF EXISTS users")
        self.conn.execute("DROP TABLE IF EXISTS tags")
        self.conn.execute("DROP TABLE IF EXISTS organizations")
        self.conn.commit()
        
        with open(schema_path, 'r') as f:
            schema = f.read()
        self.conn.executescript(schema)
        self.conn.commit()
        print("✓ Database schema initialized")
    
    def insert_batch(self, table:  str, rows: list[dict]):
        """Insert multiple rows efficiently"""
        if not rows:
            return
        
        columns = rows[0].keys()
        placeholders = ','.join(['?' for _ in columns])
        query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
        
        values = [tuple(row[col] for col in columns) for row in rows]
        self. conn.executemany(query, values)
        self.conn.commit()
        print(f"✓ Inserted {len(rows)} rows into {table}")
    
    def close(self):
        if self.conn:
            self.conn.close()