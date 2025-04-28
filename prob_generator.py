import os
import argparse
import random

from lark import Lark
from lark.grammar import Terminal, NonTerminal

from collections import defaultdict
from typing import Dict, List, Union, Optional

from tqdm import tqdm


def validate_input_file(grammar):
    if not os.path.exists(grammar):
        raise argparse.ArgumentTypeError("{0} does not exist".format(grammar))
    return grammar


def validate_output_file(output):
    if os.path.exists(output):
        raise argparse.ArgumentTypeError("{0} does already exist".format(output))
    return output


def generate(rules: Dict[NonTerminal, List[Union[NonTerminal, Terminal]]], parser: Lark) -> str:
    """
    Iteratively generate text using a stack-based approach
    """
    stack = ['start']  # Initialize with start symbol
    parts = []

    while stack:
        current = stack.pop()
        if current in rules:  # Non-terminal expansion
            expansion = random.choice(rules[current])
            for symbol in reversed(expansion):
                stack.append(symbol.name)
        else:  # Terminal symbol
            parts.append(parser.get_terminal(symbol.name).pattern.value)
    return ' '.join(parts)


def main(gram_pth: str, output_pth: str, n_iterations: int, seed: Optional[int] = None) -> None:
    pth = os.path.join(gram_pth)
    # parser = Lark(open(pth).read(), start='start', parser='lalr')
    parser = Lark.open(pth, start='start', parser='lalr')

    rules = defaultdict(list)
    for rule in parser.rules:
        rules[rule.origin.name].append(rule.expansion)

    if seed is not None:
        random.seed(seed)
    with open(output_pth, 'a') as file:
        for i in tqdm(range(n_iterations)):
            file.write(generate(rules, parser))
            if i != n_iterations - 1:
                file.write('\n')


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-i', '--input', dest='grammar', type=validate_input_file, required=True, help='Input Lark grammar')
    argParser.add_argument('-o', '--output', dest='output', type=validate_output_file, required=True, help='Output text file')
    argParser.add_argument('-n', '--n_iterations', dest='n_iterations', required=True, type=int, help='Number of strings to generate')
    argParser.add_argument('-s', '--seed', dest='seed', required=False, type=int, help='Randsom seed')
    args = argParser.parse_args()
    main(gram_pth=args.grammar, output_pth=args.output, n_iterations=args.n_iterations, seed=args.seed)
