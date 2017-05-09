# SIMPLE PRECISE PAN-TILT CONTROLLER FOR PTU-46-17.5
## App download
        PTC_0.9.2.zip 
## Requirement libary
    -Python 2.7
    -Pyserial
-Kivy(GUI)
## PTC-command
Read the instruction manual and put the command in command line
### Basic command 
	 Reset
	 r
	 Pan Limit Max
	 pnu 1000
	 Pan limit Min
	 pxu -1500
	 Move Pan 0
	 pp0 
	 Move Tilt 0 
	 tp0
## Run the program 
	python pantiltcontroller.py
	python PTC-command.py
### Old Version PTC_0.8.1
	python old\PTC.py
	
