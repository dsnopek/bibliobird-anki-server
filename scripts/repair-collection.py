#!/usr/bin/env python

from BibliobirdAnkiServer.common import CollectionInitializer

from anki import Collection

import sys

def main():
    col = Collection(sys.argv[1])
    setup = CollectionInitializer()
    setup(col)

if __name__ == '__main__': main()

