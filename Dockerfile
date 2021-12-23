FROM python:3
# Set application working directory
WORKDIR /usr/src/app
# Install requirements
RUN pip install flask pymongo requests bcrypt gevent WSGIServer qrcode libscrc uvicorn fastapi coverage
# Install application
COPY servermain.py ./
# Run application
CMD python servermain.py
