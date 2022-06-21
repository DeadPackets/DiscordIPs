#!/bin/bash

# Fetch IPs from Shodan
#shodan download discord_media_servers "ssl.cert.subject.cn:*.discord.media" --limit -1
#shodan download discord_voice_servers "ssl.cert.subject.cn:*.discord.gg" --limit -1

# Parse Shodan Output
#cat discord_media_servers.json.gz| gzip -d - | jq -r .ip_str | sort | uniq > media_ips.txt
#cat discord_voice_servers.json.gz| gzip -d - | jq -r .ip_str | sort | uniq > voice_ips.txt

# Generate Discord Domain list
#python generateList.py

# Resolve Discord domains
massdns -r ./resolvers.txt -o S -t A ./discord_domains.txt | grep -i ' A ' | cut -d' ' -f3 | sort | uniq > temp_ips.txt

# Combine all IPs into one text file
cat media_ips.txt voice_ips.txt temp_ips.txt| sort -t . -k 3,3n -k 4,4n > sorted_ips.txt

# Generate the final ranges
cat sorted_ips.txt | awk '{print $0"/32"}' | xargs echo | tr ' ' ',' > discord_ranges.txt

# Generate MD5SUM
md5sum discord_ranges.txt >> ranges_md5.txt
