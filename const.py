from enum import Enum


class Const(int, Enum):
    SEED = 17
    ROUNDING = 2
    MU = 0.1
    SIG = 0.3
    N = 100
    CHUNK_SIZE = 100
