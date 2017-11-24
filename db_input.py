import sqlite3
from datetime import datetime
import sys

try:
    conn = sqlite3.connect(sys.argv[1])
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tests")
except Exception:
    print("Wrong database")
    input("Type any key for exit")
    sys.exit(0)

cursor.execute("PRAGMA foreign_keys = ON")
cursor.execute("SELECT id, test FROM tests")
avaliableTests = cursor.fetchall()

print("Avaliable tests:")
for record in avaliableTests:
    print("{} - {}".format(record[0], record[1]))

testsRecord = {}
resultsRecord = {}

testsRecord["test"] = input("Type number of test you need or new test name: ")

if testsRecord["test"].isdecimal():
    resultsRecord["test"] = int(testsRecord["test"])
    testFound_flag = False
    for record in avaliableTests:
        if record[0] == resultsRecord["test"]:
            print("You choose test {} - {}".format(record[0], record[1]))
            testFound_flag = True
            break # I hope it always sorted...
    if testFound_flag == False:
        print("Test {} not found".format(testsRecord["test"]))
        conn.close()
        input("Type any key for exit")
        sys.exit(0)
else:
    print("You choose new test and called it \"{}\"".format(testsRecord["test"]))
    testsRecord["descr"] = input("Type description (optional): ")
    testsRecord["units"] = input("Type units: ")
    if testsRecord["test"] and testsRecord["units"]:
        cursor.execute("INSERT INTO tests (test, descr, units) VALUES (:test, :descr, :units)", testsRecord)
        conn.commit()
        resultsRecord["test"] = cursor.lastrowid
    else:
        print("Your data is wrong")
        conn.close()
        input("Type any key for exit")
        sys.exit(0)

resultsRecord["date_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
resultsRecord["condition"] = input("Type test condition (optional): ")
resultsRecord["value"] = input("Type test result value: ")
print(resultsRecord)
if resultsRecord["value"]:
    cursor.execute("INSERT INTO results (test, date_time, condition, value) VALUES (:test, :date_time, :condition, :value)", resultsRecord)
    conn.commit()
else:
    print("You didn't type value!")

conn.close()
input("Type any key for exit")
