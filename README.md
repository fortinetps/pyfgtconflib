# pyfgtconflib


##### Author :
Don Yao


#### Description : 
A simple and tiny FortiGate Configuration file parser.
It takes FortiGate Configuration as input, and output as python defaultdict.
The core parsing fuctions implemented in less than 100 lines of code.


##### Install :
pip install pyfgtconflib


#### Usage :
In [pyfgtconflib](https://github.com/fortinetps/pyfgtconflib) source repository.

A demo script called [import_export.py](https://github.com/fortinetps/pyfgtconflib/blob/main/tests/import_export.py) in tests folder.
This script open a FortiGate configuration file, parses configuration file into python dictionary, 
and print the dictionary out with nicely formatted text.
You can redirect the output to a file, to compare the original input FortiGate configuration file, 
so you could verify the config paring (import) and config dictionary printing out (export) works.

A demo script called [remove_password.py](https://github.com/fortinetps/pyfgtconflib/blob/main/tests/remove_password.py) in tests folder.
This script open a FortiGate configuration file, parses configuration file into python dictionary, 
when printing the dictionary out, it removes/strips all (encrypted) passwords, private-key, and certificate in configuration, 
it will be a little safer to share the configuration file without these information.

For additional usages/demos/tools, please check this GitHub repo site:
https://github.com/fortinetps/FortiGateConfigTools
