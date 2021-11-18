# Simple python client for GROBID REST services

This Python client is used to process a single PDF document by the GROBID service. Results are returned in an XML as well as Python Dictionary format.

## Build and run

You need first to install and start the *grobid* service, latest stable version, see the [documentation](http://grobid.readthedocs.io/). It is assumed that the server will run on the address `http://localhost:8070`. You can change the server address by editing the file `config.json`.

## Requirements

This client has been developed and tested with Python `3.10` and it does not require any dependencies beyond the standard Python ones.

## Install

Get the github repo:

```
git clone https://github.com/imtanay/grobid_client_python
cd grobid_client_python
python3 setup.py install
```

There is nothing more needed to start using this python client.

## Acknoledgement

This project is based on [grobid-python-client](https://github.com/kermitt2/grobid). 

Author and contact: [Tanay Aggarwal](https://www.tanayaggarwal.me/)
