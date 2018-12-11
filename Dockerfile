FROM python:3.7
MAINTAINER big_J

ENV NAME=reverseroski
ENV PORT=5000

COPY . /${NAME}
WORKDIR /${NAME}

RUN pip install -r requirements.txt

CMD gunicorn -b 0.0.0.0:${PORT} -w 8 reverseroski:app
