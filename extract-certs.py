#!/usr/bin/python
import argparse
import base64
import json
import os


def main():
    parser = argparse.ArgumentParser(
        description="Extract HTTPS private keys and certificates from Traefik ")
    parser.add_argument('-i', '--acme_json', default="acme.json",
                        help='The path to the acme.json file. Defaults to acme.json in the current working directory')
    parser.add_argument('-d', '--domains', default=[], nargs='*',
                        help='The domains to extract certificates for. Defaults to all.')
    parser.add_argument('-o', '--output_dir', default="./",
                        help='The Path to the directory to store the certificates. Defaults to the current working '
                             'directory.')

    args = parser.parse_args()

    certs = read_certs(args.acme_json, args.domains)
    for i in range(0, len(certs)):
        new_privkey = certs[i]['key']
        new_cert = certs[i]['cert']
        domain = certs[i]["domain"]

        old_privkey = read_cert(args.output_dir, f'{domain}.key')
        old_cert = read_cert(args.output_dir, f'{domain}.pem')
        if new_privkey != old_privkey or new_cert != old_cert:
            print(f'Certificates changed! Writing new files for {domain}')
            write_cert(args.output_dir, f'{domain}.key', new_privkey)
            write_cert(args.output_dir, f'{domain}.pem', new_cert)
        else:
            print(f'Certificates for {domain} unchanged. Skipping...')


def read_cert(storage_dir, filename):
    cert_path = os.path.join(storage_dir, filename)
    if os.path.exists(cert_path):
        with open(cert_path) as cert_file:
            return cert_file.read()
    return None


def write_cert(storage_dir, filename, cert_content):
    cert_path = os.path.join(storage_dir, filename)
    with open(cert_path, 'w') as cert_file:
        cert_file.write(cert_content)
    os.chmod(cert_path, 0o600)


def read_certs(acme_json_path, domains):
    with open(acme_json_path) as acme_json_file:
        acme_json = json.load(acme_json_file)

    certs_json = []
    for provider in acme_json:
        provider_certs = acme_json[provider]["Certificates"]
        for cert in provider_certs:
            domain = cert["domain"]["main"]
            if domains == [] or domain in domains:
                certificate = base64.b64decode(cert["certificate"]).decode("utf-8")
                key = base64.b64decode(cert["key"]).decode("utf-8")
                certs_json.append({
                    "domain": domain,
                    "cert": certificate,
                    "key": key
                })
    return certs_json


if __name__ == '__main__':
    main()