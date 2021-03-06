import mysql.connector
import hashlib

'''
Class to manage all database access
'''


class DatabaseManager:
    def __init__(self, host, databaseName, username, password=None):

        # self.mydb = mysql.connector.connect(
        #     host="sql12.freemysqlhosting.net",
        #     user="sql12269310",
        #     passwd="sc4Jm8WSRj",
        #     database="sql12269310"
        # )

        self.mydb = mysql.connector.connect(
            host=host,
            user=username,
            passwd=password,
            database=databaseName
        )


        self.designationTableName = "designations"
        self.employeeTableName = "employees"
        self.loginTablename = "login"

        self.mycursor = self.mydb.cursor()

    def checkLogin(self, username, password):
        # if username == "admin" and password == "1234":
        #     return True
        # return False
        self.mycursor.execute("SELECT password FROM " + self.loginTablename + " WHERE username = %s", (username,))
        pswd = self.mycursor.fetchone()
        if pswd is not None and hashlib.sha256(password).digest() == pswd[0]:
            return True
        return False

    def addLogin(self, username, password):
        hashpass = hashlib.sha256(password).digest()
        self.mycursor.execute("INSERT INTO " + self.loginTablename + " VALUES(%s, %s)", (username, hashpass))
        self.mydb.commit()

    def addEmployee(self, id, name, designation, originalPay, originalPayGrade, doj, pan):
        insert = "INSERT INTO " + self.employeeTableName + " VALUES(%s, %s, %s, %s, %s, %s, %s)"

        self.mycursor.execute(insert, (id, name, designation, originalPay, originalPayGrade, doj, pan))
        self.mydb.commit()

    # Edited by Sattam
    def delEmployee(self, id, name):
        command = "DELETE FROM " + self.employeeTableName + " WHERE ID = %s"
        self.mycursor.execute(command, (id,))
        self.mydb.commit()

    def editEmployee(self, id, name, designation, originalPay, originalPayGrade, doj, pan):
        command = "UPDATE " + self.employeeTableName + " " + \
                  "SET name = %s, " + \
                  "Designation = %s, " + \
                  "OriginalPay = %s, " + \
                  "OriginalGradePay = %s, " + \
                  "DOJ = %s, " + \
                  "Pan = %s " + \
                  "WHERE ID = %s"
        print command
        self.mycursor.execute(command, (name, designation, originalPay, originalPayGrade, doj, pan, id))
        self.mydb.commit()

    def changeDetail(self, id, field, newText):
        print "id=", id
        print "field=", field
        command = "update " + self.employeeTableName + " set " + field + " = %s where ID = %s"
        print "command=", command
        self.mycursor.execute(command, (newText, id))
        self.mydb.commit()

    def getEmployeeNameList(self):
        self.mycursor.execute("SELECT DISTINCT name FROM " + self.employeeTableName)
        list = [str(x[0]) for x in self.mycursor.fetchall()]
        list.sort()
        return list

    def getIdListForName(self, name):
        command = "SELECT ID FROM " + self.employeeTableName + " WHERE name = %s"
        self.mycursor.execute(command,(name,))
        list = [str(x[0]) for x in self.mycursor.fetchall()]
        return list

    def getEmployeeInfo(self, id):
        command = "SELECT * FROM " + self.employeeTableName + " WHERE ID = %s"
        self.mycursor.execute(command,(id,))
        return self.mycursor.fetchone()

    def getAllEmployeeInfo(self):
        command = "SELECT * FROM " + self.employeeTableName
        self.mycursor.execute(command)
        return self.mycursor.fetchall()

    def getAllDesignationInfo(self):
        command = "SELECT * FROM " + self.designationTableName
        self.mycursor.execute(command)
        return self.mycursor.fetchall()


    def getDesignations(self):
        self.mycursor.execute("SELECT designation FROM %s"%self.designationTableName)
        list = [str(x[0]) for x in self.mycursor.fetchall()]
        return list

    def addDesignation(self, designation, da, ha, ta, it, pt):
        try:
            insert = "INSERT INTO " + self.designationTableName + "  VALUES(%s, %s, %s, %s, %s, %s)"
            self.mycursor.execute(insert,(designation, da, ha, ta, it, pt))
            self.mydb.commit()

        # Note: properly handle exception here
        except Exception as e:
            raise e

    def getDesignationInfo(self, designation):
        command = "SELECT * FROM " + self.designationTableName + " WHERE designation = %s"
        self.mycursor.execute(command,(designation,))
        return self.mycursor.fetchone()


if __name__ == "__main__":
    db = DatabaseManager(host="sql12.freemysqlhosting.net",
                         username="sql12269310",
                         password="sc4Jm8WSRj",
                         databaseName="sql12269310")
    db.getAllEmployeeInfo()