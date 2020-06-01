FROM python:3.7-slim-buster AS compile-image
LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

RUN python -m venv /opt/venv
# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"

COPY . /usr/src/wazo-purge-db
WORKDIR /usr/src/wazo-purge-db
RUN pip install -r requirements.txt
RUN python setup.py install

FROM python:3.7-slim-buster AS build-image
COPY --from=compile-image /opt/venv /opt/venv

COPY ./etc/wazo-purge-db /etc/wazo-purge-db
RUN true \
    && mkdir -p /etc/wazo-purge-db/conf.d \
    && install -d -o www-data -g www-data /run/wazo-purge-db/ \
    && install -o www-data -g www-data /dev/null /var/log/wazo-purge-db.log

# Activate virtual env
ENV PATH="/opt/venv/bin:$PATH"
CMD ["wazo-purge-db"]
