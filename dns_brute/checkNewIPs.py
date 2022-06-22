import argparse
import hashlib
from discord_webhook import DiscordWebhook, DiscordEmbed

# Argument parser
parser = argparse.ArgumentParser(description="Check for a new release of IP addresses.")
parser.add_argument(
    "new_ranges",
    type=str,
    help="The path to the new ranges file to process.",
)
parser.add_argument(
    "sha256_file",
    type=str,
    help="The path to the sha256 file of the ranges."
)
parser.add_argument(
    "new_repo_ranges",
    type=str,
    help="The path to the repo ranges to be overwritten."
)
parser.add_argument(
    "discord_webhook_url",
    type=str,
    help="The URL to the Discord Webhook to send alerts to."
)
args = parser.parse_args()

# Open the new ranges file and compute the sha256 hash of it.
new_ranges_file = open(args.new_ranges, "rb").read()
new_ranges_hash = hashlib.sha256(new_ranges_file).hexdigest()

# Check this hash with the previous hash.
current_ranges_hash_file = open(args.sha256_file, "r")
current_ranges_hash = current_ranges_hash_file.read().strip()

print(f"Current ranges hash: {current_ranges_hash}")
print(f"New ranges hash: {new_ranges_hash}")

if new_ranges_hash != current_ranges_hash:
    print("New ranges found!")

    # Replace the latest_sha256.txt file
    current_ranges_hash_file.close()

    overwrite_current_ranges = open(args.sha256_file, 'w')
    overwrite_current_ranges.write(new_ranges_hash)
    overwrite_current_ranges.flush()
    overwrite_current_ranges.close()

    # Write the current ranges to the repo
    overwrite_repo_ranges = open(args.new_repo_ranges, 'wb')
    overwrite_repo_ranges.write(new_ranges_file)
    overwrite_repo_ranges.flush()
    overwrite_repo_ranges.close()

    # Trigger discord webhook
    webhook = DiscordWebhook(url=args.discord_webhook_url, rate_limit_retry=True)
    embed = DiscordEmbed(
            title="Discord Ranges Updated!",
            description=f"Find the newest ranges here: https://github.com/DeadPackets/DiscordIPs/blob/main/dns_brute/latest_ranges.txt",
            color='03b2f8'
    )
    embed.set_author('DiscordIP Bot', url="https://github.com/DeadPackets/DiscordIPs")
    embed.set_footer('Screw VOIP blocking!')
    embed.set_timestamp()
    embed.add_embed_field(name='New Ranges Hash', value=new_ranges_hash)
    embed.add_embed_field(name='Number of IPs', value=str(len(new_ranges_file.decode('utf-8').splitlines())))
    webhook.add_embed(embed)
    webhook.execute()