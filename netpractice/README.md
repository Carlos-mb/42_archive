*This project has been created as part of the 42 curriculum by cmelero-.*

# NetPractice

## Description

NetPractice is a practical networking project from the 42 curriculum.

The goal of this project is to learn and practice the basics of computer networking by fixing simulated network configurations. Each level contains a non-working network diagram, and the objective is to make the network functional by correctly configuring IP addresses, subnet masks, routes and gateways.

The project is composed of 10 levels. For each level, the correct configuration must be validated in the NetPractice interface and exported using the `Get my config` button.

This project focuses on the following networking concepts:

- TCP/IP addressing
- IPv4 addresses
- Subnet masks
- CIDR notation
- Network addresses
- Broadcast addresses
- Valid host ranges
- Default gateways
- Routers
- Switches
- Static routes
- Packet forwarding
- Basic OSI model concepts, especially Layer 2 and Layer 3

## Instructions

### Running the training interface

Download the NetPractice archive from the project page and extract it into a local directory.

From that directory, run:

```sh
./run.sh
```

This script starts a local web server and opens the NetPractice interface in the web browser.

If `run.sh` does not work, the interface can be started manually with Python:

```sh
python3 -m http.server 49242
```

Then open the following URL in a web browser:

```text
http://localhost:49242
```

A different port may be used if necessary.

### Using the interface

In the NetPractice interface:

1. Enter the 42 login:

```text
cmelero-
```

2. Start the training levels.
3. Read the objectives shown at the top of each level.
4. Inspect the network diagram.
5. Modify only the editable fields.
6. Use the `Check again` button to validate the configuration.
7. Once the level is correct, use the `Get my config` button to export the configuration file.
8. Repeat the process for all 10 levels.

The logs displayed at the bottom of the interface are useful to understand configuration errors, such as:

- Invalid IP address
- Incorrect subnet mask
- Missing gateway
- Missing route
- Destination not reachable
- Route not matching any interface

### Submission requirements

The repository must contain 10 exported configuration files, one for each level.

All exported configuration files must be placed at the root of the Git repository.

Example repository layout:

```text
.
├── README.md
├── cmelero-1.txt
├── cmelero-2.txt
├── cmelero-3.txt
├── cmelero-4.txt
├── cmelero-5.txt
├── cmelero-6.txt
├── cmelero-7.txt
├── cmelero-8.txt
├── cmelero-9.txt
└── cmelero-10.txt
```

The exact filenames must be the ones exported by the NetPractice interface.

Only the files present in the Git repository will be evaluated.

During the defense, three random levels must be solved again within the limited time allowed by the evaluation platform. External tools are not allowed during the evaluation. A simple calculator such as `bc` is tolerated.

## Resources

### Networking concepts studied

I have not studied for this exercise. I already am network administrator.

### References

The following references are useful for understanding the concepts required by this project:

- RFC 791: Internet Protocol
- RFC 950: Internet Standard Subnetting Procedure
- Cisco documentation about IP addressing and subnetting
- Documentation about IPv4 subnetting and CIDR notation
- Documentation about routers, switches and default gateways
- Documentation about the OSI model
- Practical subnetting exercises

### Use of AI

Specifically, AI was used to:

- Create the README blueprint.
