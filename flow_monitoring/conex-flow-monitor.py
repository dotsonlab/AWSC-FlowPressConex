#!/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO
import time, sys
import os.path

GPIO.setup("P9_12", GPIO.IN)
GPIO.setup("P9_15", GPIO.IN)
GPIO.setup("P9_23", GPIO.IN)  #greywater product
GPIO.setup("P9_27", GPIO.IN)  #washwater product

now=time.localtime(time.time())
currentmonth=now.tm_mon
currentday=now.tm_mday
currentyear=now.tm_year
filename = "{0}_{1}_{2}_conex-flow.csv".format(currentyear, currentmonth, currentday)

restart = True

#initialize averaging counter
AVE_count1=0
AVE_flow1=0

AVE_count2=0
AVE_flow2=0

AVE_count3=0
AVE_flow3=0

AVE_count4=0
AVE_flow4=0

flow3total = 0
lastflow3total = 0

count=0

global count1
global count2
global count3
global count4

count1 = 0
count2 = 0
count3 = 0
count4 = 0

def countPulse1(channel):
   global count1
   count1 = count1+1

def countPulse2(channel):
   global count2
   count2 = count2+1

def countPulse3(channel):
  global count3
  count3 = count3+1

def countPulse4(channel):
  global count4
  count4 = count4+1

GPIO.add_event_detect("P9_12", GPIO.RISING, callback=countPulse1)
GPIO.add_event_detect("P9_15", GPIO.RISING, callback=countPulse2)
GPIO.add_event_detect("P9_23", GPIO.RISING, callback=countPulse3)
GPIO.add_event_detect("P9_27", GPIO.RISING, callback=countPulse4)

while True:
    try:
        #get current time
        now=time.localtime(time.time())
        pt=time.asctime(now)  #formatted time for file
        currentmonth=now.tm_mon
        currentday=now.tm_mday
        currentyear=now.tm_year

        if (os.path.isfile(filename) and restart):
            #restart ensures that it will only execute this once.
            restart = False
            #restarting the file
            file = open(filename)
            #grab last non-blank line
            last = None
            for line in (line for line in file if line.rstrip('\n')):
                last = line
            #set totalflow to last known value
            totalflow = float(last.split(",")[4])
        elif not (os.path.isfile(filename)):
            #Initial and daily startup
            flow3total = 0
            lastflow3total = 0
            file=open(filename,"a")
            #informative messaging for starting storage file
            print "Opening ",filename, " for appending..."
            print "reading analog inputs and storing data..."
            file.write("Time,GW-Reject,INT-Reject,INT-Product,WW-Product\n")
            #add first column date/time stamp
            file.write(pt)
            file.write(",%f,%f,%f,%f\n" % (AVE_flow1,AVE_flow2,AVE_flow3,AVE_flow4))
            file.close()

        start_counter = 1
        count1=0
        count2=0
        count3=0
        count4=0
        time.sleep(1)
        start_counter = 0
        flow1 = ((count1*12.0)*5.0/588.52) #assumes test flow was 11.5 gpm as defined by manufacturer and reports in gpm
        flow2 = ((count2*12.0)*5.0/588.52)   #changed factor for 5s frequency to 1 sec
        flow3 = ((count3*12.0)*5.0/2200.0/3.78)
        flow4 = ((count4*12.0)*5.0/2200.0/3.78)
        if (count ==5)or(count ==10)or(count==15):
            print pt,'\t%s\t%.2f\t%s\t%.2f\t%s\t%.2f\t%s\t%.2f' % ( "GW-R: ",flow1,"GW-P: ",flow3,"I-R: ",flow2,"I-P: ",flow4)
        count1=0
        count2=0
        count3=0
        count4=0
        flow3total = flow3*(5/60) + lastflow3total
        lastflow3total = flow3total
        count = count+1

        if (now.tm_sec == 0)or(now.tm_sec == 15)or(now.tm_sec == 30)or(now.tm_sec == 45): #if 15sec interval, write data to file
                                         # and write only one value for second $
            AVE_count1=(AVE_count1+count1)/count
            AVE_flow1=(AVE_flow1+flow1)/count
            #print pt,'AVE-\t%s\t%f\t%f' % ( "1",AVE_count1,AVE_flow1)

            AVE_count2=(AVE_count2+count2)/count
            AVE_flow2=(AVE_flow2+flow2)/count
            #print pt,'AVE-\t%s\t%f\t%f' % ( "2",AVE_count2,AVE_flow2)

            AVE_count3=(AVE_count3+count3)/count
            AVE_flow3=(AVE_flow3+flow3)/count
            #print pt,'AVE-\t%s\t%f\t%f' % ( "3",AVE_count3,AVE_flow3)

            AVE_count4=(AVE_count4+count4)/count
            AVE_flow4=(AVE_flow4+flow4)/count
            #print pt,'AVE-\t%s\t%f\t%f' % ( "4",AVE_count4,AVE_flow4)

            if (AVE_flow1>.05)or(AVE_flow2>.05)or(AVE_flow3>.05)or(AVE_flow4>.05): #took out ! for notequal to test
                #open file to append
                file=open(filename,"a")
                #add first column date/time stamp
                file.write(pt)
                #add next columns with raw reading, and converted voltage
                file.write(",%f,%f,%f,%f\n" % (AVE_flow1,AVE_flow2,AVE_flow3,AVE_flow4))
                file.close
                #if MM/DD/YR changes, update filename
                #this translates to a new file every day
                ##!!!!header row is dropped from subsequent days
                filename = "{0}_{1}_{2}_conex-flow.csv".format(currentyear, currentmonth, currentday)

            if (now.tm_sec == 0): ##does displayig the average in the cabin matter? if not can delete this if and 4 prints below
                print pt,'AVE-\t%s\t%f\t%f' % ( "1",AVE_count1,AVE_flow1)
                print pt,'AVE-\t%s\t%f\t%f' % ( "2",AVE_count2,AVE_flow2)
                print pt,'AVE-\t%s\t%f\t%f' % ( "3",AVE_count3,AVE_flow3)
                print pt,'AVE-\t%s\t%f\t%f' % ( "4",AVE_count4,AVE_flow4)
            #reset averageing counters
            AVE_count1=0
            AVE_flow1=0

            AVE_count2=0
            AVE_flow2=0

            AVE_count3=0
            AVE_flow3=0

            AVE_count4=0
            AVE_flow4=0

            count = 0

        else:   # continue summing readings for average
            AVE_count1=AVE_count1+count1
            AVE_flow1=AVE_flow1+flow1

            AVE_count2=AVE_count2+count2
            AVE_flow2=AVE_flow2+flow2

            AVE_count3=AVE_count3+count3
            AVE_flow3=AVE_flow3+flow3

            AVE_count4=AVE_count4+count4
            AVE_flow4=AVE_flow4+flow4

    except KeyboardInterrupt:
        print '\ncaught keyboard interrupt!, bye'
        GPIO.cleanup()
        sys.exit()
