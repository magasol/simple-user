﻿# simple-user
Required: 
- Internet Connection 
- OS: Windows 
- python3.8 https://www.python.org/downloads/release/python-380/ 
- pip https://pip.pypa.io/en/stable/installing/

Before running the program installing required packages:
```
python setup.py install
```
Uninstalling packages run
```
uninstall.cmd
```
Running the program:
```
python script.py [command]
```
Commands: \
__average-age [x]__ -> Count average age of men or women or general [ female | male | all ] all is defult value \
__born [x] [y]__ -> List persons born between given dates: from -> x and to -> y in format '%Y-%m-%d' \
__clear__ -> Remove persons from database \
__gender-percentage [x]__ -> Count gender percentage [ male | female ] \
__info__ -> Short Info about program \
__list [x]__ -> List x number of persons (first name, last name, gender, age) \
__load [x]__ -> oad x number of new persons into database \
__most-common-cities [x]__ -> Show most common x cities and number of its occurrences \
__most-common-passwords [x]__ -> Show most common x passwords and number of its occurrences \
__safest-password__ -> Show safest password 
