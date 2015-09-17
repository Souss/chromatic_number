#!/usr/bin/env python

from graph import Graph
import argparse
import logging

def         main():

    parser = argparse.ArgumentParser(
        description = "Calculate the chromatic number of a graph descibe into a file."
    )
    parser.add_argument(
        '--files', nargs='+', default=["../tests/test1.txt"], type=str,
        help="List of file that contain descriptions of graphs"
    )
    args = parser.parse_args()

    for filename in args.files:
        try:
            graph = Graph(filename)
            chromatic_number = graph.get_chromatic_number()
            logging.info(
                "[ChromaticNumber][File `{}`] Chromatic number = {}"
                .format(filename, chromatic_number)
            )
        except Exception as err:
            logging.error("[ChromaticNumber][File `{}`] {} ({})"
                          .format(filename, err, type(err)))

if __name__ == "__main__":
    main()
