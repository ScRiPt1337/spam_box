# spam_box
![Screenshot](https://raw.githubusercontent.com/ScRiPt1337/spam_box/main/banner.png)

spam_box is a self hosted temp mail service by hacksec

### Requirement

- python3
- open port 25 and 6660
- root access in a vps 

### How to install in linux
```bash
curl -s -L https://raw.githubusercontent.com/ScRiPt1337/spam_box/main/install.sh | bash
```

### Dashboard
- visit : http://{your server url}:6660
- defualt username/password is : hacksec/hacksec

### Add your own domain
- Create an A DNS record with the name mail.yourdomain.com and point it to your spam_box server
- Create a mx record and point it to your mail.youdomain.com

### Demo with setup tutorial
- https://youtu.be/VqhIQxck9O4

### Live Demo
- http://hacksec.ml:6660/home/

### REST API docs
- http://hacksec.ml:6660/docs

### Contact info 
- Email : script@hacksec.in
- visit our website : https://www.hacksec.in
