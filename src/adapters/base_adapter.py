class BaseAdapter:
    def create_vm(lab_spec):
        raise Exception("BaseAdapter: unimplemented create_vm()")

    def init_vm(vm_id, lab_repo_name):
        raise Exception("BaseAdapter: unimplemented init_()")
        # success status, response string
        return (False, "unimplemented")


import netaddr
import sh
import settings


def find_available_ip():
    # try and ping. if the IP does not respond, (gives wrong return code)
    # return the IP as free
    def is_ip_free(ip):
        try:
            sh.ping(str(ip), c=1)
        except sh.ErrorReturnCode:
            return True

        return False

    def is_ip_usable(ip):
            # reject IP's like  192.0.2.0 or 192.0.2.255 for subnet 192.0.2.0/24
            return not (ip == ip_network.network or ip == ip_network.broadcast)

    for subnet in settings.get_subnet():
        ip_network = netaddr.IPNetwork(subnet)
        ip_addrs = list(ip_network)
        # logger.debug("ip addresses: %s" % str(ip_addrs))
        for ip in ip_addrs:
            if is_ip_usable(ip) and is_ip_free(ip):
                return str(ip)

    raise Exception("unable to find free ip in subnet ", settings.get_subnet())
    return None
