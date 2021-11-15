# Stride CIP_SOC Crosswalk Server

This server provides a web graphical interface to observe the crosswalk.

It also provides a web API to use in coordination with other programs

## How To Build This Server

1. Make sure Python version >=3.8 is installed on your computer.
2. Ensure that Python library `pip` is installed on your computer.
3. On Ubuntu and Mac, make sure `libpq-dev` library is installed on your computer. On Ubuntu: `sudo apt-get install -y libpq-dev`. For Mac it is recommended to install `postgresql`: `brew install postgresql`
3. In the `server` subdirectory, run `pip install -r requirements.txt`
4. Run server manually following instructions [here](https://fastapi.tiangolo.com/deployment/manually/). Run all commands in the `server` directory.