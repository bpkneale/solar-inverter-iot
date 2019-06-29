# solar-inverter-iot
IoT client for solar inverters

Uses AWS IoT core to publish solar data into the cloud

By default, searches a local directory "secrets" for the private key, root CA and local cert to connect to AWS. Also need a file aws.json for configuring thing name and endpoint.
