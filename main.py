import multiprocessing as mp

from webcam import _webcam
from scale  import _scale



if __name__ == '__main__':
    with multiprocessing.Pool(processes=3) as pool:
        #
