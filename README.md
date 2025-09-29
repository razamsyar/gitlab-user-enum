# GitLab User Enumeration Tool

Enhanced Python3 version of GitLab CE user enumeration with improved features.

**Original Exploit:** [Exploit-DB #49821](https://www.exploit-db.com/exploits/49821) by [@4D0niiS](https://github.com/4D0niiS)  
**Enhanced by:** sqlj3d1

## Features

- Output file support to save valid usernames
- Quiet and verbose modes
- Progress tracking
- Better error handling
- Color-coded output

## Installation

```bash
git clone https://github.com/yourusername/gitlab-user-enum.git
cd gitlab-user-enum
pip3 install -r requirements.txt
```

## Usage

```bash
# Basic usage
python3 gitlab_user_enum.py -u http://gitlab.local -w usernames.txt

# Save results to file
python3 gitlab_user_enum.py -u http://gitlab.local -w usernames.txt -o valid_users.txt

# Quiet mode (only show found users)
python3 gitlab_user_enum.py -u http://gitlab.local -w usernames.txt -q

# Verbose mode (show all HTTP codes)
python3 gitlab_user_enum.py -u http://gitlab.local -w usernames.txt -v
```

## Options

```
-u, --url          Target GitLab URL (required)
-w, --wordlist     Username wordlist file (required)
-o, --output       Save valid usernames to file
-q, --quiet        Only show found users
-v, --verbose      Show all HTTP response codes
-h, --help         Show help message
```

## Disclaimer

⚠️ **For authorized security testing only.**

- DO NOT use against GitLab.com
- Only use on systems you own or have written permission to test
- Unauthorized access is illegal

## License

MIT License - see LICENSE file for details.

## Credits

- Original: [@4D0niiS](https://github.com/4D0niiS) - [Exploit-DB #49821](https://www.exploit-db.com/exploits/49821)
- Enhanced: sqlj3d1
