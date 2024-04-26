# INDpay
INDpay_blockchain  
Unlocking Borderless Payments with Blockchain Innovation.   
Blockchain technology is revolutionizing the way we think about cross-border transactions. Discover how innovative blockchain solutions are unlocking a new era of seamless, secure, and lightning-fast global payments.


#INDpay DEMO

https://github.com/saifism/INDpay/assets/114340669/f6687884-bb49-44e3-9a32-d4c3e1578ccb



#MySql blockchain database

<img width="1680" alt="Screenshot 2024-04-26 at 10 21 40 PM" src="https://github.com/saifism/INDpay/assets/114340669/bcdac1b3-8637-4cb7-abf5-277d9312b8c6">



## Getting Started
To get started simply download this repository.

From the command line:

```
https://github.com/saifism/INDpay.git
```

Once downloaded, switch into the source folder and run app.py
```
$ cd INDpay # This may be different for you
$ python app.py
```
INDpay is now up and running!

## Prerequisites

### Install mySQL
Note: You may skip this if you already have mySQL installed
```
$ brew install mysql 
$ brew tap homebrew/services
$ brew services start mysql
$ mysqladmin -u root password 'yourpassword' 
```

### Configure mySQL 
Start mySql session in terminal
```$ mysql -u root -p```

Enter your password in app.py in 

app.config['MYSQL_PASSWORD'] = 'password' 


#### Create database and tables
```
mysql> 
       CREATE DATABASE INDpay;
       use INDpay;
       CREATE TABLE users(name varchar(30), email varchar(30), username varchar(20), password varchar(50));
       CREATE TABLE blockchain(number varchar(30), hash varchar(68), previous varchar(68), data varchar(100), nonce varchar(30));
```

#### Configure Database Config File
Update Line 41 in ```app.py``` with the password saved above

If you are having troubles install mySql, you may use the link below. 
https://www.youtube.com/watch?v=UcpHkYfWarM 

### Dependencies
Make sure you have Python 3 installed. Install the following dependencies.
``` 
pip3 install -r requirements.txt 
```

```  
# You can also install them manually

$ pip install Flask
  pip install simple-crypt
  pip install passlib
  pip install flask_mysqldb #mySql must be installed, see below
  pip install functools
  pip install wtforms
```

## Built With
HTML - Front end web framework

CSS - Front end styling

JS - Backend framework

Python - Backend application

Flask - Python Web Framework


## Authors
SUHAIL SAIFI - Entire Project

KARAN RANA - Blockchain / Installation Process


## License
This project is licensed under the MIT License - see the LICENSE file for details


