# <center>webserver setup</center>

## 1. Connect to EC2 instance
```bash
ssh -i mykey.pem ubuntu@3.84.178.169
```

## 2.Install and configure Apache Web Server
```bash
sudo apt update
sudo apt install apache2
```

## 3. Start Apache service and set it to start automatically on boot
```bash
sudo systemctl start apache2
sudo systemctl enable apache2
```

## 4. Create comp370_hw2.txt file
```
sudo vim /var/www/html/comp370_hw2.txt
```


## 5. Configure Apache to listen on port 8008
* Open the Apache configuration file:
```bash
sudo vim /etc/apache2/ports.conf
```
* Add the following line in the file to change Apache’s listening port to 8008:
```bash
Listen 8008
```

## 6. Set character encoding in HTTP headers
* Ensure that the Apache server correctly sets the character encoding in the HTTP response headers

* edit the Apache configuration file
```bash
sudo vim /etc/apache2/apache2.conf
```
* add this line
```
AddDefaultCharset UTF-8
```

## 7. Restart Apache service
```bash
sudo systemctl restart apache2
```


## 8. visit the file on broser
* address
```bash
http://3.84.178.169:8008/comp370_hw2.txt
```


