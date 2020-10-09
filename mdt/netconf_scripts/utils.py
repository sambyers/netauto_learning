import argparse


def cliargs():
    parser = argparse.ArgumentParser(description='Args need to connect to the system via NETCONF')
    parser.add_argument('-a', '--host',
                        help='Host to configure')
    parser.add_argument('-u', '--username',
                        help='Username for NETCONF')
    parser.add_argument('-p', '--password',
                        help='Password for NETCONF')
    parser.add_argument('-v', '--vars',
                        help='Vars file')
    args = parser.parse_args()
    return args
