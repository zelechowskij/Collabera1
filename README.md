# This is a task for Collabera recruitment

get_mac_addr.py is a script that takes MAC address as a positional argument, and returns a manufacturer name that is associated with that MAC address.

# How to use it

## Requirements
- Docker
- Git

## Steps to run this script in a Docker enviroinment
1. Clone the repository <br />
```git clone https://github.com/zelechowskij/Collabera1.git && cd Collabera1```<br />
2. **Place your API key in secret.json and save the file**<br />
3. Build an image <br />
```docker build -t getMacAddr:1.0 .```
4. Run the docker image <br />
```docker run getMacAddr:1.0 <MAC_ADDRESS>```
