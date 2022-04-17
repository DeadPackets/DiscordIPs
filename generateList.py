import re
import requests

REGIONS = {'sydney', 'brazil', 'us-east', 'us-central', 'us-west', 'russia', 'india', 'us-south', 'hongkong', 'singapore', 'southafrica', 'japan', 'rotterdam'}
NUMBER_RANGE = 50000
LINES_WRITTEN = 0

# Open the domain list file
domain_list = open('discord_domains.txt', 'w')

# Download list of Discord domains
v2ray_domains = requests.get('https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/discord').text
processed_v2ray_domains = re.findall(r'^[^#].+\..+', v2ray_domains, flags=re.MULTILINE)
print(f'Fetched {len(processed_v2ray_domains)} domains from v2fly/domain-list-community.')

# Filter out the comments and empty lines and write them
[domain_list.write(f'{domain}\n') for domain in processed_v2ray_domains]
LINES_WRITTEN += len(processed_v2ray_domains)

# `*.discord.gg`
for REGION in REGIONS:
    domain_list.writelines('\n'.join([f'{REGION}{i}.discord.gg' for i in range(NUMBER_RANGE)]))
    LINES_WRITTEN += NUMBER_RANGE
    print(f'Generating *.discord.gg domains for region "{REGION}".')

# `*.discord.media`
for REGION in REGIONS:
    domain_list.writelines('\n'.join([f'{REGION}{i}.discord.media' for i in range(NUMBER_RANGE)]))
    LINES_WRITTEN += NUMBER_RANGE
    print(f'Generating *.discord.media domains for region "{REGION}".')

# Close the file
print(f'Generated a list of {LINES_WRITTEN} potential domains.')
domain_list.flush()
domain_list.close()
