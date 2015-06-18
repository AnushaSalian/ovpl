import os
import os.path
import logging
from __init__ import *
from logging.handlers import HTTPHandler
from utils.envsetup import EnvSetUp


def __create_logger(name):
    env = EnvSetUp.Instance()
    config_spec = env.get_config_spec()
    logserver_ip = config_spec["LOGGING_CONFIGURATION"]["LOGSERVER_CONFIGURATION"]["SERVER_IP"]
    logserver_port = config_spec["LOGGING_CONFIGURATION"]["LOGSERVER_CONFIGURATION"]["SERVER_PORT"]
    logserver_uri = config_spec["LOGGING_CONFIGURATION"]["LOGSERVER_CONFIGURATION"]["URI_ENDPOINT"]
    log_level = config_spec["LOGGING_CONFIGURATION"]["LOG_LEVEL"]
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if logger.handlers == []:
        server = logserver_ip + ":" + str(logserver_port)
        print server
        http_handler = HTTPHandler(host=server, url=logserver_uri,
                                   method="POST")
        logger.addHandler(http_handler)

    return logger


logger = __create_logger("ovpl")
test_logger = __create_logger("tests")


if __name__ == '__main__':
    env = EnvSetUp.Instance()
    logger.debug("Hello World")
    GIT_CLONE_LOC = "/home/travula/"
    repo_name = "ovpl"
    dir_path = GIT_CLONE_LOC+repo_name+"/config"
    os.chdir(dir_path)
    logger.debug("Changed to Diretory: %s" % dir_path)
    logger.debug("CWD: %s" % str(os.getcwd()))
