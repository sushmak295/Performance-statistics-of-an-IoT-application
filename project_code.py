# Project: Performance Analysis of Operating Systems # General Purpose OS Raspbian
# Sagar, Neetha, Sushma

import RPi.GPIO as GPIO	# import raspberry pi import time	# Timing library
import paho.mqtt.client as mqtt # mqtt client library for IoT MQTT protocol
import os	# to get process id
import psutil	# Python process and system utilization library
import timeit

# Overhead due to all psutil commands used
# time.time() returns the time in seconds since the epoch, i.e., the point where the time starts

class all_latencies:	# This class contains all methods called by timeit.timeit()
    def t_latency(self):
        time.time()

    def ct_latency(self):	# self is argument passed to all methods in python
        psutil.cpu_times()

    def cpu_per(self):
        psutil.cpu_percent()

    def vir_mem(self):
        psutil.virtual_memory()

    def swp_mem(self):
        psutil.swap_memory()

    def b_time(self):
        psutil.boot_time()

sag=all_latencies()	# instantiate object for class

# With help of object, every method is called in timeit.timeit()
# Number=1 shows that time is being calculated for single time execution

print "overhead due to time.time():",timeit.timeit(sag.t_latency,number=1)
print "overhead due to psutil.cpu_times():",timeit.timeit(sag.ct_latency,number=1) print "overhead due to psutil.cpu_percent():",timeit.timeit(sag.cpu_per,number=1)
print "overhead due to psutil.virtual_memory():",timeit.timeit(sag.vir_mem,number=1) print "overhead due to psutil.swap_memory():",timeit.timeit(sag.swp_mem,number=1) print "overhead due to psutil.boot_times():",timeit.timeit(sag.b_time,number=1)

start = time.time()	#start timer for calculation of A to B time
 
GPIO.setmode(GPIO.BCM)	# set up BCM GPIO numbering
GPIO.setwarnings(False)	# doesn't show warnings GPIO.setup(2, GPIO.IN,pull_up_down=GPIO.PUD_UP)	# set GPIO25 as input (button)
GPIO.setup(21, GPIO.OUT)	# set direction
GPIO.output(21,GPIO.HIGH)	# set pin 21 to high
GPIO.setup(22,GPIO.IN)	# set pin 22 as input pin
print GPIO.input(2) # cpu parameters
print "SYSTEM cpu time: ",psutil.cpu_times()	# to calculate time in user and kernel mode
print "SYSTEM cpu_percent: ",psutil.cpu_percent() # system wise cpu- percentage use

# memory parameters

print "SYSTEM memory used: ",psutil.virtual_memory()	# physical and virtual memory
print "SYSTEM swapped memory: " ,psutil.swap_memory() # swapped memory

# timing parameters
print	"Boot time for Raspbian: " ,psutil.boot_time() # Boot time for operating system

# A function to start timer when interrupt occurs def my_timer(void):
global s_1	# Set to global since we are using it in my_interrupt()
s_1=time.time()	#ISR starts so time is recorded

#Function to define interrupt
#This function will run to print 3-bit counter

def my_interrupt(void):
    def makeCounter_rec(base):
        def incDigit(num, pos):	#recursive implementation new=num[:]
            if (num[pos]== base-1): new[pos]=0
            if (pos < len(num)-1):
                return incDigit(new, pos+1)
            else:
                new[pos]=new[pos]+1
                return new

        def inc(num):
            return incDigit(num,0) return inc

    base=2 inc=makeCounter_rec(base)
    n=[0,0,0]	# Initialise counter to [0,0,0] print n
    for i in range(base**len(n)):
        n=inc(n)
        print n
 
    e=time.time()	# ISR ends here so record time print "ISR latency: ",e-s_1	# ISR latency is diff between
    time of interrupt occurance and end of ISR

    pid_1=os.getpid() print pid_1
    p_1=psutil.Process(pid_1) print p_1.name
    print p_1.create_time
    print "ISR CPU time:",p_1.cpu_times()	# CPU time of process(User and Kernel)
    print "Context switches:" ,p_1.num_ctx_switches()	# Total context switches in system
    print "ISR cpu_percent:",p_1.cpu_percent()	# Percent of CPU used by process( it is negligible)
    print "number of threads used in ISR:",p_1.num_threads() # Number of threads running

    # memory parameters
    print	"ISR process memory info:" ,p_1.memory_info()
    print	"ISR process memory percent:" ,p_1.memory_percent()
    print	"ISR process memory maps:" ,p_1.memory_maps()
    print	"ISR process children: " ,p_1.children(recursive=True)

class all_latencies_ISR: global pid_1 pid_1=os.getpid() p_1=psutil.Process(pid_1)
    print "Process ID is:", pid_1

    def isrct_switches(self): p_1.num_ctx_switches()

    def isrcp_time(self): p_1.cpu_times()

    def isrcp_percent(self): p_1.cpu_percent()

    def isr_thread(self): p_1.num_threads()

    def isr_mem(self): p_1.memory_info()

    def isr_memper(self): p_1.memory_percent()

    def isr_memmap(self): p_1.memory_maps()

    def isr_child(self): p_1.children(recursive=True)

sag_1= all_latencies_ISR()
# To calculate overhead due to process psutil commands # Every method in class all_latencies_ISR is called
 
print "overhead due to p_1.num_ctx_switches():",timeit.timeit(sag_1.isrct_switches,number=1)
print "overhead due to p_1.cpu_times():",timeit.timeit(sag_1.isrcp_time,number=1)
print "overhead due to p_1.cpu_percent():",timeit.timeit(sag_1.isrcp_percent,number=1)
print "overhead due to p_1.num_threads():",timeit.timeit(sag_1.isr_thread,number=1)
print "overhead due to p_1.memory_info():",timeit.timeit(sag_1.isr_mem,number=1)
print "overhead due to p_1.memory_percent():",timeit.timeit(sag_1.isr_memper,number=1)
print "overhead due to p_1.memory_maps():", timeit.timeit(sag_1.isr_memmap,number=1)
print "overhead due to p_1.children:",timeit.timeit(sag_1.isr_child,number=1)
print " 	ISR INFORMATION ENDS HERE 	"


GPIO.add_event_detect(22, GPIO.FALLING,callback=my_timer)	# Callback to start timer on occurance of interrupt
GPIO.add_event_detect(2, GPIO.FALLING,callback=my_interrupt)	# Callback function to check interrupt

def on_connect(client,userdata,rc):
    client.subscribe("sagar/demo/led") # Subsscribing "sagar/demo/led" topic

def on_message(client,userdata,msg):
    if "green" in msg.payload:	# check for contents of payload print"green is ON"
        GPIO.output(11, True) 
    else:
        print"green is OFF" GPIO.output(11, False)
     

    if "yellow" in msg.payload:
        print"yellow is ON"
        GPIO.output(12,True)
        
    else: 
        print"yellow is OFF"
        GPIO.output(12, False)	# Control application connected to pin 
     

    if "red" in msg.payload:
        print"red is ON" GPIO.output(13, True)
    else:
        print"red is OFF" GPIO.output(13, False)
 
    pid=os.getpid()	#Getting process ID print "Process ID is:" pid
    p=psutil.Process(pid)	# Creating object for process
     
    print p.name	# Process neme,evrytime object is used to call function
    print p.create_time	# Time when process was created
    print "CPU times:",p.cpu_times()	# User and kernel mode execution time for process
    print "Context switches:" ,p.num_ctx_switches() # Number of context switches from start
    print "cpu_percent:",p.cpu_percent()	# Percent of CPU used by a process
    print "number of threads used:",p.num_threads() # Number of process threads
    # memory parameters

    print	"process memory info:" ,p.memory_info()	# Memory Used by process
    print	"process memory percent:" ,p.memory_percent()	# Percent memory used by process
    print	"process memory maps:" ,p.memory_maps()	#Return process's mapped memory region
    print	"process children: " ,p.children(recursive=True) # Knowing childrens for process
    print " 	MAIN PROCESS INFO ENDS HERE 	"

client =mqtt.Client()	#returns object for MQTT client

client.on_connect=on_connect	#Calling function client.on_message=on_message client.connect("iot.eclipse.org",1883,60) #connect with MQTT broker

GPIO.setmode(GPIO.BCM)	# Using Broadcom SOC pin configuration
GPIO.setup(11,GPIO.OUT)	# Declaring pin directions GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

end = time.time()
print 'A-B time: '	# Point A to B timing calculation
print(end-start)
print " 	SYSTEM INFO ENDS HERE 	"

client.loop_forever()	# Always check for message on MQTT broker
