FROM blacktourmaline/kali
ENV PYTHONUNBUFFERED 1
RUN set -ex; \
    	apt-get update; \
	apt-get -y install --no-install-recommends \
	python3 wmis python3-pip \
	python3-setuptools \
	; \
	rm -rf /var/lib/apt/lists/* ;

ADD queries /queries
RUN set -ex; \
	pip3 install -r queries/requirements.txt		
