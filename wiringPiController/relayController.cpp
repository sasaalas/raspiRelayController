#include <wiringPi.h>
#include <iostream>
#include <sstream>
#include <string>
#include <unistd.h>

int main (int argc, char* argv[])
{
    if (argc < 4) {
        std::cerr << "relayController: Usage: " << argv[0] << " <pin> <mode> <time in ms> for example 0 1 1000" << std::endl;
        return 1;
    }
        
    std::istringstream ss(argv[1]);
	int pin;
	if (!(ss >> pin)) {
		std::cerr << "relayController: Invalid pin id " << argv[1] << std::endl;
		return 1;
	}
	
	std::istringstream ss2(argv[2]);
	int mode;
	if (!(ss2 >> mode)) {
		std::cerr << "relayController: Invalid pin mode " << argv[2] << std::endl;
		return 1;
	}
	
	std::istringstream ss3(argv[3]);
	unsigned int upTime;
	if (!(ss3 >> upTime)) {
		std::cerr << "relayController: Invalid time format " << argv[3] << std::endl;
		return 1;
	}
	
  wiringPiSetup () ;
  pinMode (pin, OUTPUT);
  
  std::string modeString = "HIGH";
  if (mode == 0) {
	  modeString = "LOW";
	  std::cout << "relayController: Setting pin" << std::to_string(pin) << " to " << modeString << std::endl;
	  digitalWrite (pin, LOW);  
		
  }
  else {
      std::cout << "relayController: Setting pin" << std::to_string(pin) << " to " << modeString << std::endl;
	  digitalWrite (pin, HIGH);  
  }
	  
   if (upTime > 0) {
	      unsigned long sleepTime = upTime * 1000;
	       usleep(sleepTime);
	       
	       modeString = "HIGH";
	       if (mode == 1) {
		   modeString = "LOW";
		   digitalWrite (pin, LOW);  
	       }
	       else {
		   digitalWrite (pin, HIGH);  
	       }
	       
	       std::cout << "relayController: Setting pin" << std::to_string(pin) << " back to " << modeString << std::endl;	       
	  }
  
  return 0;
}
