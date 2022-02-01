FROM python:3.10
LABEL maintainer "David Davó <ddavo@ucm.es>"
ARG POPULATE_CACHE=0

WORKDIR /dao-analyzer

COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY . /dao-analyzer/

RUN if [ "$POPULATE_CACHE" -eq 1 ] ; then ./cache_scripts/main.py --ignore-errors; fi

HEALTHCHECK --interval=5m --timeout=3s --start-period=1m --retries=3 \
  CMD "curl -f localhost" || exit 1

EXPOSE 80

CMD ./init.sh
