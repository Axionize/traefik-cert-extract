### Usage
```
usage: extract-certs.py [-h] [-i ACME_JSON] [-d [DOMAINS ...]] [-o OUTPUT_DIR]

Extract HTTPS private keys and certificates from Traefik

options:
  -h, --help            show this help message and exit
  -i ACME_JSON, --acme_json ACME_JSON
                        The path to the acme.json file. Defaults to acme.json in the current working directory
  -d [DOMAINS ...], --domains [DOMAINS ...]
                        The domains to extract certificates for. Defaults to all.
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        The Path to the directory to store the certificates. Defaults to the current working directory
```
### Examples
If `acme.json` is in your current directory just run to extract all certificates.
`python /path/to/extract-certs.py`