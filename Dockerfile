FROM ubuntu:latest
LABEL authors="raphael"

ENTRYPOINT ["top", "-b"]