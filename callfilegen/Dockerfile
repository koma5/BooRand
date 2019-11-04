FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY callfilegen.py .

CMD [ "python", "-u", "./callfilegen.py" ]
