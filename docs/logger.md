# Logging in rpi-plates-recognition-client
This document details use of logger in this package. It is implemented through
`logging` package available by default in python and as such you can refer to
it's excellent documentation if this document isn't enough ([logging]
(https://docs.python.org/3/library/logging.html)).

## Usage
If you want to log something simply import logging package and instantiate
'new' logger with `.getLogger` function. Please be aware that for your logs to
be sent through WebSocket connection your logger must have specific name -
'rpiplatesrecognition_client.your-custom-name'. This allows logging package to
inherit configuration from base logger.


## Example
```python
import logging

def some_method():
    logger = logging.getLogger('rpiplatesrecognition_client.your-custom-name')
    ...
    logger.debug('some message, debug level')
    ...
    logger.warning('another message, warning level')
```

Dont instantiate your `logger` object in global context, like so:
```python
import logging

# this is wrong, won't send data through WebSocket connection
logger = logging.getLogger('rpiplatesrecognition_client.your-custom-name')
# don't do that!
...
```
This because base configuration is done within `rpiplatesrecognition_client.run`.
