from src.arguments import DefaultArgumentsSchema
from src.utils import argutil


def main():
    parser = argutil.ArgumentParser(schema=DefaultArgumentsSchema)
    parser.parse_typed_args()


if __name__ == '__main__':
    main()
