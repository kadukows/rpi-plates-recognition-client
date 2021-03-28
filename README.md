# rpi-plates-recognition-client
RPi side of rpi-plates-recognition project

## Setting up
To run flask server and other utilities this project requires 1st time set up.
After cloning and cd'ing into repo:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
This installs all appropriate packages into venv, and needs to be done only once.

After that, each time you log into new terminal you need to activate venv with
`source venv/bin/activate`.

## Running WebSocket client
This package contains one method, `run`. Simply import this method and call
this method with servers ip and unique-id to initialize connection.

## Running unit tests
To run unit tests, simply run `pytest` from root directory of repo.
