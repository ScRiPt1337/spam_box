sudo apt-get update
sudo apt-get install python3 python3-pip git uvicorn -y
git clone https://github.com/ScRiPt1337/spam_box /opt/
pip install -r requirements.txt
cp ./hacksec_tempmail/service/* /etc/systemd/system/
systemctl enable hacksec_server.service
systemctl start hacksec_server.service
systemctl enable hacksec_mail.service
systemctl start hacksec_mail.service