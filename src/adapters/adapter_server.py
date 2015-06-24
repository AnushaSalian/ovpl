#!/bin/python

# Author : Avinash <a@vlabs.ac.in>
# Organization : VLEAD, Virtual-Labs

# Services exposed by CentOSVZAdapter
# http://host-name/api/1.0/vm/create

import json
import urlparse
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from __init__ import *
from httplogging.http_logger import logger
from utils.envsetup import EnvSetUp

define("port", default=8000, help="run on the given port", type=int)



class CreateVMHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Server GET request - Success")

    def post(self):
        logger.debug("post()")
        post_data = dict(urlparse.parse_qsl(self.request.body))
        logger.debug("post(); post_data = %s" % post_data)

        lab_spec = json.loads(post_data['lab_spec'])

        (success, vm_id) = adapter_instance.create_vm(lab_spec)
        debug_string = ""

        if success:
            logger.debug("created VM id = %s" % str(vm_id))
            lab_repo_name = lab_spec['lab_repo_name']
            logger.debug("lab_repo_name = %s" % lab_repo_name)
            (success, result) = adapter_instance.init_vm(vm_id, lab_repo_name)
            if success:
                debug_string = "success status returned True from init_vm"
            else:
                debug_string = "success status returned False from init_vm"
        else:
            result = "Failed while creating VM"
            debug_string = "success status returned False from create_vm"

        if not success:
            self.set_status(500)
            logger.debug(debug_string)
        else:
            logger.debug(debug_string)

        logger.debug("result = " + str(result))
        self.write(result)


class DestroyVMHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        post_data = dict(urlparse.parse_qsl(self.request.body))
        result = adapter_instance.destroy_vm(post_data['vm_id'])
        self.write(result)


class RestartVMHandler(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        pass


if __name__ == "__main__":

    env = EnvSetUp.Instance()
    logger.debug("__main__()")
    tornado.options.parse_command_line()

    try:
        config_spec = env.get_config_spec()
    except IOError as e:
        logger.error("unable to load config.json. Exception: " + str(e))
        raise e
    except Exception as e:
        logger.error("unable to parse config.json. Exception: " + str(e))
        raise e

    # load the adapter class and instantiate the adapter
    adapter_name = config_spec['ADAPTER']['ADAPTER_NAME']
    module = __import__(adapter_name)
    AdapterClass = getattr(module, adapter_name)
    adapter_instance = AdapterClass()

    # make the Adapter log a test message
    adapter_instance.test_logging()

    options.port = config_spec['ADAPTER']["ADAPTER_PORT"]

    # endpoints of our API to create, destroy and restart the server
    create_uri = "/api/1.0/vm/create"
    destroy_uri = "/api/1.0/vm/destroy"
    restart_uri = "/api/1.0/vm/restart"

    logger.debug("__main__() PORT=%s, CreateURI=%s, DestroyURI=%s,"
                 "RestartURI=%s" %
                 (options.port, create_uri, destroy_uri, restart_uri))

    app = tornado.web.Application(
        handlers=[
            (create_uri, CreateVMHandler),
            (destroy_uri, DestroyVMHandler),
            (restart_uri, RestartVMHandler)
        ],
        debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
