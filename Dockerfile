FROM python:3.7

WORKDIR /da_bot

COPY requirements.txt requirements.txtвщслук 
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE $PORT
CMD ["python", "main.py"]