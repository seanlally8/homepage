FROM ubuntu:latest

RUN apt update && apt upgrade -y &&\
	DEBIAN_FRONTEND=noninteractive\
	apt install -y python3 python3-pip &&\
	pip install Flask
	
