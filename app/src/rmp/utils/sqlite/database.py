import logging
import sqlite3

from typing import List

from rmp.models.models import Teacher, TeacherMeta, Review, ReviewMeta

logging.root.setLevel(logging.DEBUG)


class SqlConnector:
    """Connector which loads local SQLite DB"""

    def __init__(self, db_file: str, table_name: str=None):
        """
        Initialize connector with a local file

        Args:
            db_file - sqllite file containing the teachers. Can be a blank file which will need to be initialized with create_teacher_table
            table_name - table name that will be used to retrive teacher data
        """
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.table_name = table_name
        # weirdy sql returns a list of tuples which wrap strings
        tables = [a[0] for a in self.cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
        print(self.table_name, tables)

        if self.table_name and self.table_name not in tables:
            logging.info(
                f'''Table name {self.table_name} doesn't exist. Creating...''')
            self._create_table(
                self.table_name, Teacher.FIELDS)  # creates the new table if it wasn't present

    def _create_table(self, table_name: str, column_name_type: List[tuple]):
        """Create table with a name and columns

        Args:
            table_name - new table name
            column_name_type - list of tuples with new column names. Looks like [(column name, sql type) , ...]
        """
        self.cursor.execute(f'''CREATE TABLE {table_name}
             ({', '.join([f"{column} {column_type}" for column, column_type in column_name_type])})''')
        self.conn.commit()

    def insert(self, teacher: Teacher):
        '''Insert a teacher into the table.'''
        sql = f''' INSERT INTO {self.table_name}({','.join([f[0] for f in Teacher.FIELDS])})
              VALUES({('?,' * len(Teacher.FIELDS))[:-1]}) '''
        print(sql)
        teacher_dict = teacher.json_serialize()
        print(teacher_dict)
        # assert 1==2
        self.cursor.execute(sql, teacher_dict)
        self.conn.commit()

    def get(self, first, last):
        '''Search for the teacher in the table'''
        self.cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE first='{first}' OR last='{last}'")
        return self.cursor.fetchall()

    def get_all_profs(self):
        self.cursor.execute(
            f"SELECT * FROM {self.table_name}")
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    # default_teach1 = Teacher('Example', 'Teach', 2.5, 'de anza', 'cis', 10, 9, 4.0, TeacherMeta(
    # []), [Review('cis 1', 'awesome', 'good teach', ReviewMeta(3, 3, [], [], 10, 1, 'june 1'))])
    # default_teach2 = Teacher('Example1', 'Teach2', 2.5, 'de anza', 'cis', 10, 9, 4.0, TeacherMeta(
    # []), [Review('cis 1', 'awesome', 'good teach', ReviewMeta(3, 3, [], [], 10, 1, 'june 1'))])

    sql = SqlConnector(
        '/home/taras/Documents/data/rmp/db/teachers.db', 'deanza_big')
    # sql.insert(default_teach1)
    # sql.insert(default_teach2)
    print(len(sql.get_all_profs()))
