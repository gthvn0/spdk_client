"""Simple module to send request to SPDK JSON RPC"""
import argparse
import json
import sys
import textwrap
import requests

SUCCESS = 0
ERR_FILE_NOT_FOUND = 1
ERR_WRONG_JSON = 2
ERR_MISSING_METHOD = 3
ERR_STATUS_CODE = 4

def request_is_valid(request):
    """Return true if the request is valid.
    A request is valid if it has a key 'method'.
    """
    return 'method' in request

def send_request(url, user, passwd, payload):
    """Send an SPDK JSON RPC Request and print the answer if any"""
    response = requests.post(url,
                             data=json.dumps(payload),
                             auth=(user, passwd),
                             verify=False,
                             timeout=30)

    if response.status_code != 200:
        print("Status code {}".format(response.status_code))
        return ERR_STATUS_CODE

    try:
        print(json.dumps(response.json(), indent = 4, sort_keys=True))
    except ValueError:
        print("{}".format(response.text))
        return ERR_WRONG_JSON

    return SUCCESS

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Simply send a request to an SPDK JSON RPC server.
            The JSON file can contains one or more requests.
            The format is the following:
               { 
                    "request_with_a_given_name": {
                        "id": 1,
                        "method": "bdev_get_bdevs"
                    }
                    "request_with_another_name": {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "nvmf_create_subsystem",
                        "params": {
                            "nqn": "nqn.2020-11.io.spdk:cnode1",
                            "allow_any_host": True,
                            "serial_number": "SKENRO4VDB8X"
                        }
                    }
                    ...
                }
            '''))
    parser.add_argument("--verbose", "-v", action='store_true',
                        help="increase verbosity")
    parser.add_argument("--url", type=str, metavar="location", default="localhost",
                        help="URL of the SPDK JSON RPC server [default: localhost]")
    parser.add_argument("--port", type=str, default="8000",
                        help="port of the SPDK JSON RPC server [default: 8000]")
    parser.add_argument("--user", "-u", type=str, metavar="username", default="admin",
                        help="the username [default: admin]")
    parser.add_argument("--passwd", "-p", type=str, metavar="password", default="admin",
                        help="the password [default: admin]")
    parser.add_argument("jsonfile", type=str,
                        help="JSON file that contains the request")

    args = parser.parse_args()
    json_rpc_url = "http://" + args.url + ":" + args.port
    if args.verbose:
        print("Parameters are:")
        print("  url      : " + json_rpc_url)
        print("  user     : " + args.user)
        print("  password : " + args.passwd)
        print("  JSON file: " + args.jsonfile)
        print()

    try:
        with open(args.jsonfile) as f:
            try:
                reqs = json.load(f)
            except ValueError: # includes json.decoder.JSONDecodeError
                print('ERROR: Failed to decode your JSON file')
                sys.exit(ERR_WRONG_JSON)
    except FileNotFoundError:
        print("ERROR: {} no such file or directory".format(args.jsonfile))
        sys.exit(ERR_FILE_NOT_FOUND)

    for k in reqs.keys():
        print("\n====> Parsing request {}\n".format(k))
        if not request_is_valid(reqs[k]):
            print("SKIP: {} request doesn't have any SPDK method".format(k))
            continue

        answer = send_request(json_rpc_url, args.user, args.passwd, reqs[k])
        if answer == ERR_STATUS_CODE:
            print("ERROR: Server returns wrong status code")
        elif answer == ERR_WRONG_JSON:
            print("ERROR: Failed to decode the answer from the JSON RPC server")
