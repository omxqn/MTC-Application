import datetime

import time
from threading import Thread



def get_finish_date(timer):
    times = datetime.datetime.now().time().strftime(f'%H:%M:%S')
    logger.debug("Before: ", times)
    hour, minut, sec = str(times).split(':')[0], str(times).split(':')[1], str(times).split(':')[2]
    hour = int(hour)
    minut = int(minut)
    sec = int(sec)
    total = hour + minut / 60 + sec / 3600
    try:

        time = int(timer.split(":")[0]) + int(timer.split(":")[1]) / 60
        total += time
        hour = int(total)
        minuts = round(float((total - int(total)) * 60))
        if hour >= 24:
            hour = hour - 24
        times = f"{hour}:{minuts}:{sec}"
        logger.debug("After adding: ", times)
        return times


    except Exception:
        logger.debug("time adding format isn't correct")
        return "Error"

class ThreadWithReturnValue(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


    timeers = "0:01"



    def counting_time(self,student_id,timing):
        while True:
            time.sleep(1)
            times = datetime.datetime.now().time().strftime(f'%H:%M:%S')  # get current time
            s_time = times.split(":")
            for index, i in enumerate(s_time):
                if i.startswith("0") and len(i) > 1:
                    s_time[index] = i.replace("0", "")
            times = s_time[0] + ":" + s_time[1] + ":" + s_time[2]

            logger.debug("before: ",timing,"After: ",times)
            logger.debug(int(timing.split(":")[0]) <= int(times.split(":")[0]) and int(timing.split(":")[1]) <= int(times.split(":")[1]) and int(timing.split(":")[2]))
            if int(timing.split(":")[0]) <= int(times.split(":")[0]) and int(timing.split(":")[1]) <= int(times.split(":")[1]) and int(timing.split(":")[2]) <= int(times.split(":")[2]):
                #logger.debug(f"{student_id}: Times UP!!!!")

                return student_id,"Times UP"
            else:
                return student_id,"still"





#timeers = get_finish_date("0:01")


timeers = {"2103100":"10:23:6"}
for index,i in enumerate(timeers):

    thread2 = ThreadWithReturnValue(target=Timer.counting_time,args=[Timer.counting_time,i,timeers[i]])
    thread2.start()
    logger.debug(thread2.join(), "asas")


