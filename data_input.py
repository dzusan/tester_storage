import csv

with open("log.csv", "r", newline="") as csvfile:
    logreader = csv.DictReader(csvfile)

    print("Avaliable tests:")
    count = 1
    for key in logreader.fieldnames:
        if key != "timeStamp" and key != "condition":
            print("{} - {}".format(count, key))
            count += 1

    print("Type number of test you need or new test name:")
    request = input()

    try:
        test = logreader.fieldnames[int(request) + 1]
    except ValueError:
        print("You choose new test and called it \"{}\"".format(request))
        test = request
    except IndexError:
        print("Test {} not found".format(request))
    else:
        print("You choose test \"{}\"".format(test))



    # logwriter = csv.writer(csvfile, delimiter=',')



    


    


    '''
    xdata = []
    ydata = {key: [] for key in reader.fieldnames if key != "timeStamp"}

    for row in reader:
        for key in row.keys():
            if key == "timeStamp":
                timeStampString = row[key]
                timeStampObject = datetime.strptime(timeStampString, "%Y-%m-%dT%H:%M:%S.%f")
                xdata.append(timeStampObject)
            else:
                ydata[key].append(float(row[key]))

print("Hello")

i = input()
print("YOUR: " + i)
'''
