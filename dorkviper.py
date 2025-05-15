#!/usr/bin/env python3
"""
DorkViper - Interactive Dorking Assistant
Developed by Quasar CyberTech Research Team

A professional-grade tool for ethical security research and OSINT.
"""

import webbrowser
import sys
import os
import questionary
from questionary import Style

# ASCII Art Banner
BANNER = """
██████╗  ██████╗ ██████╗ ██╗  ██╗██╗   ██╗██╗██████╗ ███████╗██████╗ 
██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██║   ██║██║██╔══██╗██╔════╝██╔══██╗
██║  ██║██║   ██║██████╔╝█████╔╝ ██║   ██║██║██████╔╝█████╗  ██████╔╝
██║  ██║██║   ██║██╔══██╗██╔═██╗ ╚██╗ ██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝██║  ██║██║  ██╗ ╚████╔╝ ██║██║     ███████╗██║  ██║
╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                      
Interactive Dorking Assistant | Quasar CyberTech Research Team
For ethical security research and OSINT purposes only
"""

# Custom style for questionary
custom_style = Style([
    ('qmark', 'fg:green bold'),
    ('question', 'fg:white bold'),
    ('answer', 'fg:green bold'),
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:green bold'),
    ('selected', 'fg:cyan bold'),
    ('separator', 'fg:cyan'),
    ('instruction', 'fg:white'),
    ('text', 'fg:white'),
    ('disabled', 'fg:gray'),
])

# Search engine base URLs
SEARCH_ENGINES = {
    "Google": "https://www.google.com/search?q=",
    "Bing": "https://www.bing.com/search?q=",
    "DuckDuckGo": "https://duckduckgo.com/?q=",
    "Yandex": "https://yandex.com/search/?text=",
    "Baidu": "https://www.baidu.com/s?wd=",
    "Shodan": "https://www.shodan.io/search?query="
}

# Dork categories and their queries
DORK_CATEGORIES = {
    "Login Portals": {
        "Admin Panels": 'intitle:"admin" OR intitle:"administrator" OR intitle:"login" OR intitle:"cpanel"',
        "Login Pages": 'inurl:login OR inurl:signin OR inurl:auth',
        "Control Panels": 'intitle:"control panel" OR intitle:"dashboard"'
    },
    "Sensitive Files": {
        "Configuration Files": 'ext:xml OR ext:conf OR ext:cnf OR ext:reg OR ext:inf OR ext:rdp OR ext:cfg OR ext:txt OR ext:ora OR ext:ini',
        "Database Files": 'ext:sql OR ext:dbf OR ext:mdb OR ext:db',
        "Backup Files": 'ext:bkf OR ext:bkp OR ext:bak OR ext:old OR ext:backup',
        "Log Files": 'ext:log OR inurl:log'
    },
    "Exposed Information": {
        "Directory Listings": 'intitle:"index of" OR intitle:"directory listing"',
        "Exposed Documents": 'ext:doc OR ext:docx OR ext:odt OR ext:pdf OR ext:rtf OR ext:sxw OR ext:psw OR ext:ppt OR ext:pptx OR ext:pps OR ext:csv',
        "API Keys & Tokens": 'intext:"api_key" OR intext:"api key" OR intext:"apikey" OR intext:"client_secret" OR intext:"client_id"',
        "Email Lists": 'filetype:xls OR filetype:xlsx intext:"email" OR intext:"e-mail" OR intext:"phone" OR intext:"contact"'
    },
    "Vulnerable Pages": {
        "SQL Injection Potential": 'inurl:php?id= OR inurl:asp?id= OR inurl:jsp?id=',
        "XSS Potential": 'inurl:search= OR inurl:query= OR inurl:q= OR inurl:s=',
        "File Inclusion": 'inurl:include OR inurl:require OR inurl:inc OR inurl:path='
    },
    "Server Information": {
        "Server Status Pages": 'intitle:"Apache Status" OR intitle:"nginx status" OR intitle:"server status"',
        "phpMyAdmin": 'intitle:"phpMyAdmin" OR inurl:phpmyadmin',
        "Server Technologies": 'intitle:"Test Page for" OR "Default Web Page"'
    },
    "Custom Dork": {
        "Custom Query": "custom"
    }
}

def clear_screen():
    """Clear the terminal screen based on OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print the DorkViper banner."""
    clear_screen()
    print("\033[94m" + BANNER + "\033[0m")

def select_search_engine():
    """Prompt user to select a search engine."""
    return questionary.select(
        "Select a search engine:",
        choices=list(SEARCH_ENGINES.keys()),
        style=custom_style
    ).ask()

def select_dork_category():
    """Prompt user to select a dork category."""
    return questionary.select(
        "Select a dork category:",
        choices=list(DORK_CATEGORIES.keys()),
        style=custom_style
    ).ask()

def select_dork_type(category):
    """Prompt user to select a specific dork type within the chosen category."""
    return questionary.select(
        f"Select a {category} dork type:",
        choices=list(DORK_CATEGORIES[category].keys()),
        style=custom_style
    ).ask()

def get_custom_dork():
    """Prompt user to enter a custom dork query."""
    return questionary.text(
        "Enter your custom dork query:",
        validate=lambda text: len(text) > 0,
        style=custom_style
    ).ask()

def get_target_domain():
    """Prompt user to optionally specify a target domain."""
    has_domain = questionary.confirm(
        "Do you want to specify a target domain?",
        default=False,
        style=custom_style
    ).ask()
    
    if has_domain:
        return questionary.text(
            "Enter the target domain (e.g., example.com):",
            validate=lambda text: len(text) > 0,
            style=custom_style
        ).ask()
    return None

def execute_dork(search_engine, dork_query, domain=None):
    """Execute the dork by opening the browser with the crafted query."""
    base_url = SEARCH_ENGINES[search_engine]
    
    # Add domain restriction if specified
    if domain:
        dork_query = f"{dork_query} site:{domain}"
    
    # Construct the full URL
    full_url = f"{base_url}{dork_query.replace(' ', '+')}"
    
    print(f"\n\033[92m[+] Executing dork query in {search_engine}...\033[0m")
    print(f"\033[93m[*] Query: {dork_query}\033[0m")
    
    try:
        # Open the URL in the default browser
        webbrowser.open(full_url)
        print(f"\033[92m[✓] Browser launched successfully!\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Error opening browser: {str(e)}\033[0m")
        return False
    
    return True

def main():
    """Main function to run the DorkViper tool."""
    try:
        print_banner()
        
        # Display disclaimer
        print("\033[91m" + "=" * 80 + "\033[0m")
        print("\033[91m[!] DISCLAIMER: This tool is for ethical security research ONLY.\033[0m")
        print("\033[91m[!] Unauthorized use against systems you don't own is illegal.\033[0m")
        print("\033[91m[!] The developers are not responsible for any misuse.\033[0m")
        print("\033[91m" + "=" * 80 + "\033[0m\n")
        
        # Get user confirmation to proceed
        proceed = questionary.confirm(
            "Do you understand and agree to use this tool ethically?",
            default=False,
            style=custom_style
        ).ask()
        
        if not proceed:
            print("\n\033[91m[!] Tool execution aborted by user.\033[0m")
            sys.exit(0)
        
        # Select search engine
        search_engine = select_search_engine()
        if not search_engine:
            print("\n\033[91m[!] No search engine selected. Exiting...\033[0m")
            sys.exit(0)
        
        # Select dork category
        dork_category = select_dork_category()
        if not dork_category:
            print("\n\033[91m[!] No dork category selected. Exiting...\033[0m")
            sys.exit(0)
        
        # Select specific dork type
        dork_type = select_dork_type(dork_category)
        if not dork_type:
            print("\n\033[91m[!] No dork type selected. Exiting...\033[0m")
            sys.exit(0)
        
        # Get the dork query
        if dork_type == "Custom Query":
            dork_query = get_custom_dork()
        else:
            dork_query = DORK_CATEGORIES[dork_category][dork_type]
        
        # Optionally specify a target domain
        target_domain = get_target_domain()
        
        # Execute the dork
        success = execute_dork(search_engine, dork_query, target_domain)
        
        if success:
            print("\n\033[92m[✓] DorkViper execution completed successfully!\033[0m")
        else:
            print("\n\033[91m[!] DorkViper execution failed.\033[0m")
        
        # Ask if user wants to run another dork
        another = questionary.confirm(
            "Do you want to run another dork?",
            default=True,
            style=custom_style
        ).ask()
        
        if another:
            main()  # Recursive call to start over
        else:
            print("\n\033[94m[*] Thank you for using DorkViper!\033[0m")
    
    except KeyboardInterrupt:
        print("\n\033[91m[!] Tool execution interrupted by user.\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91m[!] An unexpected error occurred: {str(e)}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    # Check if questionary is installed
    try:
        import questionary
    except ImportError:
        print("\033[91m[!] questionary is not installed. Installing required packages...\033[0m")
        os.system('pip install questionary')
        print("\033[92m[✓] Dependencies installed successfully!\033[0m")
    
    main()
