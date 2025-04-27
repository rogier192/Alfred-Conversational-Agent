To run Alfred:
Powering Alfred can be done in 2 different ways;
-	Connecting the Raspberry Pi to power first and afterwards powering the rest of the circuit. Powering the circuit first causes the raspberry pi to fail to boot.
-	Connecting the ground and 5v/ground wires (purple and black) to the existing power circuit, allowing the raspberry pi to power the robot or the robot to power the raspberry pi (this will fail in high power use situations).

To control Alfred you can connect directly with a mouse and or keyboard with the USB ports or you can log in through SSH. To do so you must set up a Hot Spot with the name ALFRED and the password alfredalfred. You then ssh into Alfred with alfred@<IP adress> and use the password WeLoveAlfred.
To find the ip adress, connect to the hot spot with a laptop and use ipconfig or a similar tool to find the host ip. Alfred's IP (and thus your target) will be the IP of the host with the last 3 numbers replaced with 212. An example is: ssh alfred@10.147.182.212
If you wish to transfer files you can also do so through ssh, though a tool like WinSCP may help by giving you a graphical interface (must also be on the same network as Alfred).

To start a conversation use _systemctl --user start alfred_ or _systemctl --user enable alfred_ to make Alfred run on boot.
Just say the wake word "Hey Alfred" when you see the eyes and you will connect to Elevenlabs for your conversation. To end it you can tell Alfred to please end the call and he will do say, some insistence may be necessary.

How to Connect and Operate Alfred
1.	Create a mobile hotspot with the name ALFRED and password alfredalfred.
2.	Connect to the Raspberry Pi via SSH using:
ssh alfred@<ip-address>
Then enter the password: WeLoveAlfred.
3.	Navigate to the alfred/alfredproject and alfred/alfredProject/alfredTalk directory on the Pi. Here you will find several files
