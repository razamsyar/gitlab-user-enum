# GitLab User Enumeration Tool - Enhanced Version

An enhanced Python3 implementation of the GitLab Community Edition user enumeration exploit with improved features and better error handling.

## 📋 Overview

This tool automates the process of enumerating valid usernames on GitLab CE instances by analyzing HTTP response codes. It's an improved version of the original bash script with additional features like output file support, verbosity modes, and progress tracking.

**Original Exploit:** [Exploit-DB #49821](https://www.exploit-db.com/exploits/49821) by [@4D0niiS](https://github.com/4D0niiS)  
**Enhanced by:** sqlj3d1

## ✨ Features

- ✅ **Output File Support** - Save valid usernames to a file for later use
- ✅ **Verbosity Modes** - Quiet, normal, and verbose output options
- ✅ **Progress Tracking** - Real-time progress indicator during enumeration
- ✅ **Graceful Signal Handling** - Properly handles Ctrl+C interruption with statistics
- ✅ **Better Status Code Handling** - Detailed analysis of HTTP response codes
- ✅ **Error Handling** - Comprehensive error handling for network issues
- ✅ **Color-coded Output** - Easy-to-read terminal output with color indicators
- ✅ **Type Hints** - Modern Python3 code with type annotations

## 🔧 Requirements

- Python 3.6+
- requests library

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/gitlab-user-enum.git
cd gitlab-user-enum

# Install dependencies
pip3 install -r requirements.txt

# Make the script executable (optional)
chmod +x gitlab_enum.py
```

**requirements.txt:**
```
requests>=2.25.0
```

## 🚀 Usage

### Basic Usage

```bash
python3 gitlab_enum.py -u <TARGET_URL> -w <WORDLIST>
```

### Command-line Options

```
Required Arguments:
  -u, --url URL          Target GitLab instance URL
  -w, --wordlist FILE    Path to username wordlist file

Optional Arguments:
  -o, --output FILE      Save valid usernames to file
  -q, --quiet            Quiet mode (only show found users)
  -v, --verbose          Verbose mode (show all HTTP codes)
  -h, --help             Show help message and exit
```

## 📚 Examples

### Basic Enumeration
```bash
python3 gitlab_enum.py -u http://gitlab.local -w usernames.txt
```

### Save Results to File
```bash
python3 gitlab_enum.py -u http://gitlab.local -w usernames.txt -o valid_users.txt
```

### Quiet Mode (Only Show Found Users)
```bash
python3 gitlab_enum.py -u http://gitlab.local -w usernames.txt --quiet
```

### Verbose Mode (Show All HTTP Response Codes)
```bash
python3 gitlab_enum.py -u http://gitlab.local -w usernames.txt --verbose
```

### HTTPS Target with Output File
```bash
python3 gitlab_enum.py -u https://gitlab.example.com -w /usr/share/wordlists/usernames.txt -o results.txt
```

## 🎯 HTTP Response Code Analysis

The tool analyzes various HTTP status codes:

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 200 | User exists | ✅ Reported as valid user |
| 404 | User not found | ❌ Skipped (shown in verbose mode) |
| 301/302 | Redirect | ⚠️ Potential authentication issue |
| 403 | Forbidden | ⚠️ Access denied |
| 500/502/503 | Server error | ⚠️ Target may be misconfigured |

## 📊 Output Example

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║        GitLab CE User Enumeration Tool - Enhanced Version                ║
║                                                                           ║
║        Original: @4D0niiS (Exploit-DB #49821)                            ║
║        Enhanced by: sqlj3d1                                               ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

[*] Purpose: Identify valid usernames on GitLab CE instances
[*] Original: https://www.exploit-db.com/exploits/49821
[*] Improvements: Output file support, verbosity modes, progress tracking
[!] Warning: Unauthorized access is illegal - use responsibly

[i] Loading wordlist...
[i] Total usernames to test: 100
[i] Output file: valid_users.txt

[+] Valid user: admin (HTTP 200)
[+] Valid user: root (HTTP 200)
[+] Valid user: developer (HTTP 200)

==================================================
Enumeration Complete
==================================================
[i] Usernames tested: 100
[i] Valid users found: 3
[i] Results saved to: valid_users.txt
```

## ⚠️ Legal Disclaimer

This tool is provided for **educational and authorized security testing purposes only**. 

**Important:**
- ❌ **DO NOT** run this tool against GitLab.com
- ❌ **DO NOT** use this tool on systems you don't own or have explicit permission to test
- ✅ Only use on systems where you have **written authorization**
- ✅ Intended for penetration testers, security researchers, and CTF challenges

Unauthorized access to computer systems is illegal. The author assumes no liability for misuse of this tool.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Credits

- **Original Author:** [@4D0niiS](https://github.com/4D0niiS)
- **Original Exploit:** [Exploit-DB #49821](https://www.exploit-db.com/exploits/49821)
- **Enhanced Version:** sqlj3d1

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 References

- [Original Exploit on Exploit-DB](https://www.exploit-db.com/exploits/49821)
- [GitLab Security](https://about.gitlab.com/security/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

## 📧 Contact

For questions or suggestions, feel free to open an issue on GitHub.

---

**Remember:** Always practice responsible disclosure and ethical hacking! 🛡️
