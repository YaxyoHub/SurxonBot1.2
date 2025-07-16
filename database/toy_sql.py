from .sql import connect_psql


def get_toy():
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, description, photos FROM toys ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    toys = []
    for row in rows:
        toy = {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "description": row[3],
            "photos": row[4].split(",") if row[4] else []
        }
        toys.append(toy)
    return toys


def get_toy_by_id(toy_id):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, description, photos FROM toys WHERE id = %s", (toy_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return None, None

    toy = {
        "id": row[0],
        "name": row[1],
        "price": row[2],
        "description": row[3]
    }
    photos = row[4].split(",") if row[4] else []
    return toy, photos


def add_toy(name, price, description, photos):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO toys (name, price, description, photos) VALUES (%s, %s, %s, %s)",
        (name, price, description, ",".join(photos))
    )
    conn.commit()
    cursor.close()
    conn.close()


def delete_toy(toy_id):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM toys WHERE id = %s", (toy_id,))
    conn.commit()
    cursor.close()
    conn.close()
