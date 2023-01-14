import mysql.connector

class MariaDB:
    def __init__(self) -> None:
        pass

    def MysqlConnector(self):
        self.mydb = mysql.connector.connect(        
            host = "localhost",
            user = "root",
            password = "",
            database = "unityserver"
        )

    def InsertDataFace(self, file_path, coor_X, coor_Y):
        self.MysqlConnector()

        self.Mycursor = self.mydb.cursor()
        sql = "INSERT INTO face (filename, coor_x, coor_y) values (%s, %s, %s)"
        data_user = (file_path, coor_X, coor_Y)

        self.Mycursor.execute(sql, data_user)
        self.CloseDatabase_Cursor()

    def InsertDataPath(self, file_path, coor_X, coor_Y):
        self.MysqlConnector()

        self.Mycursor = self.mydb.cursor()
        sql = "INSERT INTO facepath (filename, coor_x, coor_y) values (%s, %s, %s)"
        data_user = (file_path, coor_X, coor_Y)

        self.Mycursor.execute(sql, data_user)
        self.CloseDatabase_Cursor()

    def CloseDatabase_Cursor(self):
        self.mydb.commit()
        self.Mycursor.close()
        self.mydb.close()