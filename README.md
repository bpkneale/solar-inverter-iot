# solar-inverter-iot
IoT client for solar inverters

Uses AWS IoT core to publish solar data into the cloud

By default, searches a local directory "conf" for the configuration, private key, root CA and local cert to connect 
to AWS.

## Docker
Public repo: docker.io/bpkneale/solar-inverter-iot

Needs a volume argument:

`-v /some/local/vol:/usr/src/conf`

For specifying the configuration folder described above. 