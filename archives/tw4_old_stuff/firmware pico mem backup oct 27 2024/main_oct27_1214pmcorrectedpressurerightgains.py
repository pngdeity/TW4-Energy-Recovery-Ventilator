import sdp810_125
from combifan import combi_fan_spd
from machine import PWM, Pin, ADC, reset
from simple_pid import PID
from time import sleep, ticks_ms, ticks_diff
from machine import WDT, reset
import json
import os
import sys
import select
import network
import socket
from umqtt.robust import MQTTClient
import uping
print("you have 6 seconds to hit the red button before things get complicated, watchdog will be enabled etc")
sleep(6)
print("time's up")
print(sdp810_125.get_reading())
I_gain = 0.35
P_gain = 0.15
pid_ingress = PID(P_gain,I_gain,0, setpoint = 15)
pid_ingress.output_limits = (-100, 100)
pid_egress = PID(P_gain,I_gain,0, setpoint = 15)# pid2 is egress
pid_egress.output_limits = (-100, 100)
potpinadc = ADC(Pin(28))
oldpot_val =0
read_fail_strikes = 0
mqtt_perc = 40
main_perc = 50
persistent_vars_filename = "persistent_vars.json"
persistent_vars_dict = {"ssid_main_wifi": "use_ap",
                        "password_main_wifi": "none",
                        "ssid_ap": "TW4_ap_leader",
                        "ap_password" : "osrocks8882888",
                        "ip_leader":'192.168.4.1',
                        "ip_follower":'192.168.4.2',#this has to be 192.168.4.x, it doesn't like other ip addresses
                        "leader_or_follower" : "leader",
                        "ADAFRUIT_IO_URL" : "io.adafruit.com",
                        "ADAFRUIT_USERNAME" : b'',
                        "ADAFRUIT_IO_KEY": b'',
                        "ADAFRUIT_IO_FEEDNAME" : b'OpenERV_TW4-1',
                        "ADAFRUIT_IO_FEEDNAME_publish" : b'OpenERV_TW4-1_status',
                        }
def connect_wifi(ssid, password):
    global leader_or_follower
    global ip_follower
    if ssid == "use_ap":
        ip = make_ap()
        print("ssid was use_ap so made an access point instead, make sure this one is a leader")
        return ip, "none"
    wlan = network.WLAN(network.STA_IF)
    wdt.feed()
    if wlan.active()==True:
        wlan.active(False)
    wlan.active(True)
    wdt.feed()
    wlan.connect(ssid, password)
    wdt.feed()
    x=0
    while wlan.isconnected()==False:
        print("Waiting for connection to network with ssid ",ssid," and password:", password, "...",x)
        sleep(1)
        x=x+1
        led.toggle()
        wdt.feed()
        if x>20:
            print("couldn't connect in ", x , " seconds")
            return None, None 
    ip=wlan.ifconfig()
    print("connected to wifi, my address is:",ip[0])
    led.off()
    if leader_or_follower == "follower":
        print("old ifconfig",wlan.ifconfig())
        tuple_ip_mask =(ip_follower,'255.255.255.0')
        new_ifconfig = tuple_ip_mask+wlan.ifconfig()[2:4]
        wlan.ifconfig(new_ifconfig)
        ip=wlan.ifconfig()[0]
        print("updated ip address, which is for the follower (this one is follower): ",ip)
    return ip[0], wlan

def make_ap():
    global ssid_ap
    global ap_password
    ssid = ssid_ap
    password = ap_password
    print("making AP with ssid:",ssid," password:",password)
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password) 
    ap.active(True)
    while ap.active == False:
      pass
    print("Access point apparently started ok, ip (can't change it):", ap.ifconfig()[0])# it appears you cannot change the ip of the device while in ap mode
    return ap.ifconfig()[0]
# def cb(topic, msg):# this only gets executed if there is an mqtt message recieved, it's the callback
#     global mqtt_perc
#     try:
#         perc = int(str(msg)[2:-1]) # this might not be quite right. it should be a bytes object, so if we convert it to a string chop off extras then int taht should work.
#     except BaseException as error:
#         print("there was no message or it was not a valid integer, message was:",str(msg)[2:-1],"error exactly was: ",error)
#     else:
#         print("mqtt perc command recieved:", perc)
#         mqtt_perc = perc
def mqtt_publish(message):
    global mqtt_feedname_publish
    wdt.feed()
    client.publish(mqtt_feedname_publish,    
                   bytes(str(message), 'utf-8'), 
                   qos=0)
    wdt.feed()
    return
def save_vars():
    global persistent_vars_dict
    vars_dict=persistent_vars_dict
    global_dict_copy = globals()
    for key in vars_dict:
        vars_dict[key] = global_dict_copy[key]   
    with open(persistent_vars_filename, "w") as outfile:
         json.dump(vars_dict, outfile)
         
def restore_vars():
    with open(persistent_vars_filename,"r") as openfile:
        vars_dict = json.load(openfile)
    globals().update(vars_dict)
delta_from_internal_clock = 0
def update_clock(recieved_time):
    global delta_from_internal_clock
    delta_from_internal_clock=ticks_diff(ticks_ms(),recieved_time) # a positive value means ticks_ms is larger than recieved time
def ticks_ms2():
    global delta_from_internal_clock
    if leader_or_follower == "follower":
        synched_time = ticks_diff(ticks_ms(), delta_from_internal_clock)
        return synched_time
    if leader_or_follower == "leader":
        return ticks_ms()
def check_pot():
    global oldpot_val
    read = potpinadc.read_u16()
    print("raw pot val:", read)
    if abs(read-oldpot_val)>1600:
        oldpot_val = read
        return read/655.53
    return oldpot_val/655.53
def percent_to_pressure(perc):
    max_pressure  = 30
    pressure = perc*max_pressure/100
    if pressure > 30:# the actual pressure is divided because the sensor actually allows flow through it 
        pressure = 30
    if pressure < -30:
        pressure = -30
    if -4 < pressure < 4:
        pressure = 0
    return pressure
def check_cp_ingress():
    global main_perc
    print("main_perc:",main_perc)
    pressure = percent_to_pressure(main_perc)
    return pressure
def check_cp_egress(): # we might want a pressure bias some day so have separate functions to calculate ingress and egress pressures
    global main_perc
    print("main_perc:",main_perc)
    pressure = -1*percent_to_pressure(main_perc)
    return pressure
def run_pid_ingress():
    global last_egress_throttle
    v = check_actual_pressure()
    control = pid_ingress(v)
    combi_fan_spd(control, last_egress_throttle)
    return control
def run_pid_egress():
    global last_ingress_throttle
    v = check_actual_pressure()
    control = pid_egress(v)
    combi_fan_spd(control, last_ingress_throttle)
    return control
def period_time_calc():
    global main_perc
    if main_perc > 0:
        perc_power = main_perc
    else:
        perc_power = 0.1# to avoid division by zero
    max_time = 120_000
    prop_time = 50_000/(perc_power/100)
    if prop_time >max_time:
        prop_time = max_time
    return prop_time
oldpressure = 0
def check_actual_pressure():
    global oldpressure
    global read_fail_strikes
    correction_ratio = 3.45 #the sensor actually has a very small hole between it's inlet and the other side, which is inconvenient as the pressure drops as if flows down the tube.  The tube has to be the same length for every module, and not be pinched.
    try:
        sleep(0.01)
        pressure = correction_ratio * sdp810_125.get_reading()
    except BaseException as error: # covers all errors
        print("error, probably comm error with pressure sensor:", error)
        read_fail_strikes += 1
        if read_fail_strikes > 5: #if it fails to read more than 5 times in a row
            sleep(10)#reset the whole system by triggering watchdog
        return oldpressure
    oldpressure = pressure
    read_fail_strikes = 0
    return pressure
def try_connect_forever():
    global ip
    ip = None
    while ip == None:#keep trying forever
        wdt.feed()
        ip, wlan = connect_wifi(ssid_main_wifi,password_main_wifi)
    return ip, wlan
mqtt_cfm = 50
last_b = mqtt_cfm
last_a = check_pot()
perc = 50
def combine_percs(a, b):
    global last_b
    global last_a
    global perc
    if abs(last_b - b)>1:
        perc = b
        last_b = b
    if abs(last_a - a)>1:
        perc = a
        last_a = a
    return perc
def cb(topic, msg):# this only gets executed if there is an mqtt message recieved, it's the callback
    global mqtt_perc
    try:
        perc = int(str(msg)[2:-1]) #should be a bytes object, so if we convert it to a string chop off extras then int that should work.
    except BaseException as error:
        print("there was no message or it was not a valid integer, message was:",str(msg)[2:-1],"error was: ",)
    else:
        mqtt_perc = perc
        print("mqtt perc command recieved mqtt_perc variable updated:", mqtt_perc)
mqtt_feedname_publish = 0 
def connect_mqtt():
    global ADAFRUIT_USERNAME
    global ADAFRUIT_IO_FEEDNAME
    global ADAFRUIT_IO_FEEDNAME_publish
    global ADAFRUIT_IO_URL
    global ADAFRUIT_IO_KEY
    global mqtt_feedname_publish
    mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')
    mqtt_feedname_publish = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME_publish), 'utf-8')
    random_num = int.from_bytes(os.urandom(3), 'little')
    mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')
    client = MQTTClient(client_id=mqtt_client_id, 
                        server=ADAFRUIT_IO_URL, 
                        user=ADAFRUIT_USERNAME, 
                        password=ADAFRUIT_IO_KEY,
                        ssl=False)
    client.set_callback(cb)
    try:
        print("about to start mqtt connection")
        wdt.feed()
        client.connect()
        wdt.feed()
        mqtt_connected = 1
        print("mqtt connected ok! Recieve feed name:", ADAFRUIT_IO_FEEDNAME, "Status updates feedname:",ADAFRUIT_IO_FEEDNAME_publish)
    except Exception as e:
        mqtt_connected = 0
        print('could not connect to MQTT server, oserror -1 means the adafruit server is not working right or key or username not right -2 usually means no internet connection: {}{}'.format(type(e).__name__, e))
        print("username: ",ADAFRUIT_USERNAME, " key: ",ADAFRUIT_IO_KEY)
    if mqtt_connected == 1:
        wdt.feed()
        client.subscribe(mqtt_feedname)
        wdt.feed()
    return mqtt_connected, client
def comm_mqtt(mqtt_connected):
    if mqtt_connected == 1:
        try:
            print("got this far6")
            sleep(0.1)
            mqtt_publish(ticks_ms())
            print("clock time published")
            sleep(0.1)
            client.check_msg() #if changed from follower to leader this will cause an error, just let it go and let the watchdog reboot.
            print("mqtt messages checked ok")
        except BaseException as error:
            print("apparently connected to mqtt but got an error during effort to communicate over mqtt", error)
    return
def send_synch_udp():
    global main_perc
    global ip_follower
    receiver_port = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    x = 0
    try:
        while x < 3 :
            # Send "Hello, world!" message
            reply = str(ticks_ms())+","+ str(main_perc)
            sock.sendto(reply.encode(), (ip_follower, receiver_port))
            print(f"Sent: {reply}")
            wdt.feed()
            sleep(1)
            x = x + 1
    except BaseException as error:
        print("error while sending udp synch packet:", error)
    finally:
        sock.close()
def listen_udp_follower():
    listen_port = 12345

    data = None
    timer = ticks_ms()
    big_timeout = 100
    wdt.feed()
    while data == None and ticks_diff(ticks_ms(),timer) < (big_timeout*1000):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('', listen_port))
            print(f"Listening for UDP messages on port {listen_port}")
            sock.settimeout(3)#timeout in seconds
            wdt.feed()
            data, addr = sock.recvfrom(1024)
            wdt.feed()
            print(f"Received '{data.decode()}' from {addr}")
            return data.decode()
        except BaseException as error:
            wdt.feed()
            print("error while listening for udp synch packet:", error)
            sleep(1)
            wdt.feed()
        finally:
            sock.close()
    return None
def follower_wait_synch():
    global main_perc
    status = "not synched"
    message = None
    message = listen_udp_follower()
    wdt.feed()
    print("listened for a while, no synch packet recieved")
    print("message (synch packet presumably) recieved:", message)
    if message == None:
        reset()
        return status
    if len(message) > 4: # basic check we got a valid message
        recieved_items = message.split(",") #split the message so we can get different fields of different length reliably
        clock_leader = int(recieved_items[0])
        main_perc = float(recieved_items[1])
        update_clock(clock_leader)
        print("local clock on follower updated:",ticks_ms2())
        print("main power level from leader recieved and updated on follower:",main_perc) 
        status = "synched"
    return status
def check_wifi_reconnect(ip, wlan):
    try:    
        if wlan.isconnected() == False and leader_or_follower == "leader":
            wdt.feed()
            ip, wlan = try_connect_forever() 
            return ip, wlan
    except BaseException as error:
            print("error trying to reconnect wifi, probbly it means we are in ap mode if wlan doesn't exist error is:", error)
            return ip_leader, "none"
    return ip, wlan  
last_ingress_throttle = 0
last_egress_throttle = 0
wdt = WDT(timeout = 6500)
led=machine.Pin('LED', machine.Pin.OUT)
globals().update(persistent_vars_dict)
root_files = os.listdir('/')
if 'persistent_vars.json' not in root_files: # if the file doesn't exist then create it with the defaults.
    save_vars()
restore_vars()
ip = None
wdt.feed()
ip, wlan = try_connect_forever()
mqtt_connected = 0
wdt.feed()
#sys.exit()# this is useful for testing.  it causes things to return to the repl so you can run functions etc. as desired, ctrl+c will also do that unless you are in a try except block.
try:    
    if wlan.isconnected() == True and leader_or_follower == "leader":
        try:
            wdt.feed()
            uping.ping(ip_follower)
            wdt.feed()
            uping.ping('192.168.4.1')# if it's connected to the access point this should be the ip of the leader *it also is necessary to add this ip to the router table so things work
            wdt.feed()
            uping.ping(ADAFRUIT_IO_URL)#just to verify we can connect, makes troubleshooting easier.
            wdt.feed()
            mqtt_connected, client = connect_mqtt()
            wdt.feed()
        except BaseException as error:
            print("error trying to ping stuff to test wifi and then connect mqtt etc.  -2 seems to be no internet connection: ",error)
    if wlan.isconnected() == True and leader_or_follower == "follower":
        wdt.feed()
        uping.ping('192.168.4.1')# if it's connected to the access point this should be the ip of the leader *it also is necessary to add this ip to the router table so things work
        wdt.feed()
except BaseException as error:
        print("error trying to ping stuff:", error)
while True:
    wdt.feed()
    combi_fan_spd(last_ingress_throttle,last_egress_throttle)
    if leader_or_follower == "leader":
        cp_ingress = check_cp_ingress()
        if mqtt_connected == 1:
            wdt.feed()
            comm_mqtt(mqtt_connected)
            wdt.feed()
        main_perc = combine_percs(check_pot(), mqtt_perc)
        ip, wlan = check_wifi_reconnect(ip, wlan)
        send_synch_udp()
    if leader_or_follower == "follower":
        status = "not synched"
        while status != "synched":
            ip, wlan = check_wifi_reconnect(ip, wlan)
            wdt.feed()
            status = follower_wait_synch()
            wdt.feed()
            print("synch status from most recent try: ", status)
        cp_ingress = check_cp_ingress()*(-1)
    period_time = period_time_calc()
    pid_ingress.setpoint = cp_ingress
    pid_ingress.set_auto_mode(True, last_output=last_ingress_throttle)
    while (ticks_ms2()%period_time) < period_time/2: #if ingress section run ingress pid     
        for i in range(100):
            last_ingress_throttle = run_pid_ingress()
            wdt.feed()
        if leader_or_follower == "leader":
            main_perc = combine_percs(check_pot(), mqtt_perc)
            cp_ingress = check_cp_ingress()
        pid_ingress.setpoint = cp_ingress
        p, i, d = pid_ingress.components
        print(" sp:", pid_ingress.setpoint, " p:",check_actual_pressure()," throttle:", last_ingress_throttle) #," timemodulo:", ticks_ms()%period_time)
    pid_ingress.set_auto_mode(False)
    combi_fan_spd(last_egress_throttle, last_ingress_throttle)
    if leader_or_follower == "leader":
        cp_egress = check_cp_egress()
        main_perc = check_pot()
    if leader_or_follower == "follower":
        cp_egress = check_cp_egress()*(-1)
    pid_egress.setpoint = cp_egress
    pid_egress.set_auto_mode(True, last_output=last_egress_throttle)
    while period_time/2 < (ticks_ms2()%period_time) : #egress time
        for i in range(100):
            last_egress_throttle = run_pid_egress()
            wdt.feed()
        if leader_or_follower == "leader":
            main_perc = combine_percs(check_pot(),mqtt_perc)
            cp_egress = check_cp_egress()
        pid_egress.setpoint = cp_egress
        p, i, d = pid_egress.components
        print(" sp:", pid_egress.setpoint, " p:",check_actual_pressure()," throttle:", last_egress_throttle)#, " timemodulo:", ticks_ms()%period_time )
    pid_egress.set_auto_mode(False)


