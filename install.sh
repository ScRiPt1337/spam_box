if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   echo "use command : sudo su"
   exit 1
fi

echo "Installing..."
sudo apt-get update
sudo apt-get install python3 python3-pip git uvicorn -y
sudo git clone https://github.com/ScRiPt1337/spam_box /opt/hacksec_tempmail
pip install -r /opt/hacksec_tempmail/requirements.txt
cp /opt/hacksec_tempmail/hacksec_tempmail/service/* /etc/systemd/system/
sudo systemctl enable hacksec_server.service
sudo systemctl start hacksec_server.service
sudo systemctl enable hacksec_mail.service
sudo systemctl start hacksec_mail.service
