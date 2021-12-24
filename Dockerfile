FROM python3
# Set application working directory
# Install requirements
RUN pip install flask pymongo requests bcrypt gevent WSGIServer qrcode libscrc uvicorn fastapi coverage
# Install application
COPY ..
EXPOSE 8082
# Run application
CMD [ "python3","servermain.py"]
