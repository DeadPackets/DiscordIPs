import re
import requests
import argparse
import tempfile
import subprocess

# Defaults/Globals
REGIONS = {
    "sydney",
    "brazil",
    "us-east",
    "us-central",
    "us-west",
    "russia",
    "india",
    "us-south",
    "hongkong",
    "singapore",
    "southafrica",
    "japan",
    "rotterdam",
}
NUMBER_RANGE = 50000
LINES_WRITTEN = 0

# Argument Parser
parser = argparse.ArgumentParser(description="Fetch the latest Discord IP addresses.")
parser.add_argument(
    "-r",
    "--regions",
    metavar="REGIONS",
    type=str,
    help="A comma seperated list of ranges. Default value is all ranges.",
    default=",".join(REGIONS),
)
parser.add_argument(
    "-i",
    "--range",
    metavar="RANGE",
    type=int,
    help="The number to which to bruteforce DNS names for. Default is 50000",
    default=NUMBER_RANGE,
)
parser.add_argument(
    "-o",
    "--output",
    metavar="FILE",
    type=str,
    help="The file to write the output to. Default is ./resolved_ips_unique.txt",
    default="resolved_ips_unique.txt",
)
args = parser.parse_args()

# Create a temporary folder for results
temp_dir = tempfile.TemporaryDirectory()
print(f"Created temporary directory at: {temp_dir.name}")

# Open the domain list file
domain_list = open(f"{temp_dir.name}/discord_domains.txt", "w")

# Download list of Discord domains
v2ray_domains = requests.get(
    "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/discord"
).text
processed_v2ray_domains = re.findall(r"^[^#].+\..+", v2ray_domains, flags=re.MULTILINE)
print(
    f"Fetched {len(processed_v2ray_domains)} domains from v2fly/domain-list-community."
)

# Filter out the comments and empty lines and write them
[domain_list.write(f"{domain}\n") for domain in processed_v2ray_domains]
LINES_WRITTEN += len(processed_v2ray_domains)

# `*.discord.gg`
for REGION in args.regions.split(","):
    domain_list.writelines(
        "\n".join([f"{REGION}{i}.discord.gg" for i in range(1, args.range)])
    )
    LINES_WRITTEN += args.range
    print(f'Generating *.discord.gg domains for region "{REGION}".')

# Add newline
domain_list.write("\n")

# `*.discord.media`
for REGION in args.regions.split(","):
    domain_list.writelines(
        "\n".join([f"{REGION}{i}.discord.media" for i in range(1, args.range)])
    )
    LINES_WRITTEN += args.range
    print(f'Generating *.discord.media domains for region "{REGION}".')

# Close the file
print(f"Generated a list of {LINES_WRITTEN} potential domains.")
domain_list.flush()
domain_list.close()

# Use cloudflare dns resolver
resolver_list = open(f"{temp_dir.name}/resolvers.txt", "w")
resolver_list.write("1.1.1.1\n")
resolver_list.flush()
resolver_list.close()

# Run massdns to get the resolved IP addresses
print("Running massdns to get the resolved IP addresses...")
massdns_run = subprocess.Popen(
    [
        "massdns",
        "-r",
        f"{temp_dir.name}/resolvers.txt",
        f"{temp_dir.name}/discord_domains.txt",
        "-t",
        "A",
        "-o",
        "S",
        "-w",
        f"{temp_dir.name}/resolved_ips.txt",
        "-q",
    ]
)

# Wait for massdns to finish
massdns_run.communicate()
massdns_run.wait()
print("Massdns run finished.")

# Run the command to extract the resolved IP addresses
filter_output = subprocess.Popen(f"cat {temp_dir.name}/resolved_ips.txt | grep 'A' | cut -d' ' -f3 | grep -E '[0-9]{{1,3}}\.[0-9]{{1,3}}\.[0-9]{{1,3}}\.[0-9]{{1,3}}' | sort -u | uniq > {temp_dir.name}/resolved_ips_unique.txt", shell=True)

# Wait for command to finish
filter_output.communicate()
filter_output.wait()
print("Finished filtering the resolved IP addresses.")

# Open the unique resolved IP addresses file
resolved_ips_unique = open(f"{temp_dir.name}/resolved_ips_unique.txt", "r").read()
print(f"Found {len(resolved_ips_unique.splitlines())} unique resolved IP addresses.")

# Write the unique resolved ip addresses to a file
resolved_ips_unique_file = open(args.output, "w")
resolved_ips_unique_file.write("/32,".join(resolved_ips_unique.splitlines()) + "/32\n")
resolved_ips_unique_file.flush()
resolved_ips_unique_file.close()

# Clean the temporary directory
temp_dir.cleanup()
