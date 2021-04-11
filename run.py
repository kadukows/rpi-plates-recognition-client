import sys
import rpiplatesrecignition_client as client

if len(sys.argv) != 3:
    print('usage: ./run.py server unique_id')
    exit(1)

client.run(sys.argv[1], sys.argv[2])
