
set -x
if [ -z $1 ] || [ -z $2 ]  ; then
    echo "pass tag version"
    exit 2
fi


rsync -av global/general/* hostfootprint/general/

docker_build(){
    cd $1
    docker build -t "blacktourmaline/$1":"$2" .
    docker tag `docker images | grep "blacktourmaline/$1" | grep -F "$2" | grep -v none | awk '{ print $3 }'` docker.io/blacktourmaline/"$1":"$2"

    docker push docker.io/blacktourmaline/"$1":"$2"
    cd ..
}

case $1 in
    all)
	for i in `echo "global hostfootprint kali"`; do
	    docker_build $i $2
	done
	;;
    global)
	docker_build global $2
	;;
    hostfootprint)
	docker_build hostfootprint $2
	;;
    kali)
	docker_build kali $2
	;;
esac
