#!/usr/bin/env python

from chromaticgraph import ChromaticGraph as Graph
import argparse
import logging
import time

def         main():

    parser = argparse.ArgumentParser(
        description = "Calculate the chromatic number of a graph descibe into a file."
    )
    parser.add_argument(
        '--files', nargs='+', default=["../tests/test1.txt"], type=str,
        help="List of file that contain descriptions of graphs"
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='[Chromatic][%(asctime)s](%(levelname)s): %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S'
        )

    for filename in args.files:
        try:
            graph = Graph(filename)
            chromatic_number = graph.get_chromatic_number()
            logging.info(
                "File `{}`, Chromatic number = {}"
                .format(filename, chromatic_number)
            )
        except Exception as err:
            logging.error("File `{}`, {} ({})"
                          .format(filename, err, type(err)))

if __name__ == "__main__":
    main()
