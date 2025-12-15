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

# tach_ingress = Pin(2, Pin.IN, Pin.PULL_UP) 
# tach_egress = Pin(3, Pin.IN, Pin.PULL_UP)
# def det_rpm_interval(pin, interval):
#     blip_count = 0
#     meas_spacing_timer = ticks_us()
#     was_1 = 0
#     first_edge = 1
#     between_edges_time_us = 0
#     while ticks_diff(ticks_us(), meas_spacing_timer)/1_000_000 <= interval:
#         if pin.value() == 1:
#             was_1 = 1
#         if pin.value() == 0 and was_1 == 1 and first_edge == 1:
#             between_edges_timer = ticks_us()
#             was_1 = 0
#             first_edge = 0
#         if pin.value() == 0 and was_1 == 1 and first_edge == 0:
#             between_edges_time_us += ticks_diff(ticks_us(),between_edges_timer)
#             between_edges_timer = ticks_us()
#             blip_count += 1
#             was_1 = 0
#     if blip_count != 0:
#         between_edges_average = between_edges_time_us/blip_count
#         rps = 1000000/(between_edges_average*2)
#         rpm = rps*60
#     if blip_count == 0:
#         #print("no blips")
#         rpm = 0
#     if pin == tach_egress:
#         rpm = -rpm
#     return rpm
def calc_total_boost(boost_adjust,rel_boost, spd):
        total_boost = (boost_adjust * rel_boost) # give it a hundred percent power for a while as a boost
        if  abs(spd) > 52 and abs(spd) < 88:
            total_boost = ((boost_adjust * 1.4 * rel_boost)) # just boost the shit out of it to collect data, run again with more practical run to see what stall looks like just extra boost for that region to get it started in high winds
        if  abs(spd) >= 12 and abs(spd) < 30:
            total_boost = ((boost_adjust * 2 * rel_boost))
        if  abs(spd) >= 7.5 and abs(spd) < 12:
            total_boost = ((boost_adjust * 3 * rel_boost))
        return total_boost

def boost_two_fans(time1, time2, fan1_spd_func, fan2_spd_func, destination_spd1, destination_spd2):
    timer = ticks_ms()
    if time1 > time2:
        larger_time = time1
    if time2 >= time1:
        larger_time = time2
    done = 0
    if time1 != 0:
        fan1_spd_func(100)
    if time2 != 0:
        fan2_spd_func(100)
    while done == 0:
        if ticks_diff(ticks_ms(),timer) >= time1:
            fan1_spd_func(destination_spd1)
        if ticks_diff(ticks_ms,timer) >= time2:
            fan2_spd_func(destination_spd2)
        if ticks_diff(ticks_ms(),timer) >= larger_time:
            done = 1
    fan1_spd_func(destination_spd1)
    fan2_spd_func(destination_spd2)
    #print("boosting complete")
    return
combi_ingress_spd = 0
combi_egress_spd = 0
old_spd_ingress2 = 0
old_spd_egress2 = 0
def combi_fan_spd(spd, spd2):
    global combi_ingress_spd
    global combi_egress_spd
    global old_spd_ingress2
    global old_spd_egress2 
    boost_adjust = 0.02 #seconds so for 100 percent diff 100x this many seconds of boost
#     if -7.5 <= spd <= 7.5:  # if it's too low set them to zero.
#         combi_ingress_spd = 0 
#         combi_egress_spd = 0 # remember what you set it to.
#         E_fan_spd(combi_egress_spd)
#         I_fan_spd(combi_ingress_spd)
#     if -7.5 <= spd2 <= 7.5:  # if it's too low set them to zero.
#         old_spd_ingress2 = 0
#         old_spd_egress2 = 0
#         E_fan2_spd(0)
#         I_fan2_spd(0)
    if  spd >= 0 and (spd - combi_ingress_spd) >= 0: # if it's commanded to ingress and more than it was
        combi_egress_spd = 0
        E_fan_spd(combi_egress_spd)
        rel_boost = spd - combi_ingress_spd
        total_boost1 = calc_total_boost(boost_adjust,rel_boost, spd)
    #    print("1a")
    if  spd < 0 and (abs(spd) - combi_egress_spd) > 0:
        combi_ingress_spd = 0
        I_fan_spd(combi_ingress_spd)
        rel_boost = abs(spd) - combi_egress_spd
      #  print("1b")
        total_boost1 = calc_total_boost(boost_adjust,rel_boost, spd)  
    if  spd2 >= 0 and (spd2 - old_spd_ingress2) >= 0:
        old_spd_egress2 = 0
        E_fan2_spd(0)
        rel_boost = spd2 - old_spd_ingress2
        total_boost2 = calc_total_boost(boost_adjust,rel_boost, spd2)
     #   print("1c")
    if  spd2 < 0 and (abs(spd2) - old_spd_egress2) > 0:
        old_spd_ingress2 = 0
        I_fan2_spd(0)
        rel_boost = abs(spd2) - old_spd_egress2
        total_boost2 = calc_total_boost(boost_adjust,rel_boost, spd2)
      #  print("1d")
        
    if  spd >= 0 and (spd - combi_ingress_spd) > 0: # if fan 1 is not fast enough and fan 1 is told to ingress
        combi_ingress_spd = spd
      #  print("2 branch entered")
        if spd2 >= 0 and (spd2 - old_spd_ingress2) >= 0:
            boost_two_fans(time1=total_boost1, time2=total_boost2, fan1_spd_func = I_fan_spd, fan2_spd_func = I_fan2_spd, destination_spd1 = spd, destination_spd2 = spd2)
      #      print(" 2b")      
        if spd2 < 0 and (abs(spd2) - old_spd_egress2) > 0:
            boost_two_fans(time1 = total_boost1, time2 = total_boost2, fan1_spd_func = I_fan_spd, fan2_spd_func = E_fan2_spd, destination_spd1 = spd, destination_spd2 = abs(spd2))       
      #      print(" 2c")
    if  spd < 0 and (abs(spd) - combi_egress_spd) > 0:
        combi_egress_spd = abs(spd)
       # print(("3 branch entered"))
        if spd2 >= 0 and (spd2 - old_spd_ingress2) >= 0:
            boost_two_fans(time1 = total_boost1, time2 = total_boost2, fan1_spd_func = E_fan_spd, fan2_spd_func = I_fan2_spd, destination_spd1 = abs(spd), destination_spd2 = spd2)
       #     print(" 3a")         
        if spd2 < 0 and (abs(spd2) - old_spd_egress2) > 0:
            boost_two_fans(time1 = total_boost1, time2 = total_boost2, fan1_spd_func = E_fan_spd, fan2_spd_func = E_fan2_spd, destination_spd1 = abs(spd), destination_spd2 = abs(spd2))
       #     print(" 3b")
        
    if  spd >= 0 and (spd - combi_ingress_spd) <= 0: # if ingress on fan 1 and speed is being reduced  just set reduced speed immediately
        combi_ingress_spd = spd
        I_fan_spd(spd)
        combi_egress_spd = 0
        E_fan_spd(0)
     #   print("passed fan 1 zero or decreasing test:")
        if spd2 >= 0 and (spd2 - old_spd_ingress2) > 0:
            boost_two_fans(time1 = 0, time2 = total_boost2, fan1_spd_func = I_fan_spd, fan2_spd_func = I_fan2_spd, destination_spd1 = spd, destination_spd2 = spd2)
                     
        if spd2 < 0 and (abs(spd2) - old_spd_egress2) > 0:
     #       print("passed egress speed increase test for fan 2, no change or speed decrease for 1")
            boost_two_fans(time1 = 0, time2 = total_boost2, fan1_spd_func = I_fan_spd, fan2_spd_func = E_fan2_spd, destination_spd1 = spd, destination_spd2 = abs(spd2))
        
    if  spd < 0 and (abs(spd) - combi_egress_spd) <= 0: # if egress on fan 1 and speed is being reduced just set reduced speed immediately
        combi_egress_spd = abs(spd)
        E_fan_spd(abs(spd))
        combi_ingress_spd = 0
        I_fan_spd(0)
 #       print(" 4")
        if spd2 >= 0 and (spd2 - old_spd_ingress2) > 0:
            boost_two_fans(time1 = 0, time2 = total_boost2, fan1_spd_func = E_fan_spd, fan2_spd_func = I_fan2_spd, destination_spd1 = abs(spd), destination_spd2 = spd2)
      #      print(" 4a")        
        if spd2 < 0 and (abs(spd2) - old_spd_egress2) > 0:
            boost_two_fans(time1 = 0, time2 = total_boost2, fan1_spd_func = E_fan_spd, fan2_spd_func = E_fan2_spd, destination_spd1 = abs(spd), destination_spd2 = abs(spd2))
  #          print(" 4b")
    if  spd2 >= 0 and (spd2 - old_spd_ingress2) <= 0: # if ingress on fan 2 speed is being reduced just set reduced speed immediately
        old_spd_ingress2 = spd2
        I_fan2_spd(spd2)
        old_spd_egress2 = 0
        E_fan2_spd(0)
    #    print(" 5")
        if  spd >= 7.5 and (spd - combi_ingress_spd) > 0: # if it's not as fast as the latest command
            boost_two_fans(time1 = total_boost1, time2 = 0, fan1_spd_func = I_fan_spd, fan2_spd_func = I_fan2_spd, destination_spd1 = spd, destination_spd2 = spd2)
     #       print(" 5a")
        if  spd < -7.5 and (abs(spd) - combi_egress_spd) > 0:
            boost_two_fans(time1 = total_boost1, time2 = 0, fan1_spd_func = E_fan_spd, fan2_spd_func = I_fan2_spd, destination_spd1 = abs(spd), destination_spd2 = spd2)
    #        print(" 5b")
    if  spd2 < 0 and (abs(spd2) - old_spd_egress2) <= 0: # if egress on fan 2 and speed is being reduced just set reduced speed immediately
        old_spd_egress2 = abs(spd2)
        E_fan2_spd(abs(spd))
        old_spd_ingress2 = 0
        I_fan2_spd(0)
     #   print(" 6")
        if  spd >= 7.5 and (spd - combi_ingress_spd) > 0: # if it's not as fast as the latest command
            boost_two_fans(time1 = total_boost1, time2 = 0, fan1_spd_func = I_fan_spd, fan2_spd_func = E_fan2_spd, destination_spd1 = spd, destination_spd2 = abs(spd2))
     #       print(" 6a")
        if  spd < -7.5 and (abs(spd) - combi_egress_spd) > 0:
            boost_two_fans(time1 = total_boost1, time2 = 0, fan1_spd_func = E_fan_spd, fan2_spd_func = E_fan2_spd, destination_spd1 = abs(spd), destination_spd2 = abs(spd2))
     #       print(" 6b")
    return 
combi_fan_spd(0,0)
#sys.exit()

