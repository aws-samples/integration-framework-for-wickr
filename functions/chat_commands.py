import argparse
import shlex

def main():
    arger = argparse.ArgumentParser()

    # Arguments for top-level, e.g "subcmds.py -v"
    arger.add_argument("-v", "--verbose", action="count", default=0)

    subparsers = arger.add_subparsers(dest="command")

    # Make parser for "subcmds.py info ..."
    info_parser = subparsers.add_parser("info")
    info_parser.add_argument("-m", "--moo", dest="moo")

    # Make parser for "subcmds.py create ..."
    create_parser = subparsers.add_parser("/runbook")
    create_parser.add_argument("name")
    create_parser.add_argument("additional", nargs="*")

    # Parse
    argString = '-v /runbook Infosec-Isolate ee'
    opts = arger.parse_args(shlex.split(argString))

    # Print option object for debug
    print(opts)

    if opts.command == "info":
        print("Info command")
        print("--moo was %s" % opts.moo)

    elif opts.command == "/runbook":
        print("Running runbook %s" % opts.name)
        print("Additional: %s" % opts.additional)

    else:
        # argparse will error on unexpected commands, but
        # in case we mistype one of the elif statements...
        raise ValueError("Unhandled command %s" % opts.command)


if __name__ == '__main__':
    main()