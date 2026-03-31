# Introduction:

The WM12 is consists of two TW4 energy recovery ventilator (ERV)
modules, with a few electronic parts missing to reduce the cost, and a
foam adapter.

The TW4 energy recovery ventilator is meant to be a unit that is
embedded in a wall, to provide long term highly effective energy
recovery ventilation i.e. capture the heat and water vapor contained in
outgoing ventilation air, and transfer it to incoming ventilation air.

In the WM12, the foam, timber and hardware takes the place of the wall.

The TW4 modules are carefully designed to do this with high efficiency
and far lower low noise than anything else that does anything similar.

They include highly sensitive and accurate pressure sensors to regulate
the air pressure across the heat exchanger, thus regulating airflow into
and out of the house despite the chimney effect, wind, etc.

It's important to note that the unit is still in beta, and the modules
can be flexibly configured in many ways. This may appear to complicate
things but allows people to get what they need for longer term.

The machine is fundamentally capable of working to either prevent heat
and water vapor intrusion during periods of air conditioning, or prevent
the escape of heat during periods of heating, but the focus at first is
on cold climates, because parts that can stand high temperatures
encountered in hot climates are more expensive to make. The polymer
currently used for some of the additively manufactured parts starts to
get soft at 55 degrees C.

The WM12 can be controlled over WiFi using MQTT but it requires some
setup.

You can find the manual for the TW4 ERV here, where the WiFi related
features etc are discussed:
https://docs.google.com/document/d/1owr_riiIEUlUa45al_b7uIGe7IZfdDO1xxAAJC9aKUU/edit?usp=sharing

## General points to be aware of:

- **The silica gel coated heat exchangers may appear to have a smell
  upon first use** \*this is because they adsorb harmless chemicals from
  the packaging etc.\*. These chemicals are no more harmful than they
  are otherwise, but you can smell them primarily because they are added
  to otherwise fresh air, the smell is not covered up by other smells.
  There can only be so many milligrams of stuff adsorbed by the silica
  gel, and eventually it must all come out, or stay stuck in there. The
  smell should dissipate after a few days of operation, giving you
  clean outdoor air from then on. The material used in
  manufacture is non-toxic bio-source PLA, silica gel and isopropyl
  alcohol. There are no toxic substances used.

- Don't pull on the wires significantly, they don't have any strain
  relief, except the power wires.

- Remember Energy Recovery Ventilation is a long term value proposition.
  Although this machine has a remarkably fast payoff period as energy
  investments, or any investment, goes (less than 2 years on some
  contexts), it is meant to last a very long time. Be careful with it,
  position it in a place you are comfortable with the noise it produces,
  and ideally on a side of the house with minimal outdoor noise and
  wind. The components can be re-used to build a pair of TW4s for
  permanent installation in a dwelling for very long term, or re-sold
  while retaining their value. Additively manufactured/3d printed parts
  are not cheap or temporary, they can last a very long time and are
  relatively costly to produce.

<!-- -->

- The unit is capable of high airflow, 60 cfm is enough fresh air for a
  whole house by some measures. Most ERV units that advertise higher
  airflows will be revealed to not give anywhere near that in real world
  conditions if you actually check the manual/test data. A \$3000 large
  centralized unit in the basement of a house is only made to do about
  60 CFM during very cold weather, and it doesn't get very good
  efficiency, either, under such conditions.

- The system is quieter by far at any given airflow than similar
  push-pull units and centralized units, or any other ERV. It's also
  directly in the living space, however.

- **It may seem that the air exiting the unit is cold, if you put your
  hand in the air stream. However,** remember that any air colder than
  the surface of your hand will feel colder still if it is moving than
  if it is not. For comparison, try turning on a fan in a room, and you
  see the air exiting the fan feels colder. It is not, of course, any
  colder. Its temperature did not go down as it passed through the fan.
  We judge how cold things feel by the temperature of our hand, and how
  fast it changes. The faster the air is moving, the faster it extracts
  heat from our hand, and the lower the equilibrium temperature of our
  hand would be, should we leave it in the air stream long enough.

- If you wish to test/check the efficiency of the unit, a method using a
  low cost infrared thermometer is described elsewhere in this manual.

- The system takes a while to adjust the power level after the knob is
  adjusted. You will hear it adjusting but it takes a minute or two to
  adapt to large changes.

- Do not drop the unit, the printed parts are not strong enough to stand
  such forces. They can of course be replaced, all parts of the system
  can be replaced, but the labor and cost is significant. The machine is
  an investment. Treat it like a desktop PC when you are moving it, etc.
  Pick it up carefully with both hands, plan where you are going to put
  it ahead of time, unplug all cables before moving it, etc.

- The wind compensation similarly takes 30 seconds or more to fully
  respond, thus it is not effective in random gusty weather to block
  gusts, except to compensate for the average pressure.

- The beta units are made of MPLA. It is only good to 55 degrees C. The
  parts are not made for very hot ambient temperatures combined with
  direct sunlight. That will be addressed after proving everything in
  cold climates where such conditions are never encountered.

## Options to be aware of:

- Silica gel coating of heat exchangers. If it has a matte texture, it's
  coated with silica gel, which serves to absorb water vapor from
  outgoing air and transfer it to incoming air. This represents heat
  energy in some ways, because if there is lower humidity in incoming
  air, it accelerates the evaporation of water in the dwelling, and when
  water evaporates it absorbs a great deal of heat. The silica gel is
  the same material used in food packaging, it is non toxic and
  completely harmless. Very small amounts might come off on your hands,
  it is as harmless as sand.

<!-- -->

- The outdoor plate and hood unit allows the adaption of filters and the
  storm valve attachment, however recent changes with the sound splitter
  on the outdoor side have messed things up and I have not yet figured
  out how to use them in combination with the sound splitter in a window
  mount context/WM12. The old version with the plate and hoods and the
  fans inside the pipe is still an option if anyone needs the filter or
  storm valve modules while also mounting everything in a window.

  of components that are possible, especially with the wireless features
  of the TW4, you can put the two halves in different windows in
  different rooms etc, but I have not experimented much with this.

- The WM12 can be rotated and mounted sideways if the window is a shape
  that requires this, a window restrictor clamp should be used if this
  is done, to ensure it cannot fall out of the window.

## 

## Things during beta to be aware of:

- The initial units are made for cold climates primarily, extreme heat
  encountered in a desert could damage some components.

- Extreme heat has to be avoided during shipping, too.

<!-- -->

- The firmware is the exact same as the Leader of a pair of TW4 units.
  It has an auxiliary output for the second set of fans in the WM12,
  which is still active but not connected in a TW4 leader. In a WM12,
  only one side has a pressure sensor.

- I don't know for sure what will happen during extremely cold weather,
  like minus 30 C. Probably things will be fine, especially with the
  silica coated heat exchangers. It is very difficult to test.
  Simulations and calculations indicate some safety margin. However it
  is possible frost could accumulate on the heat exchanger or fan. This
  could cause temporary issues. The solution is to allow hot air from
  the house to exit the unit, melt the frost and evaporate the water,
  then start again. There are no provisions in the firmware for this
  right now. If the fans become stuck, you would have to take it out of
  the window, let it melt and dry and then put it back. The fans are
  waterproof. Future firmware updates may include functionality to
  detect cloggage with the pressure sensor and execute a defrost
  routine.

- The pressure detected by the pressure sensor is actually the pressure
  divided by about 4. This is because the pressure drops as the air
  flows through the narrow silicone tube, the sensor is not actually
  sealed and some air flows through it, however it still works very
  well. The pressure is divided in a repeatable and precise way, like a
  resistive divider dividing voltage, basically. Do not constrict the
  tube, or that would change things.

# Post-shipping assembly:

Consult the images to get an idea of how it goes together. Then, I
recommend the following approximate procedure, there are likely to be
details specific to your situation.

## Tools probably required:

- Ball end hex drivers, 2.5 mm and 3 mm, for the bolts and screws.

- Saw for wood

- You may or may not need a flat end screw driver, some of the clamps
  use hand-tightenable type mechanisms, some the screw head type.

- Some books or something else to prop it up on a table

- A table to work on for post shipping assembly.

- Box cutter with brand new/sharp blade to cut the foam.

- Sharpie to mark the foam and timber before cutting.

- Transparent or regular tuck tape (to attach the optional extra green
  pipe segments on the outdoor side) (some may be included, wrapped
  around the pipe segments).

## Part names:

### Heat exchangers:

![](media/image6.jpg){width="4.276042213473316in"
height="3.796357174103237in"}

### Noise splitter:

![](media/image9.jpg){width="3.4531255468066493in"
height="3.790764435695538in"}

### Mylar hat:

![](media/image8.jpg){width="3.213542213473316in"
height="3.5456911636045496in"}

### Noise splitter pipe extensions:

These extend the central pipe, reducing noise, they are not integral
because it gets too big to print, for now.

![](media/image11.jpg){width="3.651042213473316in"
height="2.3742530621172353in"}

### Wire extensions:

![](media/image7.jpg){width="2.9427088801399823in"
height="3.2132075678040244in"}

### Main pipe:

### Extra green pipe segment(s) for noise splitter (optional, reduces noise that comes in through the black foam by redirecting it downwards):

![](media/image2.jpg){width="6.5in" height="4.3529647856517935in"}

### Indoor cover and plate assembly, with pressure sensor:

![](media/image3.jpg){width="6.5in" height="3.8506944444444446in"}

### Indoor Plate and cover assembly with only 2 mosfet switches

Similar in appearance to the other cover/plate assembly.

### Black foam adapter

### Timber with hose clamps

This secures the pipes, acts as a handle and retains everything in the
window securely.

## Assembly procedure:

- Have a look at your window hold one of the main pipes in position,
  and, optionally, put the noise splitter on the pipe and have a look at
  how things are going to fit in the window. The timber should go across
  the window opening and then some, to make it practically impossible
  for the machine to fall out the window.

- Attach the clamps to the timber, and insert the pipes into the hose
  clamps, loosely. Have a look at how things are likely to fit in the
  window. Is there room for everything?

- Add the foam by pushing it onto the pipes

- ![](media/image5.jpg){width="6.447916666666667in"
  height="4.566615266841644in"}

- Make sure the ends of the pipes are more or less flush with each
  other.

- See if it fits in the window ok, decide how to trim the pipes and
  timber. Mark with a marker or pen or pencil where to cut. See if you
  have room to add the little green pipe segments on the outdoor side.
  You can put the noise splitter on temporarily to check for fit.

- Trim the timber and the foam with a sharp box cutter for the foam and
  a saw for the timber. I used an oscillating saw so I don't have to
  take the timber off in order to brace it while cutting. You may need
  to remove the pipes from the clamps and brace the timber to cut it
  safely.

- Attach the extension wires to the connector coming out of the noise
  splitter.

- Attach the noise splitters. Get them in position and tighten the
  clamps on them.

- Put the hats on the top.![](media/image1.jpg){width="6.40625in"
  height="5.143646106736658in"}

- Place the left indoor cover (the one with the silicone tube) and plate
  assembly **near** the indoor end of the pipe. Attach the cable
  connector Then with the notch at the top (12 o\'clock position), put
  the silicone tube and the wire in the notch, and slide the heat
  exchanger into the pipe. This part is a bit tricky. You have to place
  the wire and silicone tube side by side in the notch of the heat
  exchanger, with the heat exchanger nearly in the pipe, with the tube
  and wires not overlapping each other. The tube and wires should not
  pinch or bind! Things should pretty much slide freely. If the tube
  gets squished, things will not work quite right.

  - Do not pull much on the silicone tube or you may pull it out of the
    sensor and have to open the cover and put it back in the sensor. I
    tape them or glue them on to the sensor to help with this but
    nothing sticks very well to the silicone. It's a hassle to get the
    cover back on after because of the wires.

  - Notice that the heat exchanger kind of slides around freely. This is
    not quite ideal but I haven't solved it yet. **\*when you pick up
    the machine, it can slide around\*.** **So keep the machine level
    when you pick it up, more or less. Remember it's supposed to be
    installed in a wall, not moved around like this.**

- Then rotate the heat exchanger 90 degrees, ideally, to prevent any
  stress or pulling on the tube. There has to be enough extra wire on
  both ends of the heat exchanger so things don't bind or get pulled on.

- ![](media/image4.jpg){width="6.5in" height="4.875in"}

- Repeat the procedure for the left side, but you can slide the heat
  exchanger in first, and then plug the wires in, because there is no
  silicone tube to deal with.

- Now would be when you add the pipe extensions to the noise splitter,
  they help improve noise rejection but are optional. It makes things
  kind of awkward to put n the table. \*Again be aware the heat
  exchangers can slide around inside the pipe if the machine is tilted\*

- Connect the two plates together, there is a 4 pin connector that is
  used, behind the plates.

- Ensure the clamps are tight enough, there are 6 clamps, one on each
  noise splitter and one on each indoor plate, and the hose clamps
  around the pipes. The ones on the indoor plate I rarely tighten and
  they require a ball end hex driver to reach in there anyway.

- It is a good idea to power it up while it's on the table, just to
  verify things seem to be working,

  - Do not work on it while it's in the window, it's tempting but you
    may push it out of the window or something. If you accidentally pull
    it inside the window you can knock the noise splitters off if they
    aren't on properly, or break them even.

  - The table blocks the airflow unfortunately during assembly. If you
    can, lift up the back while it's running and verify the airflow
    seems to be going the right way. Watch the behavior of the hats,
    that tells you if they are under negative or positive pressure.
    Don't get your finger in the fan! I put a two by four underneath the
    rear and front in order to prop it up for testing. It's a bit
    precarious like that.

- If the mylar hats have a dent in them, adjust the seating. If they
  collapse in that area while under negative pressure and make a noise
  in the process and you cannot solve it by adjusting the seating,, you
  can just add some gorilla clear tape to that area to prevent it from
  making noise when they collapse, this is a workaround for now. The
  thinner the mylar the better the anti noise performance so it is
  pretty close to the limit. The slight dent formation is otherwise
  safe.

# Handling/window installation

## Moving the machine:

1.  Don't leave the power supply connected, disconnect it every time you
    move the machine, to simplify things.

2.  If the wooden window timber retainer is assembled correctly, it can
    be used as a handle to pick up and move the machine. Ensure the
    clamps are reasonably tight before picking it up.

3.  If the machine is tilted during motion or knocked around, the heat
    exchangers may slide around. Try to keep it more or less level to
    avoid this.

Plan each move, make sure there is nothing to trip over etc.

If anything doesn't fit or is awkward, patiently back off, put things
back, correct it and try again.

Make sure everything is properly in place and connected/tightened and so
on so nothing is going to fall off and plummet downwards, on the outdoor
side especially.

Adjust the position of the wooden window retainer before putting it in
the window. Don't loosen the hose clamps while it's in the window to
adjust the position, tempting as it may be, you may end up dropping
something out the window.

Do not pull the pipes/unit inwards while the unit is in the window, if
the outdoor components are not attached firmly they could be pushed off
by the window sill and plummet downwards.

## Normal installation in a window

You first should assemble the unit on a table, and test it to verify
there are no wiring errors etc, as it's much easier to correct things at
this stage.

Ensure that the noise splitter is fully secure on the pipe, attempt to
rotate them relative to the pipe to ensure they are secure. The bolt
does not need to be very tight to ensure a great deal of friction. Do
not overtighten the bolt or it will break the clamp.

Ensure the indoor cover(s) is/are reasonably secure, and also it's very
important the hose clamps are secure around the pipes.

Check things can fit in the window. This is not so easy, you may need to
use a measuring tape, and if you can, open the window wide and lift up
the unit (after full assembly is completed) and see if it mostly fits.
Sometimes the noise splitters hit the window sill. If this occurs, a 2
by 2 can be put on the lower part of the window to raise the assembly
but it is a hassle to seal everything.

You can change things in some ways, such as by rotating the noise
splitters so that things fit.

Don't worry if you crumple the mylar hats a bit, it appears to be
harmless.

After you have a sound plan, you can trim the extra included black
polypropylene foam, tape it to the other foam, and move it into
position, close the window, and put the window restrictor clamp in
place.

I usually close the window around the pipes themselves, with the foam
overlapping on the interior side, as I have found it easier to seal like
this.

It appears to be a good idea in some cases to tape the timber to the
foam, as it makes it easier to seal all gaps later around the window,
when this is done. It's hard to get tape in there when it's installed in
a window.

You can lift the unit safely by grabbing the timber, when the hose
clamps are secure, the only remaining problem is the heat exchangers can
slide around if they are not a tight fit. Making them a tight fit makes
things harder sometimes so the best thing is to keep the unit level at
all times and make sure the interior covers are secure against the pipes
so if they do slide around it doesn't knock the covers off and tumble
out.

The next unit I ship will have a different timber, shorter, with metal
pieces ("mending plates") extending off the end, to make shipping
cheaper, as the long timber was expensive to ship. You will measure your
window and screw the metal pieces in place such that the total length of
the metal pieces and the timber is slightly longer than your window is
wide. Thus it is practically impossible for the unit to fall out the
window in landscape mode.

If you need it to be longer because you have a very wide window, you may
need to purchase a timber locally from the hardware store and cut it,
then attach it with a screwdriver (robertson, #2 I think, the green
one), depending how secure you want it to be.

I recommend taping the edges of the foam and window shut with gorilla
clear tape or similar. Otherwise strong winds can blow significant
amounts of air through even small cracks. You don\'t generally want to
remove it very often. It doesn't look great but I see no other way to
really seal things easily.

Access to the outdoor side is useful for various reasons, to inspect
etc. It can be an awkward fit due to the sill on some windows, usually
the outdoor sill, but I have been able to shimmy it into every window I
have tried thus far.

- There should be a small metal clamp like object included in the
  package. This is the window restrictor. You clamp it to the window in
  some area to prevent the window from opening too widely, which could
  allow the machine to fall out. Strategize for when and how to add this
  before putting the unit in the window.

Just like a window air conditioner you should be very careful:

- Be extremely careful not to allow the machine to fall out the window.
  The timber across the top plus the mending plates is supposed to be
  long enough that it is quite hard for it to accidentally go out the
  window.

- You may find that the exterior part hits the outside window sill/the
  exterior wall. If this happens you may need to remove the extra little
  green pipes or not add them, or you can raise the unit up by putting a
  timber below it, in the window. Most people don't add them although
  the 45 dBa at max power is with them, not without them. The unit can
  rest on the exterior window sill and the foam still seals and
  everything works fine, in my experience.

- Do not try to move the unit with the power attached, it gets awkward
  and looks like it would considerably increase the possibility of
  accident. Also you could break something if you pull too hard on the
  power cable. Unplug the power supply and otherwise simplify things as
  much as you can before moving the device.

- You can use the timber across the top as a handle to move it around.
  Again, try no to tilt it because the heat exchangers can sometimes
  currently slide around relatively easily, I have no good solution to
  this yet.

- Remember when you turn it on that 60 cfm is a lot of air as ERVs go,
  it's as much as some full sized centralized units get during cold
  weather. If it seems a bit loud on max, that's because it's a lot of
  air and power, not because the machine is inherently noisy. It has an
  excellent noise to flow/efficiency relationship, however it also has a
  relatively high maximal power capability.

## Sideways installation

It is possible and practical to install the machine sideways. Below are
some candid photos of an actual installation.

![](media/image12.jpg){width="5.0in" height="6.666666666666667in"}

In this photo, the interior cover is oriented in a way such that the air
would come out the side and get re-inhaled by the other heat exchanger.
I recommended putting some tape over the outlet on that area.

![](media/image10.jpg){width="5.0in" height="6.666666666666667in"}

The noise splitters are rotated to get them to fit despite the window
sill. Theoretically longer pipes could also work, or a timber as a
spacer.

![](media/image13.jpg){width="5.0in" height="6.666666666666667in"}

# Repair and maintenance:

## Overview

The system is made to be maintained over the very long term, thus giving
good return on investment. The wiring is the hardest part, the schematic
is pretty simple as such things go but it is easy to put a wire in the
wrong place, **or allow a stray strand of the multi core wire to touch
the wrong place (this is a common issue so watch for it. Always twist
the multiple strands around each other before inserting in a connector
to avoid this)**.

The electronics are all standard and basic, except the pressure sensor.
The connectors are relatively user friendly. In the event of power
surges, angry exes, etc. any damaged component can be replaced, even if
the original company is gone. 50% of home improvement companies are out
of business within 5 years, so warranties are not enough.

## Fan replacement and/or bearing replacement:

Any 120 mm fan can be used, 2, 3 or 4 pin, you just need to cut the
corners off. The main issue is getting a fan that is quiet, and water
resistant, and ideally ball bearing, and high pressure. If you cannot
get waterproof fans, silicone waterproofing grease (such as marine
dielectric grease, which is used on ships to waterproof electronics) can
be painted with a brush onto the electronics of almost any ball bearing
120 mm fan. These fans can be dismantled just by removing the sticker on
the back and removing the circlip (small torx screwdrivers work to
remove the circlip). There are waterproofing sprays for electronics that
could be simply sprayed in there, but they are not common and I have
tried only one with limited success. Silicone oil is basically what
you'd want. Mineral oil would probably work fine too.\
\
The printable components can be printed by any cloud printing company,
or ideally a real person who just has a printer in the local area, which
tends to be a lot cheaper (makexyz.com is one option).

The included fans can have their bearings replaced, and the bearings
should last 7-12 years. The bearings cost only about 20 cents each and
are widely available, standard bearings.

### Bearing replacement instructions:

**Bearing size:** OD: 8 mm. ID: 3 mm. Thickness: 4 mm.(3x8x4 bearing).
If you search 3x8x4 bearing you will see a lot of people selling them in
small quantities. The ABEC rating and noise level doesn't really matter
much, in any case small time sellers usually claim more than is true,
unless you are actually buying from mcmaster-carr or directly from a
supplier.

**The circlips:** Are 3 mm outer diameter circlips. You may not need to
buy one, you can usually re use the old one, but if you lose it or break
it you can get replacements easily, get the kind with the little hooks
or complete holes on the end, ideally. Alloy is fine, stainless is
overkill.

You need to dismantle the system to get the fan on a table in front of
you, then remove the sticker covering the bearings, remove the circlip,
and the fan blades/magnet assembly just falls right out. The bearings
just fall out, you put the new bearings in and then put the circlip back
on.

To remove the circlip is the hard part. Circlip pliers of the right size
are hard to get and expensive, however I have found a good technique
using two very small torx screw drivers. You need 1-0.8 mm or smaller
torx heads. Place the two screw drivers together and push down while
levering them against each other (the handles of the screwdrivers make a
usable fulcrum point, you can tape them together to make it a little
easier) to cause the tips to spread apart. The bearing has a spring
behind it, when the circlip is released the bearing will pop up. *The
circlip may also sproing away and be lost, so be ready.*

Putting the circlip back on is a bit difficult. You can finagle it back
on with the screw driver, I've found that to be workable, but an even
easier way is to drill a 3 mm hole in the end of a 7 mm diameter hot
melt glue gun refill. It's basically a soft polymer rod. The hole
squeezes over the shaft, but the edge of the hole pushes the circlip
down nicely, until you feel it click into place. You only have to do
this every 7-12 years!

Electrical schematic:

The colors in the schematic should be the actual wire colors. Beware red
is used for both 5v and 3.3 volts. !2 volts is Yellow. Black and brown
are ground. Orange is for the ingress fan, green is for the egress fan,
both the signal to the mosfet board and the ground side of the fans.
Orange and green is also used for the pressure sensor data and clock
signals, which is which is in the schematic.

The part descriptions for electrical parts are in the BOM.

There is a PDF in the source code repository with the schematic, it is
not copied here because it's too laborious/unreliable to make sure the
various copies are always up to date if there is a change or bug
correction. You have one copy in one place and then refer to it as
needed. When things are out of beta it will be copied here.

## STL files for replacement printable parts:

See source code repository. It's a google drive linked to on the
website, and will be put in the internet archive for long term if
possible.

### 

### Note on printing the regenerator/heat exchanger:

The latest and greatest heat exchanger is produced directly with python
script generated gcode specific to the printer I use and cannot be
practically produced diy, unfortunately. However the old model can be,
and the STL is included for that, in the source repository. To do this,
simply use Cura, load th STL in, put it in the center of the build
plate, and set it to do "lines" infill with about 2.5 mm on center
(between centers of the lines) spacing and 0.45 mm width, no top layer
and no bottom layer (set them to zero). Check the preview and it should
show you a structure which is much like grid infill, parallel channels
which are square in cross section, with the outer wall. Tape can be
applied over the nubs on the side to fit in an oversized pipe, or they
can be sanded if the pipe is too small. You could also use grid infill,
but the roads tend to have problems where they intersect. When the
nozzle goes over one road, it wipes the plastic off, and not enough is
deposited on the lee side. I don't know how to solve this in Cura
without using lines infill. If you could make it so the nozzle went in
alternate directions each layer that would probably solve it well
enough.

## Replacement part numbers/sourcing:

The connectors are called pluggable screw terminal connectors, 3.81 mm
pitch.

The screws are stainless steel self tapping screws hex socket stainless
steel 304.

The part number of the fans is 11925SE-12R-FT-DW . They are available
from digikey and other electronic parts overnight supply houses.

The plastic sheet for the hats is 50 micron generic BOPET, biaxially
oriented polyethylene terepthalate, (generic mylar, mylar is a brand)
but 75 micron (3 mil) might be a better bet, some 50 micron is crinkly
and makes noise.

The adhesive is E6000, waterproof elastomeric adhesive.

The wire is silicone multi stranded wire, 24 gauge is fine for repair
stuff.

The pipe is SDR35 PVC pipe, SDR28 will NOT fit SDR35 ABS is \*not\* the
same size.

The thin transparent tape is gorilla clear.

# Efficiency:

Testing is ongoing, initial testing results indicate 87% sensible heat
recovery efficiency at 60 cfm and 75% latent heat recovery. Efficiency
is even higher at lower flows, exceeding 90 percent at 30 cfm.

## Ventilation efficiency/short circuiting:

There is a measure in the HVAC industry/building design called
ventilation efficiency. It's basically the ratio of the indoor air
quality vs the ventilation rate, or the indoor air pollution vs
ventilation rate, assuming a constant release of pollutants in the
building. There are many clever ways such as displacement flow
ventilation, to improve this above the basic so called dilution flow
approach, which is the normal approach commonly used, where a jet of air
just swirls around in a room and mixes thoroughly, and air is removed
practically randomly from the room. One thing that puts a dent in
ventilation efficiency is so called short circuits, which is a bit of a
misnomer, but it it implies fresh air transiting rapidly to the
exit/exhaust, without doing anybody any good.

Obviously the WM12 has the intake and the exhaust right next to each
other, but they are pointed in opposite directions. I have used smoke to
viualize airflow and posted a video of this on youtube. There is no
re-inhalation of air near the unit. The exiting air jets away and mixes
into the room effectively.

The only case where there is a significant although minor concern is
when the unit sticks over a window ledge, in that case some air at the
bottom near the ledge tends to swirl back in. To solve this, a piece of
paper or cardboard can be used to guide the airflow.

# Savings/investment calculations:

See spreadsheet
[[here]{.underline}](https://docs.google.com/spreadsheets/d/116Zo_kcxLSTzkiw5lbofJJ0vPNLvXxe8Esu2196i8oA/edit?usp=sharing),
it is also linked to on the website, to determine the actual return on
investment that applies to you, in your area, with your energy prices.
The machine is an investment, its value arises from long term operation.

# Specifications:

  -----------------------------------------------------------------------
  Spec                                Value
  ----------------------------------- -----------------------------------
  Max actual net fresh air flow       60 CFM

  Power supply voltage                12 Volts

  Power supply current requirement    1.5 Amps max (during fan
                                      acceleration)

  Expected actual average             87%
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
  of unit, at 15 CFM                  

  Noise emission at 1 meter in front  35 dBa
  of unit, at 30 CFM                  

  Noise emission at 1 meter in front  45 dBa
  of unit, at 60 CFM, with optional   
  extra pipe segments                 

  Wind resistance rating (from        S1 (less than 6 CFM at 20 pascals
  in-house measurements, not yet      wind pressure, total excess flow in
  certified)                          or out). It's actually better than
                                      this.

  Average power consumption at 60 CFM 9 Watts

  Average power consumption at 30 CFM 5 Watts

  Design life                         Parts can be replaced indefinitely.

  Fan bearing life span, expected     7-12 years elapsed time during
                                      normal use

  CE mark certification               Not yet.

  Underwriter's laboratory            Not yet, the power supply is UL
  certification                       listed, though.
  -----------------------------------------------------------------------

Rohs compliant.

Contains no toxic or hazardous materials.

Made in freedom.
