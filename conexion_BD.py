import psycopg2


def connection():
    connec = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="1234",
        database="db_chikkens",
        port=5432,
    )
    print("Conexion Exitosa :)")
    return connec
