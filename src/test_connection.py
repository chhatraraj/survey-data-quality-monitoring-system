from src.database.connection import test_connection

if test_connection():
    print("Connected Successfully")
else:
    print("Connection Failed")