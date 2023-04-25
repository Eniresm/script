import os
import subprocess
import re
import socket
import requests

# Define colors for console output
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
MAGENTA = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
LIGHT_YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_MAGENTA = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RESET = "\033[0m"
NORMAL = "\033[0m"
# Define Subdomains
def subdomains(directory, domain):
    with open(f"{directory}/subdomains_{domain}.txt", "w") as f:
        print("Commandes Available")
        print("1.Dnsrecon")
        print("2.Sublist3r")
        print("3.Fierce")
        print("4.Amass")
        print("5.Subfinder")
        selected_commandes = input("Entrez les commandes :")
        selected_commandes = [int(x.strip()) for x in selected_commandes.split(",")]
        for com in selected_commandes:
            if com == 1:
                print(f"{LIGHT_CYAN} dnsrecon")
                commanddns=f"dnsrecon -d {domain}"
                resultdns = subprocess.check_output(commanddns, shell=True, universal_newlines=True)
                f.write("------------------------------dnsrecon------------------------------------------------------\n")
                for line in resultdns.splitlines():
                    if domain in line:
                        f.write(line + "\n")
            if com == 2:
                print(f"{LIGHT_CYAN} sublist3r")
                commandsublist3r=f"sublist3r -d {domain}"
                resultsub=subprocess.check_output(commandsublist3r, shell=True, universal_newlines=True)
                f.write("----------------------------------sublist3r--------------------------------------------------\n")
                for line in resultsub.splitlines():
                    line = line.partition("m")[2]
                    if domain in line:
                        f.write(line + "\n")
            if com == 3:
                print(f"{LIGHT_CYAN} fierce")
                commandfierce =f"fierce --domain {domain}"
                resultsfierce=subprocess.check_output(commandfierce, shell=True, universal_newlines=True)
                f.write("-----------------------------fierce-------------------------------------------------------\n")
                for line in resultsfierce.splitlines():
                    if domain in line:
                        f.write(line + "\n")
            if com == 4:
                print(f"{LIGHT_CYAN} Amass")
                commandamass = f"amass enum -d {domain} | grep {domain}"
                resultsamass = subprocess.check_output(commandamass , shell=True, universal_newlines=True)
                f.write("-----------------------------Amass-------------------------------------------------------\n")
                for line in resultsamass .splitlines():
                    if domain in line:
                        f.write(line + "\n")
            if com == 5:
                print(f"{LIGHT_CYAN} Subfinder")
                commandsubfinder= f"subfinder -silent -d {domain} | dnsx -silent"
                resultsubfinder= subprocess.check_output(commandsubfinder, shell=True, universal_newlines=True)
                f.write("-----------------------------subfinder -------------------------------------------------------\n")
                for line5 in resultsubfinder .splitlines():
                    if domain in line5:
                        f.write(line5 + "\n")
    # Define a regular expression pattern to match subdomains
    subdomain_pattern = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}(?!\.)'
    # Open the text file for reading
    with open(f"{directory}/subdomains_{domain}.txt", 'r') as file:
        # Read the contents of the file
        contents = file.read()
        # Find all matches of the subdomain pattern in the contents
        subdomains = set(re.findall(subdomain_pattern, contents))
        with open(f"{directory}/Subdomains_{domain}.txt", 'w') as f1:
            # Parcourir chaque ligne des résultats
            f1.write('\n'.join(subdomains))
    print(f"{YELLOW} file done")

# Define fuzzing
def fuzzing(directory,output, domain):
    # print message to user
    print(f"\n{GREEN}[+] Directory search {NORMAL}\n")
    print("Available commands")
    print("1. Dirsearch")
    print("2. Dirb")
    print("3. Gobuster")
    # define the pattern for matching URLs
    url_pattern = re.compile(r'https?://\S+')
    # open the log file
    with open(f"{directory}/{output}", 'r') as f:
        with open(f"{directory}/Fuzzing_{domain}.txt", 'w') as file:
            # read the file line by line
            selected_commands = input("Enter the commands: ")
            selected_commands = [int(x.strip()) for x in selected_commands.split(",")]

            for com in selected_commands:
                for line in f:
                    if com == 1:
                        command_dirsearch = f"dirsearch -u https://{line}"
                        result_dirsearch = subprocess.check_output(command_dirsearch, shell=True, universal_newlines=True)
                        for line1 in result_dirsearch.splitlines():
                            match = url_pattern.search(line1)
                            # if a URL is found, print it
                            if match:
                                file("*******************************************")
                                file(line1)
                                file.write(match.group())
                                file.write("\n")
                    if com == 2:
                        command_dirb=f"dirb http://{line}/ /usr/share/wordlists/dirb/common.txt"
                        try:
                            result_dirb = subprocess.check_output(command_dirb, shell=True, universal_newlines=True)
                            for line2 in result_dirsearch.splitlines():
                                match = url_pattern.search(line2)
                                # if a URL is found, print it
                                if match:
                                    file("*******************************************")
                                    file.write(line2)
                                    file.write(match.group())
                                    file.write("\n")
                        except subprocess.CalledProcessError as e:
                            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}:")
                            print(e.output)
                    if com == 3:
                        command_gobuster = f"gobuster dir -e -u https://{line} -w /home/enirck/tools/SecLists/Discovery/DNS/subdomains-top1million-5000.txt"
                        try:
                            result_gobuster = subprocess.check_output(command_gobuster, shell=True, universal_newlines=True)
                            for line3 in result_gobuster.splitlines():
                                match = url_pattern.search(line3)
                                # if a URL is found, print it
                                if match:
                                    file("*******************************************")
                                    file.write(line3)
                                    file.write(match.group())
                                    file.write("\n")
                        except subprocess.CalledProcessError as e:
                            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}:")
                            print(e.output)

# Information Ghatering
def Google_Hacking(directory,output, domain):
    print(f"\n{GREEN}[+] Google Hacking {NORMAL}\n")
    print("Available commands")
    print("1. GooFuzz")
    with open(f"{directory}/{output}", 'r') as f:
        with open(f"{directory}/Google_Hacking_{domain}.txt", 'w') as file:
            # read the file line by line
            selected_commands = input("Enter the commands: ")
            selected_commands = [int(x.strip()) for x in selected_commands.split(",")]
            for com in selected_commands:
                for line in f:
                    commandgoofuzz=f"home/enirck/PycharmProjects/script_Automatisation/GooFuzz/./GooFuzz -t {line} -e pdf,bak,old -d 10"
                    result_goofuzz= subprocess.check_output(commandgoofuzz, shell=True, universal_newlines=True)
                    file.write(result_goofuzz)

def Vulnerability_Scanner(directory,output, domain):
    print(f"\n{GREEN}[+] Vulnerability Scanner {NORMAL}\n")
    print("Available commands")
    print("1. Nikto")
    with open(f"{directory}/{output}", 'r') as f:
        with open(f"{directory}/Vulnerability_Scanner_{domain}.txt", 'w') as file:
            # read the file line by line
            selected_commands = input("Enter the commands: ")
            selected_commands = [int(x.strip()) for x in selected_commands.split(",")]
            for com in selected_commands:
                for line in f:
                    commandnikto=f"nikto -h {line} "
                    result_nikto= subprocess.check_output(commandnikto, shell=True, universal_newlines=True)
                    cleaned_result_nikto = result_nikto.replace("+", "")
                    file.write(cleaned_result_nikto)
def endpoint(directory,output,domain):
    print(f"\n{GREEN}[+] End Points {NORMAL}\n")
    # define the pattern for matching URLs
    url_pattern = re.compile(r'https?://\S+')
    print("Available commands")
    print("1. Jsleak")
    selected_commands = input("Enter the commands: ")
    selected_commands = [int(x.strip()) for x in selected_commands.split(",")]
    with open(f"{directory}/{output}", 'r') as f:
        text = f.readlines()
        with open(f"{directory}/endpoint_{domain}.txt", 'w') as fi: # open the output file here
            for com in selected_commands:
                if com == 1:
                    for line in text:
                        line = line.rstrip('\n')
                        fi.write("*******************************************\n")
                        commandjs=f"echo https://{line} | jsleak -c 20 -k"
                        fi.write(line)
                        result_jsleak=subprocess.check_output(commandjs, shell=True, universal_newlines=True)
                        for line1 in result_jsleak.splitlines():
                            match = url_pattern.search(line1)
                            # if a URL is found, write it to the output file
                            if match:
                                fi.write(match.group() + "\n")


def Scan(directory,output, domain):
    print(f"\n{GREEN}[+] Scanner {NORMAL}\n")
    print("Available commands")
    print("1. Nmap")
    selected_commands = input("Enter the commands: ")
    selected_commands = [int(x.strip()) for x in selected_commands.split(",")]
    with open(f"{directory}/{output}", 'r') as f:
        text = f.readlines()
        for com in selected_commands:
            if com == 1:
                for line in text:
                    line = line.rstrip('\n')
                    command = f"nmap -A -script vuln -oX {directory}/{line}.xml {line}"
                    command1 = f"xsltproc {directory}/{line}.xml -o {directory}/{line}.html "
                    result1 = subprocess.check_output(command, shell=True, universal_newlines=True)
                    result2 = subprocess.check_output(command1, shell=True, universal_newlines=True)
                    xml = f"{directory}/{line}.xml"
                    os.remove(xml)

if __name__ == '__main__':
    domain = input(f"{BLUE}Please enter a domain name to scan: {BLUE}")
    while not domain:
        domain = input(f"{BLUE}Please enter a domain name to scan: {BLUE}")
    directory = input("Please enter a directory: ")
    while not directory:
        directory = input("Please enter a directory: ")
    an_folder =input("do you want to create a folder in your directory to put your output or you want to put it in directory answer with [yes/no] : ")
    if an_folder == "yes" :
        folder_name= input("name of your folder : ")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        directory=directory+"/"+folder_name
    elif an_folder == "no" :
        directory = directory
    else :
        an_folder = input("do you want to create a folder in your directory to put your output or you want to put it in directory answer with [yes/no] : ")

    print("Available functions")
    print("1.Subdomain Enumeration")
    print("2.Informations sur URLs")
    print("3.Nmap")
    print("4.Fuzzing")
    selected_functions = input("\nEnter comma-separated function numbers to run (e.g. 1,2,3), or type 'all' to select both all: ")

    if selected_functions == "all":
        subdomains(directory,domain)

    else:
        selected_functions = [int(x.strip()) for x in selected_functions.split(",")]
        for func in selected_functions:
            if func == 1:
                print("Subdomain Enumeration")
           