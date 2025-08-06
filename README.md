# **CPR Compression Training Kit for UCSD's ECE SIPP Final Project**
**Problem Addressed**: According to a 2017 study from the American Heart Association Journals, only about 18% of adults have reported being trained in CPR. When looking at training kits, they often cost several hundred dollars and classes may vary in price. Overall, these price ranges may seem to be a reason that adults are discouraged to take these classes or purchase training kits, and that may lead to an unfortunate result when they encounter a situation where someone needs CPR. 

**Functionality**: The overall purpose of this project is to make an affordable CPR kit that anyone can gain access to, and they can practice these CPR exercises in the comfort of their own home. The OLED display will demonstrate a brief countdown that gives the user time to prepare, and the buzzer will beep at 100BPM, which is the recommended rate for people beginning their CPR training. After an interval of 30 compressions, the buzzer will stop, the OLED display will indicate that the exercise is complete, and the user is able to rest for 7 seconds before pressing the button and starting the next 30-compression interval. This 7-second pause will give enough time for the user to practice giving 2 breaths to the patient. To ensure that the user is applying the correct amount of pressure, the LED lights will indicate when the user applies the correct amount of pressure, or when they apply too much or not enough pressure.  

*Note*: Different designs have been implemented where three LEDs + a blank display throughout compression exercise is used or a single RGB LED + show force values in OLED display is used. The overarching goal in both approaches is to make this project user-friendly and minimalistic to avoid unessential complexity.  

Materials Used:
* GME12864 OLED display
* Active buzzer
* 4-pin push button
* Round force sensitive resistor (FSR)
* RGB LED and single-color LED lights
* 330 ohm resistors
* 10k ohm resistor

## Design 1: 3 LEDs + Blank Display During Operation
<img width="3000" height="1761" alt="Image" src="https://github.com/user-attachments/assets/1650a8b8-5edb-4b25-9f7a-2bff4773d626" />

## Design 2: RGB LED + Force Value Display During Operation
<img width="3000" height="1761" alt="Image" src="https://github.com/user-attachments/assets/71c41860-17ba-4979-a3d6-e1e35e9c05dd" />
