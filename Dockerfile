FROM nvcr.io/nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

ENV NVIDIA_DRIVER_CAPABILITIES=all 
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get -y update && apt-get install -y \
    software-properties-common \
    build-essential \
    checkinstall \
    cmake \
    pkg-config \
    yasm \
    git \
    vim \
    curl \
    wget \
    sudo \
    apt-transport-https \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    dbus-x11 \
    iputils-ping \
    python3-dev \
    python3-pip

# some image/media dependencies
RUN apt-get -y update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libjpeg8-dev \
    libpng-dev \
    libtiff5-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libdc1394-22-dev \
    libxine2-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata python3-tk
ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get clean && rm -rf /tmp/* /var/tmp/* /var/lib/apt/lists/* && apt-get -y autoremove

RUN pip3 install --no-cache-dir --upgrade pip 

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY requirements-git.txt .
RUN pip3 install --no-cache-dir -r requirements-git.txt
