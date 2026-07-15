from src.database.connection import test_connection

print("=" * 50)
print("Database Connection Test")
print("=" * 50)

if test_connection():
    print("✓ Connected Successfully")
else:
    print("✗ Connection Failed")