import psycopg2.extras


class CRUDTask:
    def __get_by_owner_id(self, conn, owner_id):
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
            SELECT * FROM tasks WHERE created_by = %s;
            """
            cur.execute(sql, (owner_id,))
            tasks = cur.fetchall()
            return tasks

    def __get_by_title(self, conn, title):
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
            SELECT * FROM tasks WHERE title = %s;
            """
            cur.execute(sql, (title,))
            task = cur.fetchone()
            return task

    def create(self, conn, owner_id, title, description):
        if self.__get_by_title(conn, title):
            return "Title unavailable"
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
            INSERT INTO tasks (title, description, created_by)
            VALUES (%s, %s, %s);
            """
            values = (title, description, owner_id)
            cur.execute(sql, values)
            conn.commit()
            return None

    def read(self, conn, owner_id):
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
            SELECT * FROM tasks WHERE created_by = %s ORDER BY id ASC;
            """
            cur.execute(sql, (owner_id,))
            tasks = cur.fetchall()
            return tasks

    def update(self, conn, owner_id, current_title, new_title, new_description):
        task = self.__get_by_title(conn, current_title)
        if not task:
            return "Task does not exist"
        elif task["created_by"] != owner_id:
            return "Task does not exist"
        if self.__get_by_title(conn, new_title):
            return "New title unavailable"
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
            UPDATE tasks
            SET title = %s,
                description = %s
            WHERE created_by = %s AND title = %s;
            """
            values = (new_title, new_description, owner_id, current_title)
            cur.execute(sql, values)
            conn.commit()
            return None

    def delete(self, conn, owner_id, title):
        task = self.__get_by_title(conn, title)
        if not task:
            return "Task does not exist"
        elif task["created_by"] != owner_id:
            return "Task does not exist"
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            sql = """
            DELETE FROM tasks WHERE created_by = %s AND title = %s;
            """
            values = (owner_id, title)
            cur.execute(sql, values)
            conn.commit()
            return None


crud_task = CRUDTask()
