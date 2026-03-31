# TW4 Energy Recovery Ventilator Manual

V1.0 BETA

# Introduction

The TW4 energy recovery ventilator is a machine that harvests heat
energy and water vapor from outgoing ventilation air, and transfers it
to incoming air. It has ten to about 28 times the performance to cost
ratio and rate of return on investment of the next best machines in its
class (decentralized), and about four times better than even the next
best energy recovery ventilators available for home of the ducted type,
if you already have the ducting even, depending on how you count it.

It is made to last for a very long time, free of planned obsolescence,
and to be produced in a way that provides living wage jobs that have
relatively good working conditions and an open future.

It is made partly with methods and techniques that are normally
considered for prototyping. This makes it very flexible and has allowed
me to refine the design in several departments to a much higher degree
than is conventionally possible.\
\
However it is for now still in beta. Also each unit is assembled partly
by hand. This manual is focussed primarily on the fully assembled and
tested units (except they need to be partially dismantled for shipping
and installation).

# Unpacking/checking everything is there and not broken

Parts/packing list:

  -------------------------------------------------
  **Heavy duty attenuator, fabricate    quantity
  your own attenuator version**         
  ------------------------------------- -----------
  item                                  

  Indoor plate/cover module             2

  fan module                            2

  extension cables                      2

  power supplies                        2

  Heat exchangers                       2

                                        

  **Splitter version, with pipes**      

  item                                  

  printed noise splitter with bolt and  2
  nut and fans installed                

  Splitter mylar hat                    2

  extension segment (3 pin connectors   2
  on both ends)                         

                                        2

                                        

                                        

                                        

                                        

  pipes                                 2

                                        
  -------------------------------------------------

*Table 1.*

# Anatomy of the TW4 and how it works in general - heavy duty sound attenuator version

## Anatomy ![](media/image7.jpg){width="6.5in" height="6.859375546806649in"}

## Indoor plate and cover module:![](media/image6.jpg){width="6.5625in" height="5.09375in"}

## Indoor plate with cover removed:![](media/image3.jpg){width="6.5in" height="4.875in"}![](media/image5.jpg){width="6.666666666666667in" height="6.8125in"}

*Fan module for heavy duty attenuator version.*

## 

## Issues to be aware of in general

- Do not pull on the wires on the connectors, the metal from which the
  wires are made is not that strong. Disconnect the connectors by
  exerting force on the body of the plastic connector area, not by
  pulling on the wires.

- If the power level is less than 17% (software cutoff), it gets rounded down to
  zero.

- The software limits the maximum pressure setpoint to **34 PA** for TW4 units to protect the fan motors and maintain efficiency.
- If the power level is zero percent, the system will try to maintain a
  zero pressure across the heat exchanger i.e. pressure regulation is
  still active This may cause the fan to actually be on slightly if
  there is a static pressure caused by wind or other forces. It is
  fighting unbalanced air intrusion, which eliminates unwanted heat
  loss.

- The networking/communication only happens once every cycle. A cycle is
  between 50 and 90 seconds long, depending on the power level (longer
  for lower power levels). So commands from MQTT and propagation of
  power level from leader to follower can take up to 90 seconds.

## Description of overall working process during energy recovery mode

Basically each TW4 module has a pressure sensor that detects the air
pressure across the heat exchanger and regulates it to the commanded
level using 2 separate Proportional Integral (PI) control loops, one for
ingress and one for egress. It stores state of the applicable control
loop and switches from ingress to egress or egress to ingress then
restores the state of the applicable control loop every 20-45 seconds
(half the "Ventilation Cycle duration").

This causes it to compensate for wind, up to reasonable wind levels, but
the fans are not able to compete with strong winds. There is an
automatic storm valve add on which can be used in the future to block
the system in the event of a storm.

The Ventilation Cycle duration is determined partly by the power level, it is longer at
lower power levels to further reduce perceived noise and improve average
flow (flow is suppressed slightly during the direction reversal).

The leader and follower synchronize their clocks over wifi so the fan
reversals are synchronized.

They synchronize by the leader broadcasting UDP packets at the start of every Ventilation Cycle (UDP Port 12345),
containing the clock time and power level. A cycle is a full
ingress-egress cycle. It therefore takes up to 90 seconds for
information to propagate. The follower will not turn it's fans on unitl
it receives a synch packet, for every cycle.

The knob on the follower is inert, it will be used in the future with a
firmware update that allows the power level to be changed using either
knob.

The power level can also be changed over MQTT, and can therefore be
controlled by a smartphone or home automation system.

The leader needs to know the ip address of the follower, it must be in
the configuration file. The devices ship by default with this already
configured.

The devices work as is by themselves out of the box, but if you want to
connect to wifi for additional features, you need to edit the
configuration file using a program called Thonny running on a desktop or
laptop, and a usb-micro cable.

The microcontroller runs Micropython, a human readable and easy to edit
yet full powered programming language. The programs are not compiled,
they are stored on the microcontroller, called a Pico W, and can be
edited like a text file on a thumb drive through a program running on a
PC called Thonny. The PC connects to the Pico using a micro usb cable.

The configuration of the TW4 is drawn from a file on the pico,
persistent_vars.json. This is a text file which is also machine
readable. You can edit it directly but be careful not to insert extra
spaces in the wrong place or whatever. Capitals matter, everything has
to be exact.

Future features will include the ability to do only ingress, only
egress, or slightly pressure bias in one direction, and control each
module separately.

# Sound attenuation choices

## Heavy duty sound attenuator 

The TW4 can be used with a heavy duty sound attenuator made using
hardware store parts and pipe, which also blocks a lot of
traffic/exterior noise, or a 3d printed "noise splitter" which is
cheaper and lighter and blocks the fan noise about as well but does not
block as much exterior noise.

Right now the heavy duty attenuators are not for sale from me, you just
make one yourself, because shipping would be costly and all parts are
available locally, and this allows me to focus on the core offering.
There is a document here which describes it and the assembly/fabrication
process:

[[https://docs.google.com/document/d/1jhOIYxr6VYDhxBGIlXFxPUYev6MeVffLbuaWy17LuUc/edit?usp=sharing]{.underline}](https://docs.google.com/document/d/1jhOIYxr6VYDhxBGIlXFxPUYev6MeVffLbuaWy17LuUc/edit?usp=sharing)

![](media/image10.jpg){width="2.2083333333333335in"
height="8.666666666666666in"}

## Sound splitter

The default option is a cheaper, lighter, smaller option, which blocks
the fan noise about as well but does not attenuate exterior traffic
noise etc. as well. The fans are on the bottom of the white plastic
object. The "hat" on the top is acoustically transparent - sound tends
to mostly pass right through it. The fan noise comes up the central pipe
and goes right through the hat, while the air makes a few turns and goes
into the green pipe. The hat is conical so it can resist negative
pressure while air is being sucked out of the house. The uv resistance
may be less than the heavy duty attenuator, the hat may need to be
replaced after 20 years. It is just mylar (BOPET).

![](media/image4.jpg){width="3.9375in" height="5.6480304024496935in"}

## Further attenuation

There are two tricks, which I do not employ due to complexity and cost,
but can be employed by a do-it-yourselfer who seeks further noise
reduction.

One is the replacement of the fiberglass in the interior cover with
viscoelastic foam. Earplugs can be used. It takes about 180 standard
earplugs. Mosquito mesh might be a good idea under the grille, to keep
them in reliably. See picture below.

The second is to use viscoelastic foam to line the pipe in some region,
either before or after the heat exchanger. This requires the pipe to be
longer than the heat exchanger, but this may occur anyway with some
walls, and it can stick out on the exterior side. A space needs to be
left between the end of the foam and the beginning of the heat
exchanger. The foam will need to be removed in some circumstances, so
don't glue it in place. A 3d printed mesh-walled can of about 148 mm
outer diameter - the inner diameter of the pipe is 149 but it's not
always that round - with no center (so the air can flow through the
center but sound waves that hit the walls are largely absorbed),
basically, filled with earplugs, would make a lot of sense actually, as
a good diy option. Again, use modified pla, not standard pla or it's
likely to crack over time. The longer this segment is, the better, I
only tested one segment 10 cm long.

Both of these measures, during testing, gave reductions of 2-3 dBa each.
Together they could provide considerable reduction, allowing the TW4 to
operate at 60 CFM with only 35 dBa of noise or something, but I have not
tested everything together actually installed in a wall yet. The sheets
of foam are hard to source, and I have no good sources for them.
Neoprene foam is commonly used in this role but I don't think it would
work as well as viscoelastic foam. The earplugs work pretty well and
they aren't prohibitively expensive for a one off diy thing that will
last for many many years. Remember they lose their viscosity properties
if they are washed, they become elastic only, so probably not a good
idea to let them get wet either.

These measures may be attractive if the unit is used in an office or
bedroom.

![](media/image12.jpg){width="6.5in" height="5.145833333333333in"}

## No attenuator option

The fan module used with the heavy duty attenuator can also just be
inserted direction into the pipe, cutting costs. It should probably be
some distance inside the pipe at least, to prevent inhalation of rain.
The fans are waterproof, but you don't want rain getting sucked in and
then blown inside. A pipe elbow or similar can be used as a hood, there
are also hoods made from sheet metal that connect to a six inch pipe.
This does not provide much sound attenuation and would be only suitable
in the case of a basement or cafe something where noise is not
important, due to the lack of people or due to high ambient noise
anyway.

![](media/image2.jpg){width="5.322916666666667in"
height="5.7105304024496935in"}

The interior cover also contains fiberglass which helps attenuate noise
quite a bit. This is always included.

# Accessories

I have designed an exterior plate to which filters, valves, etc. can
attach, which clamps on to the green pipe, and also to the bottom of the
noise splitter. You can rotate the sound splitter sideway or leave it
upright. Same for the heavy duty attenuator, rotating it sideways might
get complicated because it would be heavier on one side than the other,
exerting some rotational force.

To this plate can be attached a hepa filter, as shown below. It is a
Bosch HEPA filter for a car. Adapters can be produced for other filters.
There is an adapter for 8 inch furnace filters but the filters
themselves may not do well in the rain. There is also a storm valve
available.

![filter module attached to plate ](media/image8.jpg){width="4.625in"
height="5.90625in"}![](media/image9.jpg){width="4.90625in"
height="5.6875in"}![](media/image11.jpg){width="4.208333333333333in"
height="5.177083333333333in"}

# Qualitative features list

- **Very short payoff period.** This is the ratio of the capital cost to
  net financial savings, given the cost of energy. This varies from 1.5
  years for electric resistance heat to 3.5 years for heat pump supplied
  heat, depending on the area, both how cold the weather is and the cost
  of energy and how high the unit is turned up. See spreadsheet on the
  website for details specific to you.

- Can be controlled over wifi, including by using a bridge to Alexa,
  Google Home, Matter and other home automation systems, and from a
  phone using MQTT apps.

- Repairable, this improves the payoff period by extending de facto
  lifespan and reducing maintenance cost.

# Beta issues to be aware of

- The follower takes a full cycle to get an update regarding the power
  level from the leader. **So if you change the power level with the
  knob or mqtt, it may take from 50 to even 90 seconds (the lower the
  power level the longer the cycle period) to stabilize/update
  everything. This will be improved with a future firmware update.**

- There is no way to configure the modules/pair with an easy web
  interface or anything. You have to connect by micro usb cable and edit
  a configuration file. A configuration file is used, but a bit of a hassle. You aren't
  expected to do it very often.

- The fit of the sound splitter to the pipe is a bit tight, chamfer the
  pipe edge to get it on.

- The fit of the indoor plate is a bit tight, chamfer the pipe to get it
  to fit easily. You don't really need to tighten the screw, it is
  redundant.

# Performance specs, per pair of modules:

  -----------------------------------------------------------------------
  Spec                                Value
  ----------------------------------- -----------------------------------
  Max actual net fresh air flow       60 CFM

  Power supply voltage                12 Volts

  Power supply current requirement    1.5 Amps max (during fan
                                      acceleration)

  Expected actual average             85%
  season-round efficiency at 60 cfm,  
  including water vapor/latent heat   
  if silica gel coated. Varies little 
  with conditions.                    

  Expected actual average             90%
  season-round efficiency at 30 cfm   
  including water vapor/latent heat   
  if silica gel coated. Varies little 
  with conditions.                    

  Noise emission at 1 meter in front  30 dBa
  of unit, at 15 CFM (printed         
  splitter or heavy duty attenuator   
  are about the same.)                

  Noise emission at 1 meter in front  35 dBa
  of unit, at 30 CFM                  

  Noise emission at 1 meter in front  42 dBa
  of unit, at 60 CFM, with optional   
  extra pipe segments.                

  Wind resistance rating (from        S1 (less than 6 CFM at 20 pascals
  in-house measurements, not yet      wind pressure, total excess flow in
  certified)                          or out).

  Average power consumption at 60 CFM 9 Watts

  Average power consumption at 30 CFM 5 Watts

  Design life                         Parts can be replaced indefinitely.

  Fan bearing life span, expected     7-12 years elapsed time during
                                      normal use

  CE mark certification               Not yet.

  Underwriter's laboratory            Not yet, the power supply is UL
  certification                       listed, though.
  -----------------------------------------------------------------------

*Table 2.*

Rohs compliant.

Contains no toxic or hazardous materials.

Made in freedom.

# Installation

## Installation of the pipe

As of October 13, 2024, it remains on my list of things to do to
actually install a 6 inch pipe in a wall myself. However there are many
different types of walls, exterior coverings and so on. For this reason
it is not a simple undertaking and I cannot provide specific
instructions or advice specific to any given situation, aside from:

- The importance of avoiding avoiding plumbing and electrical lines and
  load bearing elements

- That it is a common procedure for many reasons and most good
  contractors know how to do it

- The pipe needs to be sealed on the exterior side effectively, where
  the house wrap is, and also on the vapor barrier side,

- and mechanically secured in the wall effectively, using caulk or PU
  foam, usually.

- The drill is kind of big and heavy and exerts a lot of torque, and
  looks like it would be hard to hold in place while drilling, for just
  one person.

- There are other ways aside from a core drill to cut a hole in a wall
  which are easier in some ways and harder in others.

- The pipe should be slanted 2-3 degrees to allow any water to run to
  the outdoors, this is true of almost any through-wall pipe.

- Be very careful the pipe sticks out enough on both sides.

- It may help to chamfer the ends of the pipe to get the other parts on,
  this is strongly recommended. Aggressive sandpaper or a chamfer tool
  can be used.

The standard core drills are slightly larger than the pipe (150 mm is
the nominal dimension, it is 159 mm diameter on the outside, typical
core drill of this size is a 162 mm drill) so you do not need to make
the hole slanted on purpose, generally. Just cut it perpendicular to the
wall and there is enough space to slant the pipe.

Rubber wall grommets can be had for about \$15 each and are a good way
to seal the pipe to the vapor barrier or house wrap in a new build
especially, but are a bit hard to use in a retrofit. Polyurethane foam
and Tuck tape is generally the way to go with retrofits.

To cut a pipe square, there is a good trick using a band of plastic (can
be packing tape), or sheet of PET or sheets of paper taped together.
Make a single sheet that is at least 490 mm long (larger than the
circumference of a 159 mm diameter circle, which is the pipe), and wrap
it around the pipe such that it overlaps precisely with itself at the
ends, then tape it with masking tape to itself. This forms a circular
edge around the pipe which is aligned perpendicular to the central axis
of the pipe. Trace around the edge of this wrapped piece of paper with a
sharpie and you can mark the pipe effectively, then cut it with a hand
saw.

## 

## Electrical supply

You need to decide which kind you want, It is recommended to the wall wart at
first and you can always hard wire the electricity later. You can even
take a power supply of the type that can be used for hard wiring and
just put a plug on it and use that so you don't end up with an extra
power supply when the dust settles, and you have it for when you want to
hard wire it.

### Hard wired

Power supply goes in a junction box.

Power switch (a standard wall light switch is fine) goes before power
supply, not after. It needs a junction box too, of course. It can be the
same box as the power supply.

Electrician has to install the wires, or you can DIY carefully, the low
voltage side is easy but be careful on the 120 volt side.

### Wall wart style

This is a simple approach using a power supply that plugs into the
nearest outlet. You can get extension cables for these power supplies if
the cable is not long enough.

You can do a combination of wall wart and concealed wires using flat
speaker wire on the wall that can be painted over or similar.

## Installation of components after power supply and pipe is taken care of

Pictures coming before exiting beta.

Tools required:

- 1 2.5 mm \*ball end\* hex driver. A non-ball end will not fit to
  secure the indoor cover until the design is changed in this regard,
  but you also don't really need to tighten that screw, the cover stays
  on pretty well without it.

Procedure:

1.  Plug the extension cable into the fan.

2.  Put the sound attenuator on the outside and the extension wire
    through the pipe.

3.  Secure the sound attenuator to the through wall pipe: it may be a
    good idea to use some tape to secure the large heavy duty
    attenuator, just to be extra sure it cannot rotate due to high winds
    or anything as it is heavier on the top than the bottom. Transparent
    tuck tape is good and looks good.

4.  Make sure the indoor edge of the pipe is chamfered.

5.  Make sure the power supply is **not** connected to 120 volts, i.e.
    is not plugged in, or the switch is off, ideally turn the circuit
    breaker off.

6.  Remove the cosmetic cover and connect the DC power wires to the
    terminal block if you are using that kind of power supply option,
    otherwise there should be a 5.5 mm jack hanging out the side, so
    there is no need to remove the cosmetic cover. **Do not get the
    polarity backwards. Test with a multimeter if there is any
    uncertainty. Red is positive, black is negative for DC.** You can
    put the plate on the pipe for this step but you may need to take it
    off again in a minute.

7.  Put the cosmetic cover back on. You may need to take the plate off
    the pipe for this, and get someone to help hold it. Unfortunately it
    is a bit awkward to connect the power and then stuff the wires back
    under the cosmetic cover. It's even harder if the interior plate is
    already on the pipe, because you can't reach in to stuff the wires
    into posiion. I have no good solution for this right now except to
    organize the wires so it's easy to take the cover off/put it back on
    while the plate is attached to the pipe.

8.  Hold the interior cover/plate assembly in one hand, connect the
    extension wire for the fans to the assembly, and you have to finagle
    the pressure sensor tube and the wires into the notch at the top of
    the heat exchanger and slide the heat exchanger into the pipe,
    without pinching or jamming. Things should slide in with little
    force. There should be enough tube and wire to allow the parts to be
    held apart while doing this. Do not pull hard on the sensor tube or
    wires. The wires and tube should both slide if pulled on very gently
    in the notch when done. The tube cannot be pinched.

9.  Once the heat exchanger is in place, put the interior cover/plate
    assembly on the pipe. It's a bit of a tight squeeze. The plastic is
    flexible and will expand, but you may need to "hook" one side on
    only slightly and then progressively push the edge over the pipe.
    The edge of the pipe should be chamfered alraedy. The edge of the
    indoor plate is chamfered.

10. Think about if you may have forgotten anything

11. If not, you can connect the 120 volts, by plugging in the wall wart,
    or turning the light switch on, for a hard wired scenario.

12. The follower does not do anything unless it gets a synch packet from
    the leader so it won't appear to do anything until the other of the
    pair is also installed and powered up. If it still doesn't seem to
    do anything, use the troubleshooting section.

13. The plan during beta phase is to pair beta units at the factory so
    you don't have to do any setup unless you want them to be accessible
    over your home wifi network. If you need them to be available on
    Wifi, see the initial setup section.

# Initial setup

The devices work out of the box, but if you want to use additional
features, you need to edit the configuration file using a program called
Thonny and a usb-micro cable. See below for details on how to do that.

## Using the TW4 without any external wifi network

For convenience or security etc. you may not want to connect the TW4 to
your home wifi network. In that case, the TW4 leader can start its own
access point. It is a typical wifi access point in most regards, other
devices can connect to it and talk to each other through the Pico.

When factory default TW4 leader is booted up, it starts an []{.mark}

[access point:]{.mark}

[(SSID): TW4_ap_leader]{.mark}

[Password: osrocks8882888 .]{.mark}

[The ip address of the device will be:192.168.4.1]{.mark}.

## Wifi config, to connect to your home network

The wifi password and SSID and ip address of the follower has to be
entered manually over USB using Thonny. You can verify it has connected
and has internet access when it boots up by watching the diagnostics
using Thonny.

It pings google.com upon first boot if it can connect to wifi so you can
see the internet connectivity is available, then io.adafruit.com and then it tries
to ping the leader and/or gateway at 192.168.4.1.

Make sure you check every single field is correct in the config file.

The defaults and explanations (field, default, explanation):

**\"Ssid_main_wifi\": \"use_ap\":**

This is the name of the wifi network you want to connect to. If it is
"use_ap", the device will make it's own access point, that is only for
use as a leader. The follower will not work as an access point right
now.

**\"Password_main_wifi\": \"none\",**

This is the password for the wifi, of course. There should be no need to
specify WPA2 etc., it is automatic.

**\"Ssid_ap\": \"TW4_ap_leader\",**

This is the name of the access point which the leader can create, I
recommend not changing it unless you have multiple leaders in range and
you want them to be access points, so they must have different names.

**\"Ap_password\" : \"osrocks8882888\",**

This is the wifi password when the device creates an access point.

**\"Ip_leader\" :\'192.168.4.1\',**

This field is not used currently, but in the future it may be wanted if
the follower is to contact the leader using some methods.

**\"Ip_follower\" :\'192.168.4.2\',**

The leader needs to know the IP address of the follower in order to send
it synch packets. Unfortunately not all ip addresses work with all
routers/access points. The default works with the access point the Pico
can create (on the leader). Most other access points work with
192.168.0.102 in my experience. A good access point would work with
whatever you set.

**\"leader_or_follower\" : \"leader\",**

You must change this field to set whether the device is a leader or
follower. Do not use capitals or anything. It must be exact. "leader" or
"follower". Nothing else will work.

## Mqtt config using adafruit.io

The device can use other MQTT servers and I have tested it with several.
Open the persistent_vars.json file and change the Sections to reflect
the URL, username, io key and so on that you want. Description of
fields:

**\"ADAFRUIT_IO_URL\" : \"io.adafruit.com\",**

This is the url of the mqtt server.

**\"ADAFRUIT_USERNAME\" : b\'\',**

This is the username for the mqtt server/account

**\"ADAFRUIT_IO_KEY\": b\'\',**

The mqtt servers use a so called api key, a unique code which can change
on demand, which is not the same as the password for the user account.
You need to login to adafruit and get it or otherwise get it out of the
server somehow. It's pretty long usually.

**\"ADAFRUIT_IO_FEEDNAME\" : b\'OpenERV_TW4-1\',**

This is the channel which the device gets power commands from. You can
control many devices from a single channel, or you can command different
pairs differently by using different channels. Remember the data
published to this channel must be an integer from 0 to 100 and nothing
else. No decimals right now are allowed.

**\"ADAFRUIT_IO_FEEDNAME_publish\" : b\'OpenERV_TW4-1_status\',**

This channel is useful to monitor the operation of the device. Right now
the millisecond clock time of the device is published at the start of every Ventilation Cycle (UDP Port 12345) to
this channel.

It is recommended to just using Adafuit IO if you are just getting started, in
that case you only need to modify the username and enter your IO key and
things should work fine. You can also login to their website and view
the feed, enter test data and so on, which will help you get things
working how you need to.

Remember that a feed does not exist just because someone subscribed to
it. You may need to create the feed through the web interface or
whatever. Or just publish a message to the channel and it should be
created automatically.

## Home Automation (Alexa, Matter, Google Home etc.)

The approach I've picked for this is just to use an MQTT adapter/bridge.
There are modules available for all the major home automation systems to
bridge to MQTT devices. The problem is they make it incredibly
convoluted to make the device a native Google Home or Alexa or whatever
compatible device. A firmware update that includes native functionality
for at least one of these, probably Matter, could be released but is not
likely/will not be soon. MQTT does everything it needs to do here and is
compatible with common protocols.

# Troubleshooting

Every device is tested before leaving the microfactory, however damage
could be sustained during shipping or installation, or errors/omissions
during beta stage especially.

The biggest potential for issues is with the networking setup, because
wifi routers etc. are frequently of sketchy quality and not compatible
in minor or non-obvious ways, and the error codes are nearly
useless/there is no error code, it just sits there doing nothing half
the time.

If you find that it apparently won't connect to your wifi network even
when the password and ssid is correct, see if you can ping the device
first, to see if local area network communication works even if the
internet connection does not. The Thonny/Putty interface will help, see
relevant section of this manual.

After it's working, try to backup the configuration file or whatever you
are going to change before changing things again, and name the file with
the time and date it was backed up, and put it where you can find it
later. **Definitely back the whole memory of the pico up before updating
the firmware.**

  -----------------------------------------------------------------------
  Symptoms                Explanation             Cure
  ----------------------- ----------------------- -----------------------
  The fans always run at  Probably the sensor     Take the cosmetic cover
  max power               tube has come unplugged open and check the
                          or pinched, or there is sensor tube and/or
                          a wiring error.         wiring using a VOMM and
                                                  by eye.

                                                  

  Cannot connect to wifi  Try connecting the      
                          micro usb port to a     
                          computer and then start 
                          up Thonny as described  
                          below and see what the  
                          diagnostics say.        

                                                  

                                                  
  -----------------------------------------------------------------------

*Table 3.*

## Connecting with Thonny or Putty

The device gives diagnostic information about what's going on constantly
over the serial port.

Putty is a common program that can view information coming in over the
USB port. There are many others, they are called serial terminal
programs

You can also connect to change the program and settings over usb using
Thonny. This is currently the only way to change the Wifi password and
some other things. A web configurator takes second priority to flow,
efficiency and noise.

Looking at the diagnostic info can be very helpful to diagnose errors,
damage, verify the internet connectivity is available, etc.

### Putty:

Simply install Putty or another serial terminal program on a laptop or
similar, connect the USB cable from the Pico to the computer, make sure
the device is powered on, then the hard part is determining which COM
port is being used. Go into device manager and see which com ports are
in existence and try the most promising ones first. The baud rate is
115200 baud. Open up Putty and connect to that com port and it should
show you whatever the Pico is saying.

You can also open the main.py in Thonny and press the green arrow icon
in the top left hand corner. This will run the main.py program, but
allow you to instantly see the output of the program in thonny's output
window. This way you can see the very beginning of the program, the
problem with using Putty is that it takes time to connect after first
booting and you might miss things you want to see.

![](media/image1.png){width="5.40625in" height="5.03125in"}

*Figure 5.*

Enter the "serial line" as shown, except it will probably not be a 53,
it will be another number. The speed is 115200, that has to be right.
Connection type is Serial.

This diagnostic information is read only, you can leave your computer
sitting there collecting a log of information if you want. You can
connect to multiple ERV units, I often connect to both of a pair so I
can verify they are working right before shipping them.

If it seems to connect fine but no text is appearing in the putty
window, it may just not be printing anything right now, there are some
stages of the program where that happens.

### Connecting with Thonny:

Install thonny, according to the tutorial below:

[[https://projects.raspberrypi.org/en/projects/get-started-pico-w]{.underline}](https://projects.raspberrypi.org/en/projects/get-started-pico-w)

You need a micro usb cable. Connect the cable to the usb port of the TW4
(the pico), with power off. Open Thonny. Connect the usb cable to the
computer, and then in the lower right corner of Thonny, click the box
that indicates which interpreter you are using.

It should show a raspberry pi pico W on COM4 or some other COM port.
Once the com port is selected, you have to unplug the usb cable, plug it
back in again, and then click the red button within 6 seconds after
power is applied.

If you take longer than 6 seconds the watchdog will be enabled, which
will reset the device after a few seconds after Thonny connects. Some
red text would appear in a few seconds saying the back end was
restarted.

The ip address of the follower has to be one that the wifi access point
is happy with. Unfortunately sometimes some ip addresses do not work
with low quality routers/access points. Usually 192.168.0.102 works and
if not try 192.168.4.2. For the access point running on the pico
192.168.4.102 works.

The mqtt power level command must be an integer from 0 to 100, no
floating point or extra characters etc is allowed.

Note that a feed in mqtt does not exist just because someone subscribed
to it, you have to publish to it or create it explicitly.

You can open the main.py in Thonny and press the green arrow icon in the
top left hand corner. This will run the main.py program, but allow you
to instantly see the output of the program in thonny's output window.
This way you can see the very beginning of the program, the problem with
using Putty is that it takes time to connect after first booting and you
might miss things you want to see.

## Updating the firmware

To update the firmware, you just connect through thonny and then you can
backup the old files off the device in Thonny by downloading them to
your computer (put them in a sensibly named folder where you can find it
later), deleting the old files, and uploading the new files, again using
Thonny. Basically just like if it was a thumb drive, except you have to
use Thonny.

There appears to be a minor bug right now in Thonny. It sometimes sits
there and fails to show the files on the pico. You click in the lower
right hand corner and tell it to switch to the other device, on the same
com port, which is also a pico. Switching the interpreter like that gets
it to show the files. This is a bug that only recently arose and
hopefully will be fixed soon.

There is no compiling or special adapters or connectors needed. It's
also good to backup the old firmware which you know used to work, and
you can load it back on again as easily.

You cannot brick the pico by putting the wrong firmware on etc. as far
as I know.

Note that there are two "firmwares" here. There is the .uf2 file, which
is explained at the raspberry pi introduction website linked to above,
and there is the main.py and other micropython modules, which contain
the code that is specific to the ERV. You can update the UF2 file just
as easily, if you ever have to do that but there are instructions at
raspberry pi pico site.

Basically you just hold down the white reset button on the pico while
you are plugging in the USB power/cable, it will appear as a usb drive,
you copy the uf2 file to the drive and it reboots and installs the new
firmware automatically. The ERV specific micropython stuff should
actually still be there after the new uf2 file is flashed, but I
wouldn't count on it.

## Replacement of parts

The printable parts have STL files that can be printed by anyone with a
typical 3d printer. You can order them from a service like JLC3dp. Get
them made of Modified PLA or PETG, not regular PLA, which tends to fall
apart spontaneously near bolt holes etc. due to some interesting
material science phenomena. If you need other parts, consult the BOM for
the specs of the parts, most of the parts can be substituted for another
with similar specs very easily.

The fans can be 2, 3 or 4 pin fans. If they are 4 pin fans you would
just connect the PWM pin directly to the pico, not to the mosfet boards.
Almost any 120 mm PC fan will work to some degree, but the ones the TW4
comes with are particularly good, high-flow, quiet, long lasting, and
waterproof.

I used screw terminal connectors so you do not need to do much or any
difficult soldering to replace components, nor are there any concerns
about having the right connector, but this introduces the possibility of
wiring errors. After beta I think I will use a PCB.

## BOM:

The bom has to be reviewed and updated as of dec 23 2024.

                                     item group                                                                                              item                                                                                                                                                   parts per module
  ---------------------------------- ------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------ ------------------
  **regen**                                                                                                                                                                                                                                                                                         
                                                                                                                                             slices (coated or not)                                                                                                                                 8
                                                                                                                                             tape, tuck tape is the best                                                                                                                            
                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                    
  **hard plastic printed parts:**                                                                                                                                                                                                                                                                   
                                                                                                                                             Indoor cover                                                                                                                                           1
                                                                                                                                             fiberglass grid                                                                                                                                        1
                                                                                                                                             potentiometer mount                                                                                                                                    1
                                                                                                                                             indoor plate                                                                                                                                           1
                                                                                                                                             noise splitter main body                                                                                                                               1
                                                                                                                                             inner pipe extension for splitter                                                                                                                      1
                                                                                                                                             Hat seat (printed splitter)                                                                                                                            
                                                                                                                                             Flow straightener                                                                                                                                      
                                                                                                                                             Fan retention clamp                                                                                                                                    
  **fan:**                                                                                                                                                                                                                                                                                          
                                                                                                                                             fans, corners trimmed                                                                                                                                  2
  **screws and nuts and washers:**                                                                                                                                                                                                                                                                  
                                                                                                                                             12 mm washers for m3 screws for fan retention                                                                                                          
                                                                                                                                             M4 55 mm long                                                                                                                                          
                                                                                                                                             lock nuts for the splitter clamp M4                                                                                                                    
                                     screws, 12 mm long 3 mm diameter, ss, self tapping                                                                                                                                                                                                             
                                                                                                                                             for inner and outer covers to plate                                                                                                                    8
                                                                                                                                             for fiberglass grid                                                                                                                                    8
                                                                                                                                             terminal block mounting                                                                                                                                1
                                                                                                                                             regulator mounting                                                                                                                                     2
                                                                                                                                             for pot mount                                                                                                                                          2
                                                                                                                                             for fan assembly                                                                                                                                       3
                                                                                                                                             total                                                                                                                                                  24
                                     screws, M3 self tapping 25 mm long, can be regular M3 with a nut in a pinch, instead of self tapping.                                                                                                                                                          
                                                                                                                                             for indoor and outdoor plates clamp                                                                                                                    2
                                     2 mm self tapping stainless steel screws                                                                                                                                                                                                                       
                                                                                                                                             2 mm self tapping, 12 mm long for pico                                                                                                                 
  **Electronics**                                                                                                                                                                                                                                                                                   
                                                                                                                                             pico w                                                                                                                                                 1
                                     wire for wiring on indoor plate                                                                                                                                                                                                                                1
                                                                                                                                             12v                                                                                                                                                    
                                                                                                                                             5v, 3.3v                                                                                                                                               
                                                                                                                                             ground                                                                                                                                                 
                                                                                                                                             ingress pwm                                                                                                                                            
                                                                                                                                             egress pwm                                                                                                                                             
                                                                                                                                             scl pressure sensor                                                                                                                                    
                                                                                                                                             sda pressure sesnor                                                                                                                                    
                                                                                                                                             3 wire 26 awg ribbon cable for fan (extension wire) 60 cm                                                                                              1
                                                                                                                                             3 wire 26 awg ribbon cable for fan (indoor plate) 15 cm                                                                                                1
                                                                                                                                             Adjuversioned \*\*make sure you set it to 5 volts before turning things on\*\*\* voltage regulator for servo and pico, capably of 1 amp for servo.        1
                                                                                                                                             12 v power supply 2amp                                                                                                                                 1
                                                                                                                                             2.54 mm screw terminal connectors 14-position for pico                                                                                                 4
                                                                                                                                             terminal block connectors, 2 circuit can use the non-screw types in a pinch, if you pull that hard on the cable it\'s probably not bad it comes out.   1
                                                                                                                                             fuse holder, fast blow glass tube type                                                                                                        1
                                                                                                                                             low side mosfet boards                                                                                                                                 2
                                                                                                                                             fuse, 2 amp, fast blow                                                                                                                                 1
                                                                                                                                             potentiometer and knob and retaining nut                                                                                                               1
                                                                                                                                             3 pin pluggable connectors for fan, 3.81mm pitch, m/f pair                                                                                             2
                                                                                                                                             pressure sensor sdp810-125a                                                                                                                            
                                                                                                                                             fiberglass for inner cover, can use up the stuff in the big box                                                                                        1
  **Other**                                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                                    
                                                                                                                                             Plastic film for window, BOPET is good, 50 micron                                                                                                      1

*Table 4.*
