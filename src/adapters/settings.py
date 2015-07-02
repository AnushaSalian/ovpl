import sys
print sys.path
# This can be either 'TRUE' or 'FALSE' based
# from where the ADS services are running.
ADS_ON_CONTAINER = False
# BASE_IP_ADDRESS will hold the IP of the base machine on
# which containers will be created"
BASE_IP_ADDRESS = "root@10.2.56.182"
NO_STRICT_CHECKING = "StrictHostKeyChecking no"
# ADS_SERVER_ID will be CTID of the container running ADS services
ADS_SERVER_VM_ID = "<CTID>"
VM_ROOT_DIR = "/vz/root/"
VM_DEST_DIR = "/root/"
VMMANAGERSERVER_PATH = "/root/ovpl/src/vmmanager/"
VM_MANAGER_PORT = "9089"

# run VMManagerServer with the default VMManager
VM_MANAGER_SCRIPT = "vm_manager_server.py"
MAX_VM_ID = 2147483644  # 32-bit; exact value based on trial-and-error

# Settings for Bridged Adapter
SUBNET_BRIDGE = "base1br"


def get_subnet():
    # Subnet: IP addresses will be picked from and assigend to lab VMs
    SUBNET = ["10.2.56.182/24"]
    assert isinstance(SUBNET, list)
    return SUBNET


def get_test_lab_id():
    # can be used to create a test lab ID if lab id is empty
    LAB_ID = "engg01"
    assert isinstance(LAB_ID, str)
    assert LAB_ID != ""
    return LAB_ID


def get_test_os():
    LAB_ID = ""
    # can be used to set a default OS if OS is not specified in lab spec
    OS = "Ubuntu"
    assert isinstance(LAB_ID, str)
    assert OS != ""
    return OS


def get_test_os_version():
    # can be used to set a default OS version
    # if OS is not specified in lab spec
    OS_VERSION = "12.04"
    assert isinstance(OS_VERSION, str)
    assert OS_VERSION != ""
    return OS_VERSION


def get_adapter_nameserver():
    # Required by CentOSVZAdapter.py
    NAME_SERVER = "inherit"
    return NAME_SERVER


def get_adapter_hostname():
    HOST_NAME = "vlabs.ac.in"
    return HOST_NAME
