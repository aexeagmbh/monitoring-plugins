FROM aexea/django-base:py2
MAINTAINER Aexea Carpentry

WORKDIR plugins

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["bash"]
