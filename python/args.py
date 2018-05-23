from argparse import ArgumentParser

def get_args():

    # Process the command line args
    parser = ArgumentParser()
    parser.add_argument('-s', '--silent', help='do not provide a console prompt,'\
                        + ' use this mode when running as a systemd service', \
                        action='store_true')
    return parser.parse_args()
