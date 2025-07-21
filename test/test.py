import uuid
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

# --- Setup ---
# Using an in-memory database for this example, but it works the same with a file.
db = TinyDB(storage=MemoryStorage)
users_table = db.table('users')

print("--- Method 1: Using TinyDB's Automatic doc_id ---\n")

# Insert a user and capture the returned doc_id
print("Inserting 'Alice'...")
alice_data = {'name': 'Alice', 'email': 'alice@example.com'}
alice_id = users_table.insert(alice_data)

print(f"✅ 'Alice' was inserted with TinyDB's auto-generated doc_id: {alice_id}")
print(f"Type of this ID is: {type(alice_id)}\n")