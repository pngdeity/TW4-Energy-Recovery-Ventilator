from math import log, e
from machine import Pin, ADC, PWM
from time import sleep
from filter2 import lowpass_filter
import sys
unpowered_therm_adc = ADC(Pin(27))
powered_therm_adc =ADC(Pin(28))
led=Pin('LED', Pin.OUT)
led.on()

beta_unpowered =3950
beta_powered =3950
R0_unpowered = 5000
R0_powered = 5000

#calibration_constant_powered_therm = 1  # this is in units of meters per second per milliwatt-degree

T0_unpowered = 298.15 #this has to be in kelvin not celcius
T0_powered = 298.15
unpowered_supply_v = 3.3
powered_supply_v = 12

sense_r_unpowered = 4700
sense_r_powered = 100

resistance_current_limit_unpowered = 4700 #(includes sense resistance)
resistance_current_limit_powered = 300 #includes sense resistance

def check_temps(unpowered_therm_adc, powered_therm_adc):
    global sense_r_unpowered
    global sense_r_powered
    global unpowered_supply_v
    global powered_supply_v
    global unpowered_supply_v
    global powered_supply_v
    global resistance_current_limit_unpowered
    global resistance_current_limit_powered
    global beta_unpowered 
    global beta_powered
    global R0_unpowered 
    global R0_powered 
    global T0_unpowered 
    global T0_powered
    global current_unpowered
    global therm_unpowered_power
    global therm_powered_power
    voltage_unpowered_sense = (unpowered_therm_adc.read_u16()/65356)*3.3
    voltage_powered_sense = (powered_therm_adc.read_u16()/65356)*3.3

    current_unpowered = voltage_unpowered_sense/(sense_r_unpowered)
    current_powered = voltage_powered_sense/(sense_r_powered)

    total_resistance_unpowered = unpowered_supply_v/current_unpowered
    total_resistance_powered = powered_supply_v/current_powered

    therm_r_unpowered = total_resistance_unpowered-resistance_current_limit_unpowered
    therm_r_powered = total_resistance_powered-resistance_current_limit_powered

    voltage_therm_unpowered = unpowered_supply_v*(therm_r_unpowered/total_resistance_unpowered)
    voltage_therm_powered = powered_supply_v*(therm_r_powered/total_resistance_powered)
    
    therm_unpowered_power = current_unpowered*voltage_therm_unpowered
    therm_powered_power = current_powered*voltage_therm_powered
    
    T_unpowered = beta_unpowered/log(therm_r_unpowered/(R0_unpowered*(e**(-1*beta_unpowered/T0_unpowered)))) #remember this is in kelvin not celcius
    T_powered = beta_powered/log(therm_r_powered/(R0_powered*(e**(-1*beta_powered/T0_powered))))
    return T_unpowered, T_powered

last_t_above_ambient = 0
last_airspeed_proxy = 0 
def check_airspeed_proxy(T_unpowered, T_powered):
    global last_t_above_ambient
    global last_airspeed_proxy
    a=3 # this is the coefficient between temperature change and heat loss so thermal inertia basically
    t_above_ambient = T_powered - T_unpowered
    temp_diff_change = last_t_above_ambient-t_above_ambient    
    equilib_temp_diff_proxy = t_above_ambient - a*(temp_diff_change) # the higher the rate of change, the further from equilibrium you are
  #  if airspeed_proxy < 0:
   #     airspeed_proxy = 0
    last_t_above_ambient = t_above_ambient
    return 120-equilib_temp_diff_proxy

# sys.exit()
# 
# T_unpowered, T_powered = check_temps(unpowered_therm_adc, powered_therm_adc)
# airspeed_proxy = check_airspeed_proxy(T_unpowered, T_powered)
# print(airspeed_proxy, " t_u: ", T_unpowered, " t_p: ", T_powered)

while True:
    sleep(0.1)
    T_unpowered, T_powered = check_temps(unpowered_therm_adc, powered_therm_adc)
    airspeed_proxy = check_airspeed_proxy(T_unpowered, T_powered)
    #print(airspeed_proxy, " t_u: ", T_unpowered, " t_p: ", T_powered)
    print(airspeed_proxy)