#!/usr/bin/python3
import sys
import logging
import transwarp.cmdline

if __name__ == "__main__":
    try:
        transwarp.cmdline.main()
    except Exception as E:
        logging.error("error: %s" % E)
        raise
        sys.exit(1)
