import ipaddress
from cidrize import cidrize

# Process the output file and turn it into a set, eliminating duplicates
massdns_output = open('resolved_domains.txt', 'r').read().split('\n')
resolved_domains = set([ipaddress.ip_address(line.split(' ')[2]) for line in massdns_output if len(line.split(' ')) == 3 and 'com' not in line])
print(f'Resolved IP addresses: {len(massdns_output)}')
print(f'Unique IP addresses: {len(resolved_domains)}')

# Sort the IP addresses
sorted_ips = sorted(resolved_domains)

# Loop through the sorted IPs to find sequential IPs to hopefully turn into CIDRs
temp_ip = None
count = 0
ip_ranges = set()
for ip in sorted_ips:
    # Check if we already are tracking a starting IP
    if temp_ip:
        # Check if this IP is following the previous
        if int(str(ip).split('.')[-1]) == (int(str(temp_ip[count]).split('.')[-1]) + 1):
            # It is following, so increment count
            count += 1
            temp_ip.append(ip)
        else:
            # Just a quick check if we only have 1 IP
            if len(temp_ip) == 1:
                ip_ranges.update(cidrize(str(temp_ip[0]), strict=True))
            else:
                ip_ranges.update(cidrize(f'{str(temp_ip[0])}-{str(temp_ip[-1]).split(".")[-1]}', strict=True))

            # It is no longer following, so reset count and save group
            count = 0

            # Reset the tracked IPs
            temp_ip = [ip,]
    else:
        temp_ip = [ip,]

# Now we have a list of CIDRs, transform them into comma seperated format
output_ranges = ','.join([str(ip_range) for ip_range in ip_ranges])
print(f'Generated {len(ip_ranges)} CIDRs.')

# Open the output file
output_file = open('discord_ranges.txt', 'w')

# Write to it
output_file.write(output_ranges)

# Flush and close
output_file.flush()
output_file.close()