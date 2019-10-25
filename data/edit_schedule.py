import csv

with open('schedule.csv') as schedule_csv:
    read_data = csv.reader(schedule_csv)
    print("Current Schedule:\n")
    #i=0

    rows = []
    for row in read_data:
        
        if row != ["HOUR", "MINUTE", "MUSIC"]:
            rows.append([int(row[0]),int(row[1]), row[2]])
            #i+=1
            #print("%d %02s:%02s  -> %s"%(i,row[0], row[1], row[2]))

rows = sorted(rows, key = lambda x : int(x[0])*60+int(x[1]))        

i=0
for row in rows:
    
    if row != ["HOUR", "MINUTE", "MUSIC"]:
        print("%d %02s:%02s  -> %s"%(i,row[0], row[1], row[2]))

    i+=1

def save_file(data):
    with open('schedule.csv','w') as schedule_csv:
        writer = csv.writer(schedule_csv)
        writer.writerows(data)

while True:
    ans = raw_input('Edit? (y/n)')
    if ans == 'y':
        hour = input("input hour: ")
        minute = input("input minute: ")
        music = raw_input("input music: ")

        if hour > 24 or minute >= 60:
            print("WTF THIS IS NOT TIME")
            continue
        # insert data
        rows.append([hour,minute,music])
        rows = sorted(rows, key = lambda x : int(x[0])*60+int(x[1])) 

        # print schedule
        i=0
        for row in rows:
            
            if row != ["HOUR", "MINUTE", "MUSIC"]:
                print("%d %02s:%02s  -> %s"%(i,row[0], row[1], row[2]))

            i+=1

    elif ans == 'n':
        ans = raw_input("Save file? (y/n)")
        if ans == 'y':
            save_file([["HOUR", "MINUTE", "MUSIC"]]+rows)
        elif ans == 'n':
            break
        else:
            print("Invalid input. Please try again.\n")
    else:
        print("Invalid input. Please try again.\n")

