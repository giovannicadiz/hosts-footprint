# Usage VERSION="prod" o VERSION="1.0"

build-image: 
	docker build -t blacktourmaline/hostfootprint:${VER} .

push: build-image
	docker push docker.io/blacktourmaline/hostfootprint:${VER}
