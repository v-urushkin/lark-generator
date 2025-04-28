import os
import argparse


def generate():
    pass


def parse_grammar():
    pass


def main():
    pass


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-i', '--input', dest='grammar', required=True)
    argParser.add_argument('-n', '--n_iterations', dest='n_iterations', required=True, type=int, help='Number of strings to generate')
    args = argParser.parse_args()
    main()
