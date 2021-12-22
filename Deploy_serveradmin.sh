sudo yum -y update

sudo yum install git
sudo yum install python3
pip3 install flask pymongo requests bcrypt gevent WSGIServer qrcode libscrc
git clone https://github.com/Teejirapat/CS360-hotel-system.git
cd CS360-hotel-system
python3 serveradmin.py
