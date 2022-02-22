if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   echo "use command : sudo su"
   exit 1
fi

echo "Uninstalling..."
rm -rf /opt/hacksec_tempmail/
sudo systemctl stop hacksec_mail.service
sudo systemctl stop hacksec_server.service
sudo systemctl disable hacksec_server.service
sudo systemctl disable hacksec_mail.service
rm /etc/systemd/system/hacksec_server.service
rm /etc/systemd/system/hacksec_mail.service
