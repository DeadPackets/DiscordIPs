import re
import requests

REGIONS = {'sydney', 'brazil', 'us-east', 'us-central', 'us-west', 'russia', 'india', 'us-south', 'hongkong', 'singapore', 'southafrica', 'japan', 'rotterdam'}
NUMBER_RANGE = 10500

# Open the domain list file
domain_list = open('discord_domains.txt', 'w')

# Download list of Discord domains
v2ray_domains = requests.get('https://raw.githubusercontent.com/v2ray/domain-list-community/master/data/discord').text

# Filter out the comments and empty lines and write them
[domain_list.write(f'{domain}\n') for domain in re.findall(r'^[^#].+\..+', v2ray_domains, flags=re.MULTILINE)]

# `*.discord.gg`
for REGION in REGIONS:
    domain_list.writelines('\n'.join([f'{REGION}{i}.discord.gg' for i in range(NUMBER_RANGE)]))

# `*.discord.media`
for REGION in REGIONS:
    domain_list.writelines('\n'.join([f'{REGION}{i}.discord.media' for i in range(NUMBER_RANGE)]))

# Close the file
domain_list.flush()
domain_list.close()