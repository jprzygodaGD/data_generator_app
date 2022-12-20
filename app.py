from processor import ArgumentProcessor
from parser import collect_args


def main():
    arguments = ArgumentProcessor(collect_args())
    arguments.produce_output()


if __name__ == "__main__":
    main()