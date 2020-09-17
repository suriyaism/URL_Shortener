FROM python:3.7.3

RUN pip install --upgrade pip

COPY . /usr/src/app/

WORKDIR /usr/src/app
RUN pip install -r requirements.txt

CMD python run.py