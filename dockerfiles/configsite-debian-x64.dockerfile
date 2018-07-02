FROM debian:latest

RUN apt-get update ; apt-get -y upgrade ; apt-get update
RUN apt-get -y install python3 sudo debhelper dh-virtualenv dpkg-dev python3-venv

# Set up the dockcross entry point
COPY dockerfiles/dockcross/entrypoint.sh dockerfiles/dockcross/dockcross /dockcross/
RUN chmod 777 -R /dockcross
ENTRYPOINT ["/dockcross/entrypoint.sh"]

ENV DEFAULT_DOCKCROSS_IMAGE configsite-debian-x64
COPY dockerfiles/*.deb dockerfiles/configsite-debian-x64.dockerfile /temp/
WORKDIR /temp
RUN dpkg -i configsite_0.1-1_amd64.deb && echo "Configsite installed" || echo "Configsite not installed"

WORKDIR /work
