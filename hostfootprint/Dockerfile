FROM python:3
ENV PYTHONUNBUFFERED 1
RUN set -ex; \
    	http_proxy="http://172.32.49.146:9999"  https_proxy="http://172.32.49.146:9999" \ 
    	apt-get update; \
    	http_proxy="http://172.32.49.146:9999"  https_proxy="http://172.32.49.146:9999" \ 
	apt-get -y install --no-install-recommends \
	nmap vim-tiny curl \
	screen \
	; \
	rm -rf /var/lib/apt/lists/* ;
	
RUN mkdir /hostfootprint
WORKDIR /hostfootprint
ADD requirements.txt /hostfootprint
RUN set -ex; \
    	http_proxy="http://172.32.49.146:9999"  https_proxy="http://172.32.49.146:9999" \ 
	pip install -r requirements.txt		
ADD . /hostfootprint
COPY looping_map.sh /root/looping_map.sh
COPY screen_hostfootprint /root/.screenrc