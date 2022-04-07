FROM python:3.10
LABEL maintainer "David Davó <ddavo@ucm.es>"
ARG POPULATE_CACHE=0
ARG DAOA_VERSION=''

WORKDIR /dao-analyzer

RUN pip install --upgrade pip

COPY . /dao-analyzer/

RUN pip install -e .

RUN if [ "$POPULATE_CACHE" -eq 0 ] && [ -e ./datawarehouse ]; then rm -r ./datawarehouse; fi
RUN if [ "$POPULATE_CACHE" -eq 1 ] ; then python -m cache_scripts --ignore-errors; fi
RUN if [ ! -z "$DAOA_VERSION" ]; then sed -i -e "s/__version__\s*=.*/__version__ = '${DAOA_VERSION}'/i" ./dao_analyzer/__init__.py; fi
VOLUME "/dao-analyzer/datawarehouse"

HEALTHCHECK --interval=5m --timeout=3s --start-period=1m --retries=3 \
  CMD "curl -f localhost" || exit 1

EXPOSE 80

CMD ./init.sh
