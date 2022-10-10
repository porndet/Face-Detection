import mysql.connector

class MariaDB:
    def __init__(self) -> None:
        pass

    def MysqlConnector(self):
        self.mydb = mysql.connector.connect(        
            host = "localhost",
            user = "root",
            password = "",
            database = "systemsecurity"
        )

    def InsertData(self, Data, Data2, Data3):
        self.MysqlConnector()

        self.Mycursor = self.mydb.cursor()
        sql = "INSERT INTO record (speed, distance, date) values (%s, %s, %s)"
        data_user = (Data, Data2, Data3)

        self.Mycursor.execute(sql, data_user)

        self.CloseDatabase_Cursor()

    def CloseDatabase_Cursor(self):
        self.mydb.commit()
        self.Mycursor.close()
        self.mydb.close()



# mydb = mysql.connector.connect(
#   host = "localhost",
#   user = "root",
#   password = "",
#   database = "systemsecurity"
# )

# mycursor = mydb.cursor()

# test1 = 1
# test2 = 2
# test3 = "2022-09-13 11:46:10"

# data_user = (test1, test2, test3)

# sql = "INSERT INTO record (speed, distance, date) values (%s, %s, %s)"
# data_user = (float(test1), float(test2), test3)
# mycursor.execute(sql, data_user)

# mydb.commit()
# mycursor.close()
# mydb.close()