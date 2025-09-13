try:
    conn = psycopg2.connect(
        host='localhost', database='fastapi', user='postgres', password='Sanchez7', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connected successfuly!")
except Exception as error:
    print("connection failed The error was ", error)
