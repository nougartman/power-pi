# Power Pi
**Home power consumption monitoring using a Raspberry Pi**

This fork of the Power Pi project add the ability to calculate flat rate electricity cost based on data collected by your LDR sensors. This can not be used to calculate tariffs that operate on a variable rate such as peak and off peak tariffs. 

Aditionally the DhtWebHist folder contains the appDhtWebHist.py file that will initiate a Flask webserver displaying the latest sensor readings, aproximate total cost for each electricity meter (e.g. my own home has one meter for the aircons and hot water that is tariffed at a slightly lower rate than general power). It will also display the historical data in a scalable graph using highcharts.

Due to the initial values of the sqlite table columns being null, you will need to either run the PowerPi-run first.py file or add a small value to the sensor_1_rate_cost and sensor_2_rate_cost columns in the database to ensure that the PowerPi.py script does not encounter an error due to the total_cost column trying to calculate a null value.

## Hardware Sensors
Our electrical power board has a red LED that pulses each time 1Wh of energy is consumed.   The LED will flash fast or slow, depending on the load being drawn from the network. 


### Raspberry Pi with an analogue sensor
We can use a _light dependant resistor_ (also known as an _LDR_ or _photoresistor_) to sense the pulse of light from our power meter without directly connecting to any of the mains powered circuits.  We can therefore count every 1000 pulses the meter is equivilent to measure each kWh used.  

 Unlike the Arduino, the Raspberry Pi's GPIO pins are unable to measure resistance and can only sense if the voltage supplied to them is above a certain voltage (approximately 2 volts). The circuit at [Raspberry Pi LDR GPIO circuit](http://www.instructables.com/id/Raspberry-Pi-GPIO-Circuits-Using-an-LDR-Analogue-S/) shows a very simple circuit using only an _LDR_ and 1uF capacitor.


