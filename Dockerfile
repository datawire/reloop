FROM datawire/base-ubuntu:f57de33dfe
MAINTAINER Datawire <dev@datawire.io>
LABEL PROJECT_REPO_URL         = "git@github.com:datawire/reloop.git" \
      PROJECT_REPO_BROWSER_URL = "https://github.com/datawire/reloop" \
      DESCRIPTION              = "Datawire Reloop" \
      VENDOR                   = "Datawire, Inc." \
      VENDOR_URL               = "https://datawire.io/"

#
# README
# ------
#
# This is a Docker image for the Datawire Reloop project.
#
# This Dockerfile is structured to optimally use the Docker cache as much as possible without being inflexible. The
# general order of events is:
#
# 1. Install OS dependencies which do not change too much
# 2. Install application dependencies (e.g. Python requirements.txt)
# 3. Install the application code
# 4. Configure things that need to be configured (e.g. nginx)
#
# The service and configuration will be installed into /datawire/config and /datawire/<module>. If you modify <module>
# in your program source tree (e.g. rename 'hello' to 'foobar' then update config/uwsgi.ini to the new module name.
#
# ASK if you do not know the answer before blindly hacking up this file!
#

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY dist/reloopd /bin

RUN chmod +x /bin/reloopd
ENTRYPOINT ["/bin/reloopd", "run"]
