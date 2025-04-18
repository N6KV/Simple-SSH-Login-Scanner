# Simple SSH login scanner -- <-N6KV->
import os # For checking file existence
import subprocess # For running shell commands
import re # For extracting usernames and ips
import ipaddress # For checking if ip is ipv4 or ipv6
import argparse # For asking the user how many lines to scan (from journalctl logs)
import time # For outputting how long it took to run the script
import sys # See below
import atexit # For printing the banner at the end of the script


def scan_logins(limit): # Scan logins from auth.log
    log_path = "/var/log/auth.log" # Default path for auth.log (old way)
    print("\033[33m[*]\033[0m Attempting to read auth.log...")
    print("^" * 50) # Separator for readability

    try: # Try to read auth.log
        with open(log_path, "r") as log_file:  # Open auth.log file

            lines = log_file.readlines() # Read all the lines
            failed = [line for line in lines if "Failed password" in line] # Filter for failed login attempts

            for line in failed[-limit:]: # Print only the last 'limit' lines (100 if not specified)
                print("\033[31m[!]\033[0m Failed login detected in auth.log file:")
                parse_failed_login(line) # Parse the line to extract username and ip
                print("-" * 50)  # Separating each failed login (for readability)

            if not failed: # If no failed logins were found
                print("\033[33m[*]\033[0m No failed login attempts found in auth.log.")

    except PermissionError: # If permission is denied (e.g. not running as root or with sudo)
        print(f"\033[31m[!]\033[0m Insufficient permissions to read auth.log at {log_path}. Please run as root / with sudo.")
    except Exception as e: # Catch any other errors
        print(f"\033[31m[!]\033[0m Failed to read {log_path}: {e}")
        print("\033[33m[*]\033[0m Falling back to journalctl...")
        scan_journalctl_logins(limit) # Check jorunalctl logs because auth.log is not accessible for whatever reason ¯\_('_')_/¯


def scan_journalctl_logins(limit, read_all=False): # Scan logins from journalctl (new way)
    print("\033[33m[*]\033[0m Attempting to read journalctl logs...")
    print("^" * 50) # Separator for readability

    try: # Try to read journalctl logs
        cmd = ["journalctl", "-u", "ssh", "--no-pager"] # Read journalctl logs for ssh service
        if not read_all: # If read_all isn't set, then read the last 500 lines
            cmd += ["-n", "500"]  # default chunk
        result = subprocess.run(cmd, capture_output=True, text=True) # Run it and capture the output
        lines = result.stdout.split("\n") # Split the output into lines

        # Filter failed logins
        failed_logins = [line for line in lines if "Failed password" in line]
        if not failed_logins: # If no failed logins were found
            print("\033[33m[*]\033[0m No failed login attempts found in journalctl logs.") # print it
            return

        # Show only the last {limit} entries
        for line in failed_logins[-limit:]:
            print("\033[31m[!]\033[0m Failed login detected in journalctl logs:") # Print it
            parse_failed_login(line) # Parse the line to extract username and ip
            print("-" * 50) # Separating each failed login (for readability)

    except Exception as e: # Catch any errors
        print(f"\033[31m[!]\033[0m Failed to read journalctl logs: {e}")

def parse_failed_login(line): # Extract username and ip from the line
    username_patterns = [
        r"invalid user (\S+)", # Regex pattern for invalid username
        r"Failed password for (\S+)" # Regex pattern for username in general
    ]
    ip_pattern = r"from (\S+)" # Regex pattern for ip

    username = None # Initialize username
    for pattern in username_patterns: # Check each pattern for username
        match = re.search(pattern, line)
        if match: # If a match is found, extract the username into {username}
            username = match.group(1)
            break

    ip_match = re.search(ip_pattern, line) # Search for ip in the line

    if username: # If username was found
        print(f"\033[32m->\033[0m Username: {username}")
    if ip_match: # If ip was found
        ip = ip_match.group(1)
        try: # Check if ip is ipv4 or ipv6
            ip_obj = ipaddress.ip_address(ip)
            ip_type = "IPv6" if ip_obj.version == 6 else "IPv4"
        except ValueError: # If ip is not valid
            ip_type = "Invalid IP"

        if ip == "127.0.0.1" or ip == "::1": # Check if ip is localhost
            print(f"\033[32m->\033[0m IP Address: {ip} ({ip_type} - Localhost)") # If yes, print it
        else:
            print(f"\033[32m->\033[0m IP Address: {ip} ({ip_type})") # If not, then not ;)
    print(f"\033[32m->\033[0m Timestamp: {line.split()[0]} {line.split()[1]} {line.split()[2]}") # Print the timestamp

def printbanner(): # Print the banner (ending the timer and print it)
    end_time = time.time() # End the timer
    elapsed_time = end_time - start_time # Calculate the elapsed time
    print(f"\033[33m[*]\033[0m Script finished in {elapsed_time:.2f} seconds.") # Print the elapsed time
    print("-" * 50) # Separator for readability

if __name__ == "__main__": # Main function
    start_time = time.time() # Start the timer
    atexit.register(printbanner) # Register the printbanner function to be called at exit

    parser = argparse.ArgumentParser(description="Simple SSH login scanner.")
    parser.add_argument("--limit", type=int, default=100, help="How many failed logins to show (default: 100)")
    parser.add_argument("--all", action="store_true", help="Read all journalctl logs instead of only the last 500 lines")
    args = parser.parse_args() # Parse the arguments

    if args.all: # If the --all flag is set, ask for confirmation
        print("\033[33m[*]\033[0m You used the \033[3m--all\033[0m flag, which reads the entire log instead of just the last 500 lines.")
        print("\033[33m[*]\033[0m Depending on your server's size and popularity, this may load a large amount of data and take time.")
        confirm = input("\033[34m[?]\033[0m Are you sure you want to continue? (y/N): ").strip().lower()
        if confirm != "y": # If the user doesn't confirm
            print("\033[31m[!]\033[0m Aborted by user.")
            print("-" * 50) # Separator for readability
            sys.exit(0) # Exit the script -the fancy way-

    if os.path.exists("/var/log/auth.log"): # Check if auth.log exists, if yes
        scan_logins(args.limit) # scan it
    else: # else
        print(f"\033[33m[*]\033[0m /var/log/auth.log not found. Checking journalctl logs...") # Print that it doesnt exist and then
        scan_journalctl_logins(args.limit, args.all) # check journalctl logs
