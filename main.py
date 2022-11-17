import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC Address")
    parser.add_option("-m", "--mac", dest="mac_address", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more information")
    elif not options.mac_address:
        parser.error("[-] Please specify a MAC Address, use --help for more information")
    return options


def change_map(interface, mac_address):
    subprocess.call(f"ifconfig {interface} down", shell=True)
    subprocess.call(f"ifconfig {interface} hw ether {mac_address}", shell=True)
    subprocess.call(f"ifconfig {interface} up", shell=True)

    print(f"[+] Changing MAC address of {interface} to {mac_address}")


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w".encode(), ifconfig_result)
    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("[-] Could not read the MAC Address")


options = get_arguments()
try:
    current_mac = get_current_mac(options.interface).decode()
except AttributeError:
    current_mac = get_current_mac(options.interface)
print("Current MAC: " + str(current_mac))
change_map(options.interface, options.mac_address)

try:
    current_mac = get_current_mac(options.interface).decode()
except AttributeError:
    current_mac = get_current_mac(options.interface)
if current_mac == options.mac_address:
    print("[+] MAC Address was successfully changed to " + current_mac)
else:
    print("[-] MAC Address did not changed")



