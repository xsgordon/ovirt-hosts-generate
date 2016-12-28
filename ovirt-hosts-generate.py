import argparse
from ovirtsdk.api import API

def _parseArguments():

    parser = argparse.ArgumentParser(description="Automatically generate" +
                                     "Ansible hosts file for all guests that" +
                                     "report an IP address.")
    parser.add_argument("-l", "--location", action="store",
                        default="https://127.0.0.1/")
    parser.add_argument("-u", "--user", action="store", default="admin@internal")
    parser.add_argument("-p", "--password", action="store", required=True)
    parser.add_argument("-K", "--key-file", action="store", required=False)
    parser.add_argument("-C", "--cert-file", action="store", required=False)
    parser.add_argument("-A", "--ca_file", action="store", required=False)
    parser.add_argument("-I", "--insecure", action="store_true", required=False)

    return parser.parse_args()

def main():

    args = _parseArguments()

    api = API(url=args.location,
              username=args.user,
              password=args.password,
              key_file=args.key_file,
              cert_file=args.cert_file,
              ca_file=args.ca_file,
              insecure=args.insecure)

    # Retrieve all guests that are up and showing an IP
    vms = api.vms.list(query="ip != \"\" and status = \"up\"")

    print("[rhev-guests]")

    for vm in vms:

        # Technically this check that the guest agent info is present should
        # not be needed, as if it game back as having an IP above the agent
        # must be there.
        if vm.get_guest_info():

            # Get the list of IP addresses for the guest.
            ips = vm.get_guest_info().get_ips().get_ip()
            for ip in ips:
                print("%s # %s" % (ip.get_address(), vm.name))

if __name__ == "__main__":
    main()
