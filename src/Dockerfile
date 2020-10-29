FROM python:3.8
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt \
    && mkdir -p /usr/src/app/store
VOLUME ["/usr/src/app/store"]
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
