import json
import sqlite3

from rmp.models.models import Teacher, TeacherMeta, Review, ReviewMeta

class SqlConnector:
    
    def __init__(self, db_file, table_name):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.table_name = table_name

    def create_teacher_table(self):
        print(Teacher.FIELDS)
        self._create_table(self.table_name, Teacher.FIELDS)

    def _create_table(self, table_name:str, column_name_type:tuple):
        self.cursor.execute(f'''CREATE TABLE {table_name}
             ({', '.join([f"{column} {column_type}" for column, column_type in column_name_type])})''')
        self.conn.commit()

    def insert(self, teacher:Teacher):
        sql = f''' INSERT INTO {self.table_name}({','.join([f[0] for f in Teacher.FIELDS])})
              VALUES({('?,' * len(Teacher.FIELDS))[:-1]}) '''
        print(sql)
        teacher_dict = teacher.json_serialize()
        print(teacher_dict)
        # assert 1==2
        self.cursor.execute(sql,teacher_dict)
        self.conn.commit()

    def get(self, first, last):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE first='Example'")
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    default_teach1 = Teacher('Example', 'Teach',2.5,'de anza','cis',10,9,4.0,TeacherMeta([]),[Review('cis 1','awesome','good teach',ReviewMeta(3,3,[],[],10,1,'june 1'))])
    default_teach2 = Teacher('Example1', 'Teach2',2.5,'de anza','cis',10,9,4.0,TeacherMeta([]),[Review('cis 1','awesome','good teach',ReviewMeta(3,3,[],[],10,1,'june 1'))])
    sql = SqlConnector('test.db','teachers_de_anza')
    # sql.create_teacher_table()
    # sql.insert(default_teach1)
    # sql.insert(default_teach2)
    print(sql.get('',''))