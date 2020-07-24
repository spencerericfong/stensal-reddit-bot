from modes import *
import sys

def main():
    if '--manual' in sys.argv or '--m' in sys.argv:
        manual()
        sys.exit(0)
    else:
        auto()
        sys.exit(0)

if __name__ == '__main__':
    main()
