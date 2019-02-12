## KEEP IN MY MIND WHILE CODING



* __#1: You're responsible for code quality.__
* __#2: Use meaningful names.__
* __#3: Write code that expresses intent.__
* __#4: Code should speak for itself. Less comments = less maintenance.__
* __#5: Leave the code better than you found it.__
* __#6: Single-responsibility code.__
i.e function does 1 thing well. Less arguments = better function.
classes: most methods use most of the class' properties.
* __#7: Tests (TDD).__
* __#8: Work on big picture skeleton, then fill in the details later__ 
(interface first, implementation later).
* __#9: Independent components that can be used in different places.__
* __#10: Master your craft__

___

## Setup Instructions:

### Linux Machines:

* __#1: Install the right version of mongoDB from [here](https://websiteforstudents.com/install-mongodb-on-ubuntu-18-04-lts-beta-server/) or for non-ubuntu users [here](https://docs.mongodb.com/manual/administration/install-on-linux/) and start the mongodb server__
* __#2: open up the terminal and type the following__ 
```
git clone https://github.com/never2average/CyllideBackend
cd CyllideBackend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd CyllideBackend
python3 app.py
```

### Non-linux Machines:


* __#1: Get mongodb installed and running from [here](https://docs.mongodb.com/manual/administration/install-on-os-x/)__
* __#2: Repeat from step 2__
