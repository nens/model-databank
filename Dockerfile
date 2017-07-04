# for now, use the same base image as the subgrid-flow image uses
FROM harbor.lizard.net/threedi/subgrid-flow-base-trusty:20170615

# six is required; cleanup after install
RUN pip install -U six && rm -rf /tmp/*

# make sure buildout cache directories are not in the docker container
# RUN rm -r ~/.buildout

VOLUME /srv
