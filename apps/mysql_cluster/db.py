import mysql.connector

cnx = mysql.connector.connect(
    user="projectUser", password="ukMULbEQ@;U8B", host="127.0.0.1", database="sakila"
)


def fetch_actors():
    with cnx.cursor() as cursor:
        cursor.execute("SELECT * FROM actor ORDER BY last_update DESC LIMIT 5")
        rows = cursor.fetchall()

    return rows


def add_actor(actor_first_name, actor_last_name, time):
    
    add_new_actor_query = (
            "INSERT INTO actor "
            "(first_name, last_name, last_update) "
            "VALUES (%s, %s, %s)"
        )
    
    data = (actor_first_name, actor_last_name, time)

    with cnx.cursor() as cursor:
        cursor.execute(add_new_actor_query, data)
        cnx.commit()