from enum import Enum


class Instruction(Enum):
    FROM = "FROM"
    RUN = "RUN"
    COPY = "COPY"
    ADD = "ADD"
    CMD = "CMD"
    ENTRYPOINT = "ENTRYPOINT"
    ENV = "ENV"
    EXPOSE = "EXPOSE"
    VOLUME = "VOLUME"
    WORKDIR = "WORKDIR"
