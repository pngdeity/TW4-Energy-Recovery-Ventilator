from machine import PWM, Pin
from time import sleep, ticks_ms, ticks_us, ticks_diff
import sys
ingress_fan = PWM(Pin(0))
ingress_fan.freq(70000)
def I_fan_spd(spd_prcnt):
        if spd_prcnt > 100:
            spd_prcnt = 100
        if spd_prcnt < 0:
            spd_prcnt = 0
        if spd_prcnt < 7.5:
            spd_prcnt = 0
        duty = spd_prcnt*65530/100
        duty = int(duty)
        if duty <0:
            duty = 0
        ingress_fan.duty_u16(duty)
        return spd_prcnt
egress_fan = PWM(Pin(1))
egress_fan.freq(70000)
def E_fan_spd(spd_prcnt):
        if spd_prcnt > 100:
            spd_prcnt = 100
        if spd_prcnt < 0:
            spd_prcnt = 0
        if spd_prcnt < 7.5:
            spd_prcnt = 0
        duty = spd_prcnt*65530/100
        duty = int(duty)
        if duty <0:
            duty = 0
        egress_fan.duty_u16(duty)
        return spd_prcnt
ingress_fan2 = PWM(Pin(2))
ingress_fan2.freq(20_000)
def I_fan2_spd(spd_prcnt):
        if spd_prcnt > 100:
            spd_prcnt = 100
        if spd_prcnt < 0:
            spd_prcnt = 0
        if spd_prcnt < 7.5:
            spd_prcnt = 0
        duty = spd_prcnt*65530/100
        duty = int(duty)
        if duty <0:
            duty = 0
        ingress_fan2.duty_u16(duty)
        return spd_prcnt

egress_fan2 = PWM(Pin(3))
egress_fan2.freq(20_000)
def E_fan2_spd(spd_prcnt):
        if spd_prcnt > 100:
            spd_prcnt = 100
        if spd_prcnt < 0:
            spd_prcnt = 0
        if spd_prcnt < 7.5:
            spd_prcnt = 0
        duty = spd_prcnt*65530/100
        duty = int(duty)
        if duty <0:
            duty = 0
        egress_fan2.duty_u16(duty)
        return spd_prcnt
def calc_persistence_time(old_throttle, destination_throttle, other_fan_destination_throttle = 50):
    if old_throttle >= 80:
        persistence_time = (old_throttle - destination_throttle)*0.0002*1000 #the coefficient is seconds per percent throttle so for full swing from  -100 to 100 it would be 2 seconds if 0.01
    if old_throttle > 40 and old_throttle < 80:
        persistence_time = (old_throttle - destination_throttle)*0.02*1000
    if old_throttle <= 40:
        persistence_time = (old_throttle - destination_throttle)*0.13*1000
    #print("persistence time:",persistence_time)
    return persistence_time  #we may make it a polynomial or something some other day or depend in a structured way on the old and new throttle                    
start_clock_ms = 0
ingress0_old_throttle = 0
egress0_old_throttle = 0
ingress1_old_throttle = 0
egress1_old_throttle = 0 
def ingress0_object(destination_throttle): #they don't go to the destintation immediately they get closer each time they are called according to time elapsed
    global start_clock_ms
    global ingress0_old_throttle
    adjusted_throttle = physthrottle_asfuncoftime(start_clock_ms, ingress0_old_throttle, destination_throttle)
    #print("ingress throttlwe:",adjusted_throttle)
    I_fan_spd(adjusted_throttle)
    result = False
    if adjusted_throttle == destination_throttle:
        ingress0_old_throttle = destination_throttle
        result = True
    return result
def egress0_object(destination_throttle):
    global start_clock_ms
    global egress0_old_throttle
    result = False
    #print("dest throttle:", destination_throttle)
    adjusted_throttle = physthrottle_asfuncoftime(start_clock_ms, egress0_old_throttle, destination_throttle)
    E_fan_spd(adjusted_throttle)
    #print("egress_throttle:",adjusted_throttle)
    if adjusted_throttle == destination_throttle:
        egress0_old_throttle = destination_throttle
        result = True
    return result
def ingress1_object(destination_throttle): #they don't go to the destintation immediately they get closer each time they are called according to time elapsed
    global start_clock_ms
    global ingress1_old_throttle
    adjusted_throttle = physthrottle_asfuncoftime(start_clock_ms, ingress1_old_throttle, destination_throttle)
    #print("ingress throttlwe:",adjusted_throttle)
    I_fan2_spd(adjusted_throttle)
    result = False
    if adjusted_throttle == destination_throttle:
        ingress1_old_throttle = destination_throttle
        result = True
    return result
def egress1_object(destination_throttle):
    global start_clock_ms
    global egress1_old_throttle
    result = False
    #print("dest throttle:", destination_throttle)
    adjusted_throttle = physthrottle_asfuncoftime(start_clock_ms, egress1_old_throttle, destination_throttle)
    E_fan2_spd(adjusted_throttle)
    #print("egress_throttle:",adjusted_throttle)
    if adjusted_throttle == destination_throttle:
        egress1_old_throttle = destination_throttle
        result = True
    return result
# def ingress1_object(destination_throttle):
#     global start_clock_ms
#     global ingress1_old_throttle
#     adjusted_throttle = physthrottle_asfuncoftime(start_clock_ms, ingress1_old_throttle, destination_throttle)
#     E_fan2_spd(adjusted_throttle)
#     result = False
#     if adjusted_throttle == destination_throttle:
#         ingress1_old_throttle = destination_throttle
#         result = True
#     return result
# def egress1_object(destination_throttle):
#     global start_clock_ms
#     global egress1_old_throttle
#     adjusted_throttle = physthrottle_asfuncoftime(start_clock_ms, egress1_old_throttle, destination_throttle)
#     I_fan2_spd(adjusted_throttle)
#     result = False
#     if adjusted_throttle == destination_throttle:
#         egress1_old_throttle = destination_throttle
#         result = True
#     return result
def physthrottle_asfuncoftime(start_clock_ms, old_throttle, destination_throttle): #for each physical fan this function is applied. should have other fan's destination to determine persistence time but it's usually similar
    time_elapsed = ticks_diff(ticks_ms(),start_clock_ms) #time elapsed since combi_fan was called to adjust fan speeds
    if old_throttle < 75:
        ramp_down_time_ms = old_throttle*0.03*1000+1
    if old_throttle >= 75:
        ramp_down_time_ms = old_throttle*0.03*1000+1
    #print("ramp_down_time:",ramp_down_time_ms)
    if destination_throttle == 0:
        persistence_time = calc_persistence_time(old_throttle, destination_throttle)
        if time_elapsed < persistence_time:
            return old_throttle
        if time_elapsed >= persistence_time:
            fraction_done_ramp_down = (time_elapsed - persistence_time)/ramp_down_time_ms
            if fraction_done_ramp_down >= 1:
                return 0
            fraction_remaining = 1 - fraction_done_ramp_down
            if fraction_remaining <= 0:
                return 0
            else:
                return old_throttle*fraction_remaining
            
    else: # we might use this later to implement some kind of boost if destination is higher than old throttle esp zero to jump the capacitor
        return destination_throttle
def speed_to_action(speed, ingress_fanfunc, egressfanfunc):
    
    if speed < 0:
        r1 = ingress_fanfunc(0)
        r2 = egressfanfunc(abs(speed))
    if speed >= 0:
        r1 = ingress_fanfunc(speed)
        r2 = egressfanfunc(0)
    return r1, r2
def combi_fan_spd(spd, spd2): # spd is the main fan pair, -100 to 100, used in the tw4, spd2 is the shadow/mirror fan, used in the left side of the wm12.
    global start_clock_ms
    start_clock_ms = ticks_ms()
    r1, r2 = False, False
    r3, r4 = False, False
    while r1 == False or r2 == False or r3 == False or r4 == False:
        r1,r2 = speed_to_action(spd, ingress0_object, egress0_object)
        r3,r4 = speed_to_action(spd2, ingress1_object, egress1_object)
    #print("done adjusting fansapparently")
    return 
combi_fan_spd(0,0)
#sys.exit()

