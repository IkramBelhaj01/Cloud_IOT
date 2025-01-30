from psycopg2 import connect
from psycopg2.extensions import connection
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class User:
    email: str
    password: str

def create_connection() -> connection:
    """Crée une connexion à la base de données PostgreSQL"""
    try:
        cnx = connect(
            host='db',
            user='admin',
            password='1234',
            database='db_ms'
        )
        return cnx
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

def get_user_by_email(email: str):
    """Récupère un utilisateur par email"""
    conn = create_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT email, password FROM T_USER WHERE email = %s", (email,))
        user = cur.fetchone()
        conn.close()
        return User(email=user[0], password=user[1]) if user else None
    return None

def create_user(email: str, password: str):
    """Ajoute un nouvel utilisateur"""
    conn = create_connection()
    if conn:
        cur = conn.cursor()
        hashed_password = generate_password_hash(password)
        try:
            cur.execute("INSERT INTO T_USER (email, password) VALUES (%s, %s)", (email, hashed_password))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de l'insertion : {e}")
            return False
        finally:
            conn.close()
    return False
