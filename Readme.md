# SPDK JSON-RPC client

See [JSON-RPC Remote access](https://spdk.io/doc/jsonrpc_proxy.html)

This script allows to read a JSON file that contains several requests.

```json
{
	"Name/description of the first request": {
		"id": 1,
		"method": "bdev_get_bdevs"
	},
	"Name/description of the second request": {
		"id": 1,
		"method": "nvmf_get_subsystems"
	}
}
```

The body of a request is a copy/paste of JSON-RPC example given
on [SPDK:JSON-RPC](https://spdk.io/doc/jsonrpc.html).

---

usage: spdk_json_rpc_client.py [-h] [--verbose] [--url location] [--port PORT]
                               [--user username] [--passwd password]
                               jsonfile

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

positional arguments:
  jsonfile              JSON file that contains the request

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         increase verbosity
  --url location        URL of the SPDK JSON RPC server [default: localhost]
  --port PORT           port of the SPDK JSON RPC server [default: 8000]
  --user username, -u username
                        the username [default: admin]
  --passwd password, -p password
                        the password [default: admin]

