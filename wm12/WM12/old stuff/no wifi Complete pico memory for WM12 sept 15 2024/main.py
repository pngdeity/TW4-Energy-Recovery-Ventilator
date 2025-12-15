import sdp810_125
from combifan import combi_fan_spd
from machine import PWM, Pin, ADC
from simple_pid import PID
from time import sleep, ticks_ms, ticks_diff
from machine import WDT
sleep(2)
print(sdp810_125.get_reading())
I_gain = 2
P_gain = 0.8 
pid_ingress = PID(P_gain,I_gain,0, setpoint = 15)
pid_ingress.output_limits = (-100, 100)
pid_egress = PID(P_gain,I_gain,0, setpoint = 15)# pid2 is egress
pid_egress.output_limits = (-100, 100)
potpinadc = ADC(Pin(28))
oldpot_val =0
read_fail_strikes = 0
def check_pot():
    global oldpot_val
    read = potpinadc.read_u16()
    if abs(read-oldpot_val)>1600:
        oldpot_val = read
        return read/655.53
    return oldpot_val/655.53
def percent_to_pressure(perc):
    pressure = perc*0.076
    if pressure > 7.6:# the actual pressure is divided because the sensor actually allows flow through it 
        pressure = 7.6
    if pressure < -7.6:
        pressure = -7.6
    if -1.5 < pressure < 1.5:
        pressure = 0
    return pressure
def check_cp_ingress():
    percent = check_pot()
    pressure = percent_to_pressure(percent)
    return pressure
def check_cp_egress(): # we might want a pressure bias some day so have separate functions to calculate ingress and egress pressures
    percent = check_pot()
    pressure = -1*percent_to_pressure(percent)
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
    perc_power = check_pot()
    max_time = 120_000
    prop_time = 50_000/(perc_power/100)
    if prop_time >max_time:
        prop_time = max_time
    return prop_time
oldpressure = 0
def check_actual_pressure():
    global oldpressure
    global read_fail_strikes
    try:
        sleep(0.01)
        pressure = sdp810_125.get_reading()
    except BaseException as error: # covers all errors
        print("error, probably comm error with pressure sensor:", error)
        read_fail_strikes += 1
        if read_fail_strikes > 5: #if it fails to read more than 5 times in a row
            sleep(10)#reset the whole system by triggering watchdog
        return oldpressure
    oldpressure = pressure
    read_fail_strikes = 0
    return pressure
last_ingress_throttle = 0
last_egress_throttle = 0
#wdt = WDT(timeout = 5000)
while True:
    #wdt.feed()
    period_time = period_time_calc()
    combi_fan_spd(last_ingress_throttle,last_egress_throttle)
    cp_ingress = check_cp_ingress()
    comm_timer = ticks_ms()
    while ticks_diff(ticks_ms(),comm_timer)<6_000:
        #wdt.feed()
        pass
    pid_ingress.setpoint = cp_ingress
    pid_ingress.set_auto_mode(True, last_output=last_ingress_throttle)
    while (ticks_ms()%period_time) < period_time/2: #if ingress section run ingress pid     
        for i in range(100):
            last_ingress_throttle = run_pid_ingress()
            #wdt.feed()
            #print(i)
        cp_ingress = check_cp_ingress()
        pid_ingress.setpoint = cp_ingress
        p, i, d = pid_ingress.components
        print(" sp:", pid_ingress.setpoint, " p:",check_actual_pressure()," throttle:", last_ingress_throttle) #," timemodulo:", ticks_ms()%period_time)
    pid_ingress.set_auto_mode(False)
    combi_fan_spd(last_egress_throttle, last_ingress_throttle)
    cp_egress = check_cp_egress()
    comm_timer = ticks_ms()
    while ticks_diff(ticks_ms(),comm_timer)<6_000:
        #wdt.feed()
        pass
    pid_egress.setpoint = cp_egress
    pid_egress.set_auto_mode(True, last_output=last_egress_throttle)
    while period_time/2 < (ticks_ms()%period_time) : #egress time
        for i in range(100):
            last_egress_throttle = run_pid_egress()
            #print(i)
            #wdt.feed()
        cp_egress = check_cp_egress()
        pid_egress.setpoint = cp_egress
        p, i, d = pid_egress.components
        print(" sp:", pid_egress.setpoint, " p:",check_actual_pressure()," throttle:", last_egress_throttle)#, " timemodulo:", ticks_ms()%period_time )
    pid_egress.set_auto_mode(False)