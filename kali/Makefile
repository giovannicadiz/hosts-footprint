# Usage VERSION="prod" o VERSION="1.0"

build-image: 
	docker build -t blacktourmaline/kali:${VER} .

push:
	docker tag ${TAG} blacktourmaline/kali:${VER}
	docker push docker.io/blacktourmaline/kali:${VER}
