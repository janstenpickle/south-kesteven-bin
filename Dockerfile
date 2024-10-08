FROM python:slim
WORKDIR /app
COPY ./requirements.txt .


#install firefox for headless use firefox:
RUN apt-get update
RUN apt-get install -y firefox-esr
RUN rm -rf /var/lib/apt/lists/*

#install python requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY ./main.py .
#start python script
CMD ["python3", "-u", "main.py"]
