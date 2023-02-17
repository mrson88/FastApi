"# FastAPI"

$ sudo apt-get update
$ sudo apt install python3-pip
$ pip3 install -r requirements.txt

$ sudo apt install nginx

$ cd /etc/nginx/sites-enabled/
$ sudo nano fastapi_nginx

server {    
listen 80;    
server_name 44.202.137.;    
location / {        
proxy_pass http://127.0.0.1:8000;    
}
}
caddy reverse-proxy --from phuonghoang88.online --to localhost:8000
$ sudo service nginx restart
$ python3 -m uvicorn main:app
uvicorn main:app --reload --host 0.0.0.0 --port 80

#set password linux
echo "export PASS_DATABASE=" >> ~/.bashrc
echo "export PASS_MAIL=" >> ~/.bashrc
echo "export MAIL_NAME=" >> ~/.bashrc