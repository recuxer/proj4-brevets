# Project 4:  Brevet time calculator with Ajax

Reimplement the RUSA ACP controle time calculator with flask and ajax

## Assignment Information:

Revision Author: John Nemeth
Sources: Class material
         http://arrow.readthedocs.io/en/latest/
         https://docs.python.org/2/tutorial/modules.html
         http://exampleprogramming.com/nose.html
         https://rusa.org/octime_alg.html
         and other, less used web resources

## Description:

For Users: 
This calculator is used by entering in the control distances for a brevet event
to determine the opening and closing times of that control point. When a Mile 
or Kilometer value is entered and enter is pressed or the cursor moves to 
another input field, the times will be calculated and output to the relevant
position on the webpage. The distance of the control point must not be greater
than the brevet distance. A warning will pop up if that happens.

For developers:
Test cases are included in the tests/ directory. It can be executed with
"nosetests tests/ --exe" from the brevets directory while in a virtual
environment.   
