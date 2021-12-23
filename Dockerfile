FROM node:16


RUN sudo yum -y update
RUN sudo yum install git 
RUN sudo yum install python3
RUN pip3 install flask pymongo requests bcrypt gevent WSGIServer qrcode libscrc uvicorn fastapi 
EXPOSE 8082
CMD ["python3","servermain.py"]
