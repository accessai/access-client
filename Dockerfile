FROM python:3.6-slim

RUN apt-get -qy update && apt-get -qy install build-essential && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/* && \
    mkdir -p /accessai/access-fiu

WORKDIR /accessai/access-fiu

# layer caching since dependencies don't change much
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
SHELL ["/bin/bash", "-c"]
RUN python setup.py install
WORKDIR /accessai
COPY samples .

# cleanup
RUN rm -r access-fiu

VOLUME ["/accessai"]

EXPOSE 8000
CMD ["python", "-m", "access_fiu"]
