import psycopg2.extras
from werkzeug.security import check_password_hash, generate_password_hash

from app.utils import check_email


class CRUDUser:
    def __get_by_username(self, conn, username):
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
            SELECT * FROM users WHERE username = %s;
            """
            cur.execute(sql, (username,))
            user = cur.fetchone()
            return user

    def __get_by_email(self, conn, email):
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
            SELECT * FROM users WHERE email = %s;
            """
            cur.execute(sql, (email,))
            user = cur.fetchone()
            return user

    def create(self, conn, username, email, password):
        with conn.cursor() as cur:
            if len(username.split()) > 1:
                return "Spaces are not allowed in the username"
            elif len(username) > 32:
                return "Maximum length of the username is 32 characters"
            elif len(email) > 64:
                return "Maximum length of the email is 64 characters"
            elif len(password) < 12 or len(password) > 256:
                return "Password must be between 12 and 256 characters"
            elif not check_email(email):
                return "Not a valid email address"
            elif self.__get_by_username(conn, username):
                return "Username unavailable"
            elif self.__get_by_email(conn, email):
                return "Email unavailable"
            sql = """
            INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s)
            """
            values = username, email, generate_password_hash(password)
            cur.execute(sql, values)
            conn.commit()
            return None

    def read(self, conn, username):
        user = self.__get_by_username(conn, username)
        return user

    def authenticate(self, conn, username, password):
        user = self.__get_by_username(conn, username)
        if not user:
            return "Could not validate credentials"
        hashed_password = user.get("hashed_password")
        if not check_password_hash(hashed_password, password):
            return "Could not validate credentials"
        return None


crud_user = CRUDUser()
