FROM python:3.11-slim

WORKDIR /app

COPY requirement.txt .
RUN pip install -r requirement.txt

COPY . .

ENV FLASK_APP=app.py

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
