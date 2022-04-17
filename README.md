# DiscordIPs

A set of Python scripts (and a Github Action!) to curate a list of IP ranges that belong to Discord or run Discord services to be used with applications such as WireGuard.

## What We Know

- `*.discord.gg`: All the Voice Chat servers of Discord
- `*.discord.media`: All the streaming/video servers of Discord
- Currently, the following Discord regions exist:
  - `sydney`
  - `brazil`
  - `us-east`
  - `us-central`
  - `us-west`
  - `us-south`
  - `russia`
  - `india`
  - `hongkong`
  - `singapore`
  - `southafrica`
  - `japan`
  - `rotterdam`
- You can find a list of updated Discord-related domains [here](https://github.com/v2fly/domain-list-community/blob/master/data/discord)

## How It Works

The following steps take place inside the scripts included in this repository:

1. `generateList.py`: Generate a list for each region (for example, `sydney`) of possible sub-domains for both `discord.gg` and `discord.media` domains following the format `<REGION><NUMBER>.discord.(gg/media)`.
2. `generateList.py`: Fetch and parse the latest domain from [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community/blob/master/data/discord).
3. Run `massdns` with a list of resolvers from [here](https://github.com/janmasarik/resolvers) and save the results to a file.
4. `processOutput.py`: Process the output of `massdns` to get a unique list of sorted IPs, then use [cidrize](https://pypi.org/project/cidrize/) to condense the IPs into CIDRs.
5. ???
6. Profit!

## TODOs

[X] Add documentation to README
[X] Add more output to python scripts
[X] Create requirements.txt
[ ] Create Github Action to automatically run everything
[ ] Add customization to python scripts based on command-line arguments
