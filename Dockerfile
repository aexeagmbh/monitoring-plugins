FROM axsemantics/django-base:py3.8-buster
MAINTAINER Aexea Carpentry

WORKDIR plugins

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["bash"]
