import datetime
def get_finish_date(time):

    times = datetime.datetime.now().time().strftime(f'%H:%M:%S')
    print("Before: ",times)
    hour,minut,sec = str(times).split(':')[0],str(times).split(':')[1],str(times).split(':')[2]
    hour = int(hour)
    minut = int(minut)
    sec = int(sec)
    total = hour+minut/60+sec/3600
    try:

        time = int(time.split(":")[0])+int(time.split(":")[1])/60
        total+=time
        hour = int(total)
        minuts = round(float((total - int(total)) * 60))
        if hour>=24:
            hour = hour-24
        times = f"{hour}:{minuts}:{sec}"
        print("After adding: ",times)
        return times


    except Exception:
        print("time adding format isn't correct")
        return "Error"

#get_finish_date("5:30")
