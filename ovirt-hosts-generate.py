import argparse
from ovirtsdk.api import API

def _parseArguments():
    """
    Parse command line arguments using argparse, these parameters currently
    mimic those of the command line client for the oVirt/RHEV API and relate
    primarily to initiating the API connection.
    """

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
    """
    Initiate API connection and retrieve list of guests that have IP address
    information available.
    """

    args = _parseArguments()

    # Initiate API connection, some of these values will be empty depending on
    # the type of the connection being used (particularly secure versus
    # insecure). Using insecure=True (by specifying -I on the command line) is
    # the easiest way to get up and running but of course trades off security.
    api = API(url=args.location,
              username=args.user,
              password=args.password,
              key_file=args.key_file,
              cert_file=args.cert_file,
              ca_file=args.ca_file,
              insecure=args.insecure)

    # Retrieve all guests that are up and showing an IP
    vms = api.vms.list(query="ip != \"\" and status = \"up\"")

    # Print a basic group header for the hosts.
    # TODO: Separate groupings for each guest OS type.
    print("[rhev-guests]")

    # Loop through all the returned VMs.
    for vm in vms:

        # Technically this check that the guest agent info is present should
        # not be needed, as if it came back as having an IP above the agent
        # must be there.
        if vm.get_guest_info():

            # Get the list of IP addresses for the guest.
            # TODO: The structure of this would suggest we might want to verify
            #       how robust it is if more than one record comes back etc.
            ips = vm.get_guest_info().get_ips().get_ip()
            for ip in ips:
                print("%s # %s" % (ip.get_address(), vm.name))

if __name__ == "__main__":
    main()
