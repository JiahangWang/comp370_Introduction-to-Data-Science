# <center>database setup</center>

## 1. Connect to EC2 instance
```bash
ssh -i mykey.pem ubuntu@3.84.178.169
```

## 2. install MariaDB
```bash
sudo apt update
sudo apt install mariadb-server
```

## 3. Configure the database to run on an external port
* open the configuration file:
```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

* Find and comment out the following line
```
bind-address            = 127.0.0.1
```

## 4. Restart MariaDB Service
```bash
sudo service mariadb restart
```

## 5. set the password for the root user
* Open the terminal and log into the MariaDB server with superuser privileges:
```bash
sudo mysql
```
* set the password for the root user
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root_password';
```
* Refresh permissions and exit
```sql
FLUSH PRIVILEGES;
EXIT；
```

## 6. Create an Empty Database
* log in to database
```bash
mysql -u root -proot_password
```
* create database and exit
```sql
CREATE DATABASE comp370_test;
EXIT;
```

## 7. Add a New User
* log in to database
```bash
mysql -u root -proot_password
```
* add a user named “comp370” and set a password for it
```sql
CREATE USER 'comp370'@'%' IDENTIFIED BY '$ungl@ss3s';
```
* give prililege to new user
```sql
GRANT ALL PRIVILEGES ON comp370_test.* TO 'comp370'@'%';
```

* Refresh permissions and exit
```sql
FLUSH PRIVILEGES;
EXIT；
```

## 8. change the port of MariaDB
* open the MariaDB configuration file
```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```
* In the configuration file, find the [mysqld] section and add or edit the following line to specify the new port
```sql
[mysqld]
port = 6002
```
* Restart the MariaDB service to make changes effective:
```bash
sudo service mariadb restart
```

## 9. DBeaver
* Use database client to connect MariaDB database server on EC2

* connection information
```
- Host: 3.84.178.169
- Port: 6002
- Username: comp370
- Password: $ungl@ss3s
- Database: comp370_test
```
