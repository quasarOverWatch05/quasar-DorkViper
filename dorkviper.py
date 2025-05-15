import os
import sys
import webbrowser
import time
import random
from urllib.parse import quote_plus

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear the terminal screen based on OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display the DorkViper banner."""
    banner = f"""
    {Colors.GREEN}
    ██████╗  ██████╗ ██████╗ ██╗  ██╗██╗   ██╗██╗██████╗ ███████╗██████╗ 
    ██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██║   ██║██║██╔══██╗██╔════╝██╔══██╗
    ██║  ██║██║   ██║██████╔╝█████╔╝ ██║   ██║██║██████╔╝█████╗  ██████╔╝
    ██║  ██║██║   ██║██╔══██╗██╔═██╗ ╚██╗ ██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗
    ██████╔╝╚██████╔╝██║  ██║██║  ██╗ ╚████╔╝ ██║██║     ███████╗██║  ██║
    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
    {Colors.ENDC}
    {Colors.BOLD}{Colors.GREEN}[ DorkViper v1.0 - Interactive Google Dorking Tool ]{Colors.ENDC}
    {Colors.WARNING}[ Developed by Quasar CyberTech Research Team ]{Colors.ENDC}
    {Colors.FAIL}[ For ethical security research only ]{Colors.ENDC}
    """
    print(banner)

def print_disclaimer():
    """Display the legal disclaimer."""
    disclaimer = f"""
    {Colors.BOLD}{Colors.WARNING}LEGAL DISCLAIMER:{Colors.ENDC}
    {Colors.WARNING}This tool is provided for educational and ethical security research purposes only.
    Misuse of this tool may violate laws, regulations, or terms of service.
    The authors are not responsible for any direct or indirect damage caused by
    the misuse of this tool. Always ensure you have proper authorization before
    conducting security assessments on any target.{Colors.ENDC}
    """
    print(disclaimer)
    input(f"\n{Colors.BOLD}Press Enter to acknowledge and continue...{Colors.ENDC}")

def get_dork_categories():
    """Return a dictionary of dork categories and their corresponding queries."""
    return {
        "1": {
            "name": "Login Pages",
            "query": "intitle:\"login\" OR inurl:\"login\" OR intext:\"username\" OR intext:\"password\" site:{}"
        },
        "2": {
            "name": "Sensitive Directories",
            "query": "intitle:\"index of\" OR intitle:\"directory listing\" site:{}"
        },
        "3": {
            "name": "Configuration Files",
            "query": "ext:xml OR ext:conf OR ext:cnf OR ext:reg OR ext:inf OR ext:rdp OR ext:cfg OR ext:txt OR ext:ora OR ext:ini site:{}"
        },
        "4": {
            "name": "Database Files",
            "query": "ext:sql OR ext:dbf OR ext:mdb OR ext:db site:{}"
        },
        "5": {
            "name": "Backup Files",
            "query": "ext:bkf OR ext:bkp OR ext:bak OR ext:old OR ext:backup site:{}"
        },
        "6": {
            "name": "Exposed Documents",
            "query": "ext:doc OR ext:docx OR ext:odt OR ext:pdf OR ext:rtf OR ext:sxw OR ext:psw OR ext:ppt OR ext:pptx OR ext:pps OR ext:csv site:{}"
        },
        "7": {
            "name": "WordPress Files",
            "query": "inurl:wp-content OR inurl:wp-includes site:{}"
        },
        "8": {
            "name": "Log Files",
            "query": "ext:log OR inurl:log site:{}"
        },
        "9": {
            "name": "Finding Subdomains",
            "query": "site:*.{}"
        },
        "10": {
            "name": "Open FTP Servers",
            "query": "intitle:\"index of\" inurl:ftp site:{}"
        },
        "11": {
            "name": "Web Server Detection",
            "query": "intitle:\"test page for\" \"Apache HTTP Server\" site:{}"
        },
        "12": {
            "name": "phpMyAdmin",
            "query": "intitle:\"phpMyAdmin\" inurl:\"phpMyAdmin\" site:{}"
        },
        "13": {
            "name": "Vulnerable Parameters",
            "query": "inurl:php?id= OR inurl:category.php?id= OR inurl:news.php?id= site:{}"
        },
        "14": {
            "name": "Error Messages",
            "query": "\"Warning:\" \"error on line\" site:{}"
        },
        "15": {
            "name": "Network Devices",
            "query": "intitle:\"Router Configuration\" OR intext:\"Cisco\" site:{}"
        }
    }

def get_target_domain():
    """Get and validate the target domain from user input."""
    while True:
        target = input(f"\n{Colors.BOLD}Enter target domain (e.g., example.com):{Colors.ENDC} ").strip()
        if target and "." in target and " " not in target:
            return target
        print(f"{Colors.FAIL}Invalid domain format. Please try again.{Colors.ENDC}")

def select_dork_category(categories):
    """Let the user select a dork category."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}Available Google Dork Categories:{Colors.ENDC}")
    
    for key, category in categories.items():
        print(f"{Colors.CYAN}[{key}] {category['name']}{Colors.ENDC}")
    
    while True:
        choice = input(f"\n{Colors.BOLD}Select a category (1-{len(categories)}):{Colors.ENDC} ").strip()
        if choice in categories:
            return choice
        print(f"{Colors.FAIL}Invalid choice. Please select a number between 1 and {len(categories)}.{Colors.ENDC}")

def execute_dork(domain, category_data):
    """Execute the selected Google dork by opening a browser."""
    query = category_data["query"].format(domain)
    encoded_query = quote_plus(query)
    search_url = f"https://www.google.com/search?q={encoded_query}"
    
    print(f"\n{Colors.GREEN}Executing dork: {category_data['name']}{Colors.ENDC}")
    print(f"{Colors.BOLD}Query:{Colors.ENDC} {query}")
    print(f"\n{Colors.WARNING}Opening browser...{Colors.ENDC}")
    
    # Add a small delay to make the experience more interactive
    for i in range(3, 0, -1):
        print(f"{Colors.CYAN}Launching in {i}...{Colors.ENDC}", end="\r")
        time.sleep(0.5)
    
    webbrowser.open(search_url)
    return search_url

def save_history(domain, category_name, query, url):
    """Save the search history to a file."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    history_file = "dorkviper_history.txt"
    
    with open(history_file, "a") as f:
        f.write(f"[{timestamp}] Domain: {domain} | Category: {category_name} | URL: {url}\n")
    
    print(f"\n{Colors.GREEN}Search saved to {history_file}{Colors.ENDC}")

def main():
    """Main function to run the DorkViper tool."""
    try:
        clear_screen()
        print_banner()
        print_disclaimer()
        
        while True:
            clear_screen()
            print_banner()
            
            # Get target domain
            domain = get_target_domain()
            
            # Get dork categories and let user select one
            categories = get_dork_categories()
            category_choice = select_dork_category(categories)
            selected_category = categories[category_choice]
            
            # Execute the selected dork
            search_url = execute_dork(domain, selected_category)
            
            # Save search history
            save_history(domain, selected_category["name"], selected_category["query"].format(domain), search_url)
            
            # Ask if user wants to continue
            continue_choice = input(f"\n{Colors.BOLD}Do you want to perform another search? (y/n):{Colors.ENDC} ").strip().lower()
            if continue_choice != 'y':
                break
        
        print(f"\n{Colors.GREEN}Thank you for using DorkViper. Goodbye!{Colors.ENDC}")
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Operation cancelled by user. Exiting...{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}An error occurred: {str(e)}{Colors.ENDC}")
    
    sys.exit(0)

if __name__ == "__main__":
    main()