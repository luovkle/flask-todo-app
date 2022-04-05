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
        if len(title) > 32:
            return "Maximum length of the title is 32 characters"
        elif len(description) > 128:
            return "Maximum length of the description is 128 characters"
        elif self.__get_by_title(conn, title):
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

    def read(self, conn, owner_id, title=None):
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if title:
                sql = """
                SELECT * FROM tasks WHERE created_by = %s AND title = %s;
                """
                values = (owner_id, title)
                cur.execute(sql, values)
                task = cur.fetchone()
                return task
            else:
                sql = """
                SELECT * FROM tasks WHERE created_by = %s ORDER BY id ASC;
                """
                cur.execute(sql, (owner_id,))
                tasks = cur.fetchall()
                return tasks

    def update(self, conn, owner_id, current_title, new_title, new_description):
        if len(new_title) > 32:
            return "Maximum length of the title is 32 characters"
        elif len(new_description) > 128:
            return "Maximum length of the description is 128 characters"
        task = self.__get_by_title(conn, current_title)
        if not task:
            return "Task does not exist"
        elif task["created_by"] != owner_id:
            return "Task does not exist"
        if self.__get_by_title(conn, new_title) and current_title != new_title:
            return "New title unavailable"
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if current_title != new_title and task["description"] != new_description:
                sql = """
                UPDATE tasks
                SET title = %s,
                    description = %s
                WHERE created_by = %s AND title = %s;
                """
                values = (new_title, new_description, owner_id, current_title)
            elif current_title != new_title and task["description"] == new_description:
                sql = """
                UPDATE tasks
                SET title = %s
                WHERE created_by = %s AND title = %s;
                """
                values = (new_title, owner_id, current_title)
            elif current_title == new_title and task["description"] != new_description:
                sql = """
                UPDATE tasks
                SET description = %s
                WHERE created_by = %s AND title = %s;
                """
                values = (new_description, owner_id, current_title)
            elif current_title == new_title and task["description"] == new_description:
                return None
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
