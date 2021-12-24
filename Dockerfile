FROM ubuntu:20.04

# Download updates and install python3, pip and vim
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install vim -y

# Install all requrements for our app
RUN pip install flask pymongo requests bcrypt gevent WSGIServer qrcode libscrc uvicorn fastapi coverage
# Install application

WORKDIR /usr/src/app

COPY . .


# Expose container port to outside host
EXPOSE 8082

# Run application
CMD [ "python3", "servermain.py" ]
