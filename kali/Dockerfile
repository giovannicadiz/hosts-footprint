FROM blacktourmaline/kali
ENV PYTHONUNBUFFERED 1
RUN set -ex; \
    	apt-get update; \
	apt-get upgrade -y; \
	apt-get remove -y wmis; \
	apt-get -y install --no-install-recommends \
	python3 wmi-client python3-pip \
	python3-setuptools \
	screen \
	; \
	rm -rf /var/lib/apt/lists/* ;

ADD queries /queries
COPY screen_kali /root/.screenrc
COPY winmap.sh /root/winmap.sh
RUN set -ex; \
	pip3 install -r queries/requirements.txt
