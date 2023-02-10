import mysql.connector as mydb
import os

table_names = ["Face_Pictures", "RightEye_Pictures", "LeftEye_Pictures" ,"Mouth_Pictures" ,"Nose_Pictures"]
table_dict = {'face' : 'Face_Pictures', 'eyeright' : 'EyeRight_Pictures', 'eyeleft' : 'EyeLeft_Pictures', 'mouth' : 'Mouth_Pictures', 'nose' : 'Nose_Pictures'}
db_dict = {'temp' : 'Temp_Data', 'main' : 'Main_Data'}

class mydatabase:
    def __init__(self, db_selected):
        self.conn = mydb.connect(
            host = "localhost",
            user = "root",
            password = "",
            port='3306',
        )
        self.conn.ping(reconnect=True)
        self.cur = self.conn.cursor()
        self.connect_db(db_selected=db_selected)

    def Deleteinitalize(self):
        query = self.cur.execute("DROP DATABASE IF EXISTS `Temp_Data`")
        self.cur.execute(query)
        self.conn.commit()
    
    def disconnect_db(self):
        self.cur.close()
        self.conn.close()

    def connect_db(self,db_selected):
        database_cur = db_dict[db_selected]
        # コネクションの作成

        # コネクションが切れた時に再接続してくれるよう設定
        self.conn.ping(reconnect=True)
        blank = ""

        # 接続できているかどうか確認
        print(self.conn.is_connected())

        self.cur = self.conn.cursor()

        if(database_cur == 'Temp_Data'):
            # self.cur.execute("DROP DATABASE IF EXISTS `Temp_Data`")
            self.cur.execute("CREATE DATABASE IF NOT EXISTS `Temp_Data`")
            self.cur.execute("USE `Temp_Data`")
        elif(database_cur == 'Main_Data'):
            self.cur.execute("CREATE DATABASE IF NOT EXISTS `Main_Data`")
            self.cur.execute("USE `Main_Data`")

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS `Face_Pictures` (
            `Pic_ID` int(11) auto_increment primary key,
            `file_path` varchar(255) not null,
            `second_path` varchar(255) not null,
            `ev_toggle` int(11) not null
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS `EyeRight_Pictures` (
            `Pic_ID` int(11) auto_increment primary key,
            `file_path` varchar(255) not null,
            `coor_x` int(11) not null,
            `coor_y` int(11) not null,
            `ev_toggle` int(11) not null
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS `EyeLeft_Pictures` (
            `Pic_ID` int(11) auto_increment primary key,
            `file_path` varchar(255) not null,
            `coor_x` int(11) not null,
            `coor_y` int(11) not null,
            `ev_toggle` int(11) not null
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS `Mouth_Pictures` (
            `Pic_ID` int(11) auto_increment primary key,
            `file_path` varchar(255) not null,
            `coor_x` int(11) not null,
            `coor_y` int(11) not null,
            `ev_toggle` int(11) not null
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS `Nose_Pictures` (
            `Pic_ID` int(11) auto_increment primary key,
            `file_path` varchar(255) not null,
            `coor_x` int(11) not null,
            `coor_y` int(11) not null,
            `ev_toggle` int(11) not null
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            """
        )
        
        self.conn.commit()
        print('connected')

    #データベースにデータを登録する、INSERTを使用する
    def database_insert(self, table_selected=0, file_path="", second_path="", coor_x=0, coor_y=0):
        #table_numは1から
        table_selected_name = table_dict[table_selected]
        print(table_selected_name)
        if(table_selected == 'face'):
            query = str("INSERT INTO " + table_selected_name + "(`file_path`, `second_path`) VALUES(%s, %s)")
            self.cur.execute(query, (file_path, second_path))
        elif(table_selected == 'eyeright'):
            query = str("INSERT INTO " + table_selected_name + "(`file_path`, `coor_x`, `coor_y`) VALUES(%s, %s, %s)")
            self.cur.execute(query, (file_path, coor_x, coor_y))
        elif(table_selected == 'eyeleft'):
            query = str("INSERT INTO " + table_selected_name + "(`file_path`, `coor_x`, `coor_y`) VALUES(%s, %s, %s)")
            self.cur.execute(query, (file_path, coor_x, coor_y))
        elif(table_selected == 'mouth'):
            query = str("INSERT INTO " + table_selected_name + "(`file_path`, `coor_x`, `coor_y`) VALUES(%s, %s, %s)")
            self.cur.execute(query, (file_path, coor_x, coor_y))
        elif(table_selected == 'nose'):
            query = str("INSERT INTO " + table_selected_name + "(`file_path`, `coor_x`, `coor_y`) VALUES(%s, %s, %s)")
            self.cur.execute(query, (file_path, coor_x, coor_y))
        self.conn.commit()

def Deletedatabase(db_selected):
    db_ins = mydatabase(db_selected = db_selected)
    db_ins.Deleteinitalize()
    db_ins.disconnect_db()
    # query = self.cur.execute("DROP DATABASE IF EXISTS `Temp_Data`")
    # self.cur.execute(query)


def readfile_db(db_selected):
    db_ins = mydatabase(db_selected=db_selected)
    data_file = open('data.txt', 'r')
    data_lines = data_file.readlines()
    for i in range(len(data_lines)):
        data_split = data_lines[i].split(' ')
        table_selected = data_split[0]
        file_path = data_split[1]
        data_count = len(data_split)
        #print(data_count)
        #データ数によって引数のオプションを変える、顔画像のテーブルは切り出し画像と加工画像
        if data_count == 4:
            coor_x = data_split[2]
            coor_y = data_split[3]
            db_ins.database_insert(table_selected=table_selected, coor_x=coor_x, coor_y=coor_y, file_path=file_path)
        elif data_count == 3:
            second_path = data_split[2]
            db_ins.database_insert(table_selected=table_selected, file_path=file_path, second_path=second_path)
    db_ins.disconnect_db()

def database_input(db_selected=0, table_selected=0, coor_x=0, coor_y=0, file_path="", second_path=""):
    if(db_selected != 0):
        db_name = db_selected
        db_ins = mydatabase(db_name)
    db_ins = mydatabase(db_selected=db_selected)
    db_ins.database_insert(table_selected=table_selected, file_path=file_path, second_path=second_path, coor_x=coor_x, coor_y=coor_y)
    db_ins.disconnect_db()

if __name__ == '__main__':
    readfile_db('main')
    print('end')