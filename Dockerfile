FROM python:3.8


WORKDIR /insurance_quote

COPY app/. /insurance_quote/

#RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000 

ENV FLASK_APP=app.py

ENTRYPOINT ["flask"]

CMD [ "run", "--host", "0.0.0.0" ]