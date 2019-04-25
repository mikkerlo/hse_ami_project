FROM ubuntu:bionic

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        git && \
    pip3 install flake8 \
    pep8-naming \
    flake8-comprehensions \
    flake8-pep3101 \
    flake8-pyi \
    flake8-quotes \
    flake8-mutable

