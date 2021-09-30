sudo apt-get update
sudo apt-get install python3 python3-pip git uvicorn -y
pip install -r requirements.txt
cp ./hacksec_tempmail/service/* /etc/systemd/system/
systemctl enable hacksec_server.service
systemctl start hacksec_server.service
systemctl enable hacksec_mail.service
systemctl start hacksec_mail.service