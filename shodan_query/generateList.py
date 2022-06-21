import re
import requests

# Open the domain list file
domain_list = open('discord_domains.txt', 'w')

# Download list of Discord domains
v2ray_domains = requests.get('https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/discord').text
processed_v2ray_domains = re.findall(r'^[^#].+\..+', v2ray_domains, flags=re.MULTILINE)
print(f'Fetched {len(processed_v2ray_domains)} domains from v2fly/domain-list-community.')

# Filter out the comments and empty lines and write them
[domain_list.write(f'{domain}\n') for domain in processed_v2ray_domains]
domain_list.flush()
domain_list.close()
