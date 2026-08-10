import mysql.connector

# Connect to MySQL server (default port 3306)
conn = mysql.connector.connect(
    host="localhost",       # or your server IP
    user="root",            # replace with your MySQL username
    password="!wmo!26211317pw"  # replace with your MySQL password
)

# Create a cursor object
cursor = conn.cursor()

# Create a new database (if not exists)
cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce_db")

# Connect specifically to the new database
conn.database = "ecommerce_db"




