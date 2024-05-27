FROM python:3.12
ARG POPULATE_CACHE=0
ARG PYTHON_PKG=dao-analyzer
ARG DAOA_VERSION
ARG REVISION
ARG CREATED

LABEL maintainer "David Davó <ddavo@ucm.es>"
LABEL org.opencontainers.image.source "https://github.com/grasia/dao-analyzer"
LABEL org.opencontainers.image.licenses "GPL-3.0"
LABEL org.opencontainers.image.title "DAO-Analyzer"
LABEL org.opencontainers.image.description "Explore the DAO world"
LABEL org.opencontainers.image.revision $REVISION 
LABEL org.opencontainers.image.version $DAOA_VERSION
LABEL org.opencontainers.image.created $CREATED

WORKDIR /dao-analyzer

COPY . ./

RUN pip install --upgrade pip

RUN --mount=type=cache,target=/root/.cache pip install $PYTHON_PKG[docker]
RUN rm -rf ./dist

RUN if [ "$POPULATE_CACHE" -eq 0 ] && [ -e ./datawarehouse ]; then rm -r ./datawarehouse; fi
RUN if [ "$POPULATE_CACHE" -eq 1 ] ; then daoa-cache-scripts --ignore-errors; fi
VOLUME "/dao-analyzer/datawarehouse"

ENV PATH="$PATH:/dao-analyzer/scripts"

HEALTHCHECK --interval=5m --timeout=3s --start-period=1m --retries=3 \
  CMD "curl -f localhost" || exit 1

EXPOSE 80

CMD ./init.sh
