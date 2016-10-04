import Adafruit_BBIO.ADC as ADC
import time, sys
import os.path

####setup ADC and assign input pin
ADC.setup()
#analog input pins are
# "AIN0", "P9_39"
# "AIN1", "P9_40"
# "AIN2", "P9_37"
# "AIN3", "P9_38"
# "AIN4", "P9_33"
# "AIN5", "P9_36"
# "AIN6", "P9_35"

psensor_pin1 = 'P9_40'
psensor_pin2 = 'P9_37'
psensor_pin3 = 'P9_38'
psensor_pin4 = 'P9_33'
psensor_pin5 = 'P9_36'

now=time.localtime(time.time())
currentmonth=now.tm_mon
currentday=now.tm_mday
currentyear=now.tm_year
filename = "{0}_{1}_{2}_conex-pressure.csv".format(currentyear, currentmonth, currentday)

restart = True

#initialize averaging counter
AVE_reading1=0
AVE_volts1=0
AVE_pressure1=0

AVE_reading2=0
AVE_volts2=0
AVE_pressure2=0

AVE_reading3=0
AVE_volts3=0
AVE_pressure3=0

AVE_reading4=0
AVE_volts4=0
AVE_pressure4=0

AVE_reading5=0
AVE_volts5=0
AVE_pressure5=0

count=0
printcount=0

#### Begin measurement loop
while True:
    try:
        #read analog pin #
        reading1 = ADC.read(psensor_pin1)
        time.sleep(0.1)
        reading2 = ADC.read(psensor_pin2)
        time.sleep(0.1)
        reading3 = ADC.read(psensor_pin3)
        time.sleep(0.1)
        reading4 = ADC.read(psensor_pin4)
        time.sleep(0.1)
        reading5 = ADC.read(psensor_pin5)
        time.sleep(0.1)

        # increment counter for average calculation
        count = count+1

	# increment printcounter
	printcount = printcount+1

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

        elif not (os.path.isfile(filename)):
            file=open(filename,"a")
            #informative messaging for starting storage file
            print "Opening ",filename, " for appending..."
            print "reading analog inputs and storing data..."
            file.write("Time,P1,P2,P3,P4,P5\n")
            #add first column date/time stamp
            file.write(pt)
            file.write(",%f,%f,%f,%f,%f\n" % (AVE_pressure1,AVE_pressure2,AVE_pressure3,AVE_pressure4,AVE_pressure5))
            file.close()

        #scale reading back to voltage
        volts1=reading1*1.800
        volts2=reading2*1.800
        volts3=reading3*1.800
        volts4=reading4*1.800
        volts5=reading5*1.800

        #scale 1.8V reading to pressure based on 4-20mA signal read
        #from shunt resistor with a 1.8V max at 20 mA corresponding to
        #200 psi and a 4mA min corresponding to 0 psi
        pressure1 = volts1 * 347.22 - 125.00 + 3.65 #feed
        pressure2 = volts2 * 347.22 - 125.00 + 4.55 #greywater reject
        pressure3 = volts3 * 347.22 - 125.00 + 4.06 #inter reject
        pressure4 = volts4 * 140.45 - 49.16 - 0.37 #wash product
        pressure5 = volts5 * 140.45 - 49.16 + 1.16 #inter product
        
	if (printcount>5):
            print pt,'\t%s\t%.2f\t%s\t%.2f\t%s\t%.2f\t%s\t%.2f\t%s\t%.2f' % ( "F: ",pressure1,"GW-R: ",pressure2,"I-P: ",pressure5,"I-R: ",pressure3,"W-P",pressure4)
            printcount=0
        
	#write to the screen #
        ###comment this out when not testing####
        #print pt,'\t%s\t%f\t%f\t%f\t%i' % ( "1",reading1,volts1,pressure1,count)
        #print pt,'\t%s\t%f\t%f\t%f\t%i' % ( "2",reading2,volts2,pressure2,count)
        #print pt,'\t%s\t%f\t%f\t%f\t%i' % ( "3",reading3,volts3,pressure3,count)
        #print pt,'\t%s\t%f\t%f\t%f\t%i' % ( "4",reading4,volts4,pressure4,count)
        #print pt,'\t%s\t%f\t%f\t%f\t%i' % ( "5",reading5,volts5,pressure5,count)

        if (now.tm_sec == 0)&(count>10): #if new minute, write data to file
                                         # avd write only one value for second $
                AVE_reading1=(AVE_reading1+reading1)/count
                AVE_volts1=(AVE_volts1+volts1)/count
                AVE_pressure1=(AVE_pressure1+pressure1)/count
                print pt,'AVE-\t%s\t%f\t%f\t%f' % ( "1",AVE_reading1,AVE_volts1,AVE_pressure1)

                AVE_reading2=(AVE_reading2+reading2)/count
                AVE_volts2=(AVE_volts2+volts2)/count
                AVE_pressure2=(AVE_pressure2+pressure2)/count
                print pt,'AVE-\t%s\t%f\t%f\t%f' % ( "2",AVE_reading2,AVE_volts2,AVE_pressure2)

                AVE_reading3=(AVE_reading3+reading3)/count
                AVE_volts3=(AVE_volts3+volts3)/count
                AVE_pressure3=(AVE_pressure3+pressure3)/count
                print pt,'AVE-\t%s\t%f\t%f\t%f' % ( "3",AVE_reading3,AVE_volts3,AVE_pressure3)

                AVE_reading4=(AVE_reading4+reading4)/count
                AVE_volts4=(AVE_volts4+volts4)/count
                AVE_pressure4=(AVE_pressure4+pressure4)/count
                print pt,'AVE-\t%s\t%f\t%f\t%f' % ( "4",AVE_reading4,AVE_volts4,AVE_pressure4)

                AVE_reading5=(AVE_reading5+reading5)/count
                AVE_volts5=(AVE_volts5+volts5)/count
                AVE_pressure5=(AVE_pressure5+pressure5)/count
                print pt,'AVE-\t%s\t%f\t%f\t%f' % ( "5",AVE_reading5,AVE_volts5,AVE_pressure5)


                #open file to append
                file=open(filename,"a")
                #add first column date/time stamp
                file.write(pt)
                #add next columns with raw reading, and converted voltage
                file.write(",%f,%f,%f,%f,%f\n" % (AVE_pressure1,AVE_pressure2,AVE_pressure3,AVE_pressure4,AVE_pressure5))
                #add first column date/time stamp
                file.close()
                #if MM/DD/YR changes, update filename
                #this translates to a new file every day
                filename = "{0}_{1}_{2}_conex-pressure.csv".format(currentyear, currentmonth, currentday)

                #reset averageing counters
                AVE_reading1=0
                AVE_volts1=0
                AVE_pressure1=0

                AVE_reading2=0
                AVE_volts2=0
                AVE_pressure2=0

                AVE_reading3=0
                AVE_volts3=0
                AVE_pressure3=0

                AVE_reading4=0
                AVE_volts4=0
                AVE_pressure4=0

                AVE_reading5=0
                AVE_volts5=0
                AVE_pressure5=0

                count=0
        else:   # continue summing readings for average
                AVE_reading1=AVE_reading1+reading1
                AVE_volts1=AVE_volts1+volts1
                AVE_pressure1=AVE_pressure1+pressure1

                AVE_reading2=AVE_reading2+reading2
                AVE_volts2=AVE_volts2+volts2
                AVE_pressure2=AVE_pressure2+pressure2

                AVE_reading3=AVE_reading3+reading3
                AVE_volts3=AVE_volts3+volts3
                AVE_pressure3=AVE_pressure3+pressure3

                AVE_reading4=AVE_reading4+reading4
                AVE_volts4=AVE_volts4+volts4
                AVE_pressure4=AVE_pressure4+pressure4

                AVE_reading5=AVE_reading5+reading5
                AVE_volts5=AVE_volts5+volts5
                AVE_pressure5=AVE_pressure5+pressure5

        #sleep for (.1 s)
        time.sleep(.1)

    except KeyboardInterrupt:
        print '\ncaught keyboard interrupt!, bye'
        sys.exit()
        ####currently, program only stops with a CTRL-C
