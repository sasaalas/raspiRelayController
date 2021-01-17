CXX = g++
CPPFLAGS =        # put pre-processor settings (-I, -D, etc) here
CXXFLAGS = -Wall  # put compiler settings here
LDFLAGS = -lwiringPi # put linker settings here

relayController: relayController.o
	$(CXX) -o $@ $(CXXFLAGS) $(LDFLAGS) relayController.o

.cpp.o:
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $<

clean:
	$(RM) *.o *.d relayController
