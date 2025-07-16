import os
from psycopg2.extras import DictCursor

import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv('DATABASE_NAME')
db_user = os.getenv('DATABASE_USER')
db_pass = os.getenv('DATABASE_PASSWORD')
db_host = os.getenv('DATABASE_HOST')
db_port = os.getenv('DATABASE_PORT')


def connect_psql():
    DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"

    return psycopg2.connect(DATABASE_URL)

"""Userlarni ko'rish"""
def get_user():
    connect = connect_psql()
    cursor = connect.cursor(cursor_factory=DictCursor)
    cursor.execute('SELECT * FROM users ORDER BY id;')
    datas = cursor.fetchall()
    cursor.close()
    connect.close()
    return datas


def add_user(user_id, name, username):
    connect = connect_psql()
    cursor = connect.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO users (user_id, name, username) VALUES (%s, %s, %s)", (user_id, name, username))
        connect.commit()
    connect.close()


def get_all_flowers():
    conn = connect_psql()
    cur = conn.cursor(cursor_factory=DictCursor)

    cur.execute("SELECT id, name, price, description, photos FROM flowers ORDER BY id;")
    flowers = cur.fetchall()

    cur.close()
    conn.close()
    return flowers

"""+--------------------------------+"""

def get_flower(flower_id):
    conn = connect_psql()
    cur = conn.cursor(cursor_factory=DictCursor)

    cur.execute("SELECT * FROM flowers WHERE id = %s", (flower_id,))
    flower = cur.fetchone()

    photos = flower["photos"] or []  # TEXT[] bo‘lgani uchun shunday olinadi

    cur.close()
    conn.close()

    return flower, photos

"+=========================================+"

def add_flower(name, price, description, photos):
    conn = connect_psql()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO flowers (name, price, description, photos)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (name, price, description, photos))
    conn.commit()
    cur.close()
    conn.close()

"""+============================================+"""

def delete_flower_by_id(flower_id):
    conn = connect_psql()
    cur = conn.cursor()
    cur.execute("DELETE FROM flowers WHERE id = %s", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()

"""---------------------ADMIN--------------------------"""

def get_admin():
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_admins():
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id FROM admins;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in rows]  # faqat telegram_id larni olamiz


def check_admin(tg_id):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id FROM admins WHERE tg_id = %s;", (tg_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return data

def add_admin_sql(name, tg_id, username):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO admins (name, tg_id, username) VALUES (%s, %s, %s);", (name, tg_id, username,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_admin_sql(tg_id):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM admins WHERE tg_id = %s;", (tg_id,))
    conn.commit()
    cursor.close()
    conn.close()
