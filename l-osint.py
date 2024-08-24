import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import os
from googlesearch import search
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# قائمة المنصات الاجتماعية لدعمها
platforms = {
    'Twitter': 'https://twitter.com/',
    'Facebook': 'https://facebook.com/',
    'Instagram': 'https://instagram.com/',
    'GitHub': 'https://github.com/',
    'Reddit': 'https://www.reddit.com/user/',
    'Pinterest': 'https://www.pinterest.com/',
    'Tumblr': 'https://www.tumblr.com/',
    'Snapchat': 'https://www.snapchat.com/add/',
    'WhatsApp': 'https://wa.me/',
    'TikTok': 'https://www.tiktok.com/@',
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_intro():
    intro = """
                    &xx   &$X+x&X  xX+
                  &XX$&Xx++x&&&&&&
                && x&XxxX&&&&&&&&$X$&&$&&     $XX
              &$$ &&$$&&XXX$$$$$XXXXXx++;;x
             $X$ &&$&&$XXX$&&&&$&&$$$$$$&&&           &
             X$X&&$$$X&&&&&$x: ;&&&&&$$$$$X&&&
           &&$&&&&$$$&&&&&&X :&&&&&&$&&&&&&&&&&&
        XX&X&&$&&&$$&X& $.$&&&&;.X$$$$$$$$$&&$X$XX$$
       X$&; x$&&:&&$$&& ;&  &&&&&$X$$$$XX$$$$&&&&&$x+x++
     &X$&& &&;+& +.&&X$$&&;&&  &&&&&X$$$$XX$$$$&&&$X$&&
     X$&&&+&&.x&;&x &&XX&$$$$&&;$X&&&&&x&&&&&XX$$Xxx+++x
    xX&&$&$$& x&&&&& &&&X&&X&X$$&$$$&&&&&&&&&&&&&&&&&&$
   x$ $X$$X&&;.&X&X&$;&&&&&&&&&&&$&&&&&&&&&&&&&&&&&&
  X  X&$$$X&&&&&$&&&&$X&&&&&&&&&&&$&&&&&&&&&&&&&&&&&&$
    +&  &$&&&&&&&&  &.&&&&&&& &&&  &&&&&&&&&&X    X
      &&X&:&&&&& &      &&&&&&& $  & &&&&&&&&&&X    X
        && &&&&                     & &X&$&X  +
            &+&&.                  +& & $$ $:
                 $      ;. &       & &&  X
                  &      .:;    +  &
                    &           &
                      &;+;&
    """
    print(Fore.RED + Style.BRIGHT + intro)
    print(Fore.YELLOW + Style.BRIGHT + " " * 20 + "• CODEC BY M0HV4R4 •")
    print()

def print_search_options():
    print(Fore.CYAN + Style.BRIGHT + "Select the type of search you want to perform:")
    print(Fore.CYAN + "•"*60)
    print(Fore.GREEN + Style.BRIGHT + "[1] ==> " + Fore.LIGHTYELLOW_EX + "Search by Username")
    print(Fore.GREEN + Style.BRIGHT + "[2] ==> " + Fore.LIGHTYELLOW_EX + "Search by Full Name")
    print(Fore.GREEN + Style.BRIGHT + "[3] ==> " + Fore.LIGHTYELLOW_EX + "Search by Email")
    print(Fore.GREEN + Style.BRIGHT + "[4] ==> " + Fore.LIGHTYELLOW_EX + "Search by Phone Number")
    print(Fore.GREEN + Style.BRIGHT + "[5] ==> " + Fore.RED + "Exit")
    print(Fore.CYAN + "•"*60)
    print()

def search_social_media(username):
    results = {}
    for platform, url_template in tqdm(platforms.items(), desc="Checking platforms", unit="platform"):
        url = f'{url_template}{username}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                meta_tags = soup.find_all('meta', attrs={'name': re.compile(r'og:title|og:url', re.I)})
                title = soup.find('title')

                if meta_tags or (title and 'not found' not in title.get_text().lower()):
                    results[platform] = {'url': url, 'exists': True}
                else:
                    results[platform] = {'url': url, 'exists': False}
            else:
                results[platform] = {'url': url, 'exists': False}
        except requests.RequestException:
            results[platform] = {'url': url, 'exists': False}

    return results

def search_with_google(query):
    search_results = []
    try:
        print(Fore.CYAN + Style.BRIGHT + f"Searching for '{query}' on Google...")
        for url in search(query, num_results=20):
            search_results.append(url)
    except Exception as e:
        search_results.append(f"Error: {str(e)}")
    return search_results

def process_results(results):
    processed_results = {}
    urls_seen = set()
    for url in results:
        if url not in urls_seen:
            processed_results[url] = {'url': url, 'exists': True}
            urls_seen.add(url)
    return processed_results

def print_results(results, search_type):
    if search_type in ['3', '4']:  # Email or Phone search
        title = "Email Search Results" if search_type == '3' else "Phone Number Search Results"
        print(Fore.CYAN + Style.BRIGHT + f"\n{title}")
        print(Fore.RED + "•"*60)
        for url in results:
            print(Fore.GREEN + Style.BRIGHT + "[+] ==> " + Fore.CYAN + url)
        print(Fore.RED + "•"*60)
    elif search_type == '2':  # Full Name search
        print(Fore.CYAN + Style.BRIGHT + "\nGoogle Search Results")
        print(Fore.RED + "•"*60)
        for url in results:
            print(Fore.GREEN + Style.BRIGHT + "[+] ==> " + Fore.CYAN + url)
        print(Fore.RED + "•"*60)
    else:
        print(Fore.CYAN + Style.BRIGHT + "\nSocial Media Accounts Check")
        print(Fore.RED + "•"*60)
        for platform, info in results.items():
            status = Fore.GREEN + Style.BRIGHT + "Exists" if info['exists'] else Fore.RED + Style.BRIGHT + "Does not exist"
            prefix = Fore.GREEN + Style.BRIGHT + '[+]' if info['exists'] else Fore.RED + Style.BRIGHT + '[-]'
            color = Fore.GREEN if info['exists'] else Fore.RED

            formatted_url = Fore.CYAN + info['url']
            print(f"{prefix} {platform}: {formatted_url} - {status}")
        print(Fore.RED + "•"*60)

if __name__ == "__main__":
    clear_screen()  # مسح الشاشة عند بدء التشغيل
    first_run = True
    while True:
        if first_run:
            print_intro()
            first_run = False
        print_search_options()

        search_type = input(Fore.CYAN + Style.BRIGHT + "Enter your choice (1/2/3/4/5): ").strip()
        search_type_input = Fore.WHITE + search_type  # Set the color of the input text to white

        if search_type == '1':
            username = input(Fore.MAGENTA + "Enter the username to check: ").strip()
            results = search_social_media(username)
        elif search_type == '2':
            full_name = input(Fore.MAGENTA + "Enter the full name to check: ").strip()
            search_results = search_with_google(full_name)
            results = process_results(search_results)
        elif search_type == '3':
            email = input(Fore.MAGENTA + "Enter the email to check: ").strip()
            search_results = search_with_google(email)
            results = process_results(search_results)
        elif search_type == '4':
            phone_number = input(Fore.MAGENTA + "Enter the phone number to check: ").strip()
            search_results = search_with_google(phone_number)
            results = process_results(search_results)
        elif search_type == '5':
            print(Fore.YELLOW + Style.BRIGHT + "Exiting the program. Goodbye!")
            break
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid option selected.")
            results = {}

        if results:
            print_results(results, search_type)

        input(Fore.CYAN + Style.BRIGHT + "Press Enter to return to the menu...")
        clear_screen()
        print_intro()
