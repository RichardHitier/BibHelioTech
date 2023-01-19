FROM ubuntu:22.04
LABEL maintainer="Benjamin Renard <benjamin.renard@irap.omp.eu>,\
                  Richard Hitier <hitier.richard@gmail.com>"

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common git wget unzip python3 python3-pip python3-venv openjdk-8-jre openjdk-8-jdk maven zip vim curl poppler-utils zip
RUN add-apt-repository ppa:alex-p/tesseract-ocr && \
    apt install -y tesseract-ocr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java

ARG USER_UID
ARG USER_GID

RUN groupadd --gid $USER_GID bibheliotech && \
    useradd --uid $USER_UID --gid $USER_GID -ms /bin/bash bibheliotech
USER bibheliotech
WORKDIR /home/bibheliotech

ENV VIRTUAL_ENV=/home/bibheliotech/venv
RUN python3 -m venv $VIRTUAL_ENV &&\
    . ./venv/bin/activate &&\
    pip install --upgrade pip
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -U pip sutime && \
    mvn dependency:copy-dependencies -DoutputDirectory=./jars -f $(python -c 'import importlib; import importlib.util; import pathlib; print(pathlib.Path(importlib.util.find_spec("sutime").origin).parent / "pom.xml")')

# RUN git clone https://github.com/ADablanc/BibHelioTech.git
WORKDIR /home/bibheliotech/BibHelioTech
COPY . .
RUN pip install wheel && pip install -r requirements.txt
RUN cd ressources/ && \
    jar uf $VIRTUAL_ENV/lib/python3.10/site-packages/sutime/jars/stanford-corenlp-4.0.0-models.jar \
           edu/stanford/nlp/models/sutime/english.sutime.txt