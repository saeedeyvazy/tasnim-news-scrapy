
import schedule 
import time 
import os

  
print('Start Scheduler' )
schedule.every(10).seconds.do(lambda: os.system('scrapy crawl tasnim -s JOBDIR=crawls/tasnim')) 
print('Next job is set to run at: ' + str(schedule.next_run()))
  
# infinite loop to run the scheduled spider 
while True: 
    schedule.run_pending() 
    time.sleep(1) 