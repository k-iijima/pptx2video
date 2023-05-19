FROM nvidia/cuda:11.0.3-base-ubuntu20.04
USER root

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ Asia/Tokyo

RUN mkdir -p /root/src
COPY src/ /root/src/
COPY requirements.txt /root/src
WORKDIR /root/src/

RUN sed -i 's@archive.ubuntu.com@ftp.jaist.ac.jp/pub/Linux@g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository ppa:apt-fast/stable && \
    apt-get update && \
    apt-get -y install apt-fast &&\
    apt-fast -y install locales tzdata && \
    locale-gen ja_JP.UTF-8 && \
    #localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    apt-fast -y install libopencv-dev cmake wget sudo python3-pip libx264-dev ffmpeg libreoffice python3-uno zip unzip fontconfig imagemagick && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip uninstall uno
RUN pip install -r requirements.txt

RUN wget https://moji.or.jp/wp-content/ipafont/IPAexfont/IPAexfont00301.zip && \
    unzip IPAexfont00301.zip && \
    mkdir -p /usr/share/fonts/ipa && \
    cp IPAexfont00301/*.ttf /usr/share/fonts/ipa && \
    fc-cache -fv

COPY ./policy.xml /etc/ImageMagick-6/policy.xml
