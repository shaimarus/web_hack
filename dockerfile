FROM dizcza/docker-hashcat

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.8 \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /opt/hashcat/
RUN pip3 --no-cache-dir install -r /opt/hashcat/requirements.txt

RUN mkdir /opt/JohnTheRipper/
RUN mkdir /opt/tmp/
RUN git clone "https://github.com/magnumripper/JohnTheRipper.git" /opt/JohnTheRipper/ && cd /opt/JohnTheRipper/src && ./configure && make -s clean && make -sj4

COPY ./dict/ /opt/hashcat/dict
COPY ./static/ /opt/hashcat/static
COPY ./templates/ /opt/hashcat/templates

COPY ./web_hack.py /opt/hashcat/



WORKDIR /opt/hashcat