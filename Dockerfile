FROM python:3.10
LABEL maintainer "David Davó <ddavo@ucm.es>"
ARG POPULATE_CACHE=0

WORKDIR /dao-analyzer

RUN pip install --upgrade pip

COPY . /dao-analyzer/

RUN pip install -e .
RUN pip install -r requirements_docker.txt
RUN rm -rf .git

RUN if [ "$POPULATE_CACHE" -eq 0 ] && [ -e ./datawarehouse ]; then rm -r ./datawarehouse; fi
RUN if [ "$POPULATE_CACHE" -eq 1 ] ; then daoa-cache-scripts --ignore-errors; fi
VOLUME "/dao-analyzer/datawarehouse"

HEALTHCHECK --interval=5m --timeout=3s --start-period=1m --retries=3 \
  CMD "curl -f localhost" || exit 1

EXPOSE 80

CMD ./init.sh
