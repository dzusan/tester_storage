import sqlite3
from datetime import datetime
import sys
import colorama
import win32com.client as win

def fillinput(prompt, default=""):
    win.Dispatch("WScript.Shell").SendKeys(default)
    return input(prompt)

def errprint(*args, **kwargs):
    print("\x1b[1;31;40mERROR: ", end="")
    print(*args, end="", **kwargs)
    print("\x1b[0m")


def dialog(conn, cursor):
    cursor.execute("SELECT id, test FROM tests")
    avaliableTests = cursor.fetchall()

    print("Avaliable tests:")
    for record in avaliableTests:
        print("{} - {}".format(record[0], record[1]))

    testsRecord = {}
    resultsRecord = {}

    testsRecord["Test"] = input("Type number of test you need or new test name: ")

    if testsRecord["Test"].isdecimal():
        resultsRecord["Test"] = int(testsRecord["Test"])
        testFound_flag = False
        for record in avaliableTests:
            if record[0] == resultsRecord["Test"]:
                print("You choose test {} - {}".format(record[0], record[1]))
                testsRecord["Test"] = record[1] # For following mnemonic print
                testFound_flag = True
                break # I hope it always sorted...
        if testFound_flag == False:
            errprint("Test {} not found".format(testsRecord["Test"]))
            return
    else:
        print("You choose new test and called it \"{}\"".format(testsRecord["Test"]))
        testsRecord["Description"] = input("Type description (optional): ")
        testsRecord["Units"] = input("Type units: ")
        if testsRecord["Test"] and testsRecord["Units"]:
            cursor.execute("INSERT INTO tests (test, descr, units) VALUES (:Test, :Description, :Units)", testsRecord)
            conn.commit()
            resultsRecord["Test"] = cursor.lastrowid
        else:
            errprint("Your data is wrong", file=sys.stderr)
            return

    resultsRecord["Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prefill condition field with value in last record
    cursor.execute("SELECT condition FROM results ORDER BY id DESC LIMIT 1")
    lastCondition = cursor.fetchall()
    resultsRecord["Condition"] = fillinput("Type test condition (optional): ", default=lastCondition[0][0])
    
    resultsRecord["Value"] = input("Type test result value: ")
    if resultsRecord["Value"]:
        cursor.execute("INSERT INTO results (test, date_time, condition, value) VALUES (:Test, :Time, :Condition, :Value)", resultsRecord)
        conn.commit()
        print("\nYou made record:")
        print("Test: {}".format(testsRecord["Test"]))
        for key in resultsRecord.keys():
             if key != "Test":
                print("{}: {}".format(key, resultsRecord[key]))
    else:
        errprint("You didn't type value!")

#################################
colorama.init()

try:
    conn = sqlite3.connect(sys.argv[1])
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tests")
except Exception:
    errprint("Wrong database")
    input("Type any key for exit")
    sys.exit(0)

cursor.execute("PRAGMA foreign_keys = ON")

try:
    while(True):
        print("")
        dialog(conn, cursor)
except KeyboardInterrupt:
    print("")
    errprint("You break the program")
except EOFError:
    print("")
    errprint("You break the program")
finally: # Unexpected break
    conn.close()
    print("--- break ---") # For debug
