"""
Main interface of OVPL with the external world.
Controller interfaces with LabManager and VMPoolManager.

"""

# from time import time
from datetime import datetime
import LabManager
import VMPoolManager
from State import State
from http_logging.http_logger import logger
from utils import git_commands


class Controller:
    def __init__(self):
        self.system = State.Instance()

    def test_lab(self, deployed_by, lab_id, lab_src_url, revision_tag=None):
        logger.debug("test_lab() for lab ID %s and git url %s" %
                     (lab_id, lab_src_url))
        try:
            lab_spec = LabManager.get_lab_reqs(lab_src_url, revision_tag)
            self.update_lab_spec(lab_spec, lab_id, lab_src_url, revision_tag)
            if lab_spec['lab']['runtime_requirements']['hosting'] == \
                    'dedicated':
                """ TODO: Undeploy , fnd proper place to invoke undeploy"""
            # self.undeploy_lab(lab_id)
            vmpoolmgr = VMPoolManager.VMPoolManager()
            logger.debug("test_lab(); invoking create_vm() on vmpoolmgr")
            lab_state = vmpoolmgr.create_vm(lab_spec)
            logger.debug("test_lab(): Returned from VMPool = %s" %
                         (str(lab_state)))
            ip = lab_state['vm_info']['vm_ip']
            port = lab_state['vm_info']['vmm_port']
            vmmgrurl = "http://" + ip
            logger.debug("test_lab(): vmmgrurl = %s" % (vmmgrurl))
            try:
                (ret_val, ret_str) = LabManager.test_lab(vmmgrurl, port,
                                                         lab_src_url,
                                                         revision_tag)
                if(ret_val):
                    self.update_state(lab_state, deployed_by)
                    logger.info("test_lab(): test succcessful")
                    return ip
                else:
                    logger.error("test_lab(); Test failed with error:" +
                                 str(ret_str))
                    return "Test failed: See log file for errors"
            except Exception, e:
                logger.error("test_lab(); Test failed with error: " + str(e))
                return "Test failed: See log file for errors"
                """ TODO: Garbage collection clean up for the created VM """
            finally:
                self.system.save()
        except Exception, e:
            logger.error("test_lab(): Test failed with error: " + str(e))
            return "Test failed: See log file for errors"

    def update_lab_spec(self, lab_spec, lab_id, lab_src_url, revision_tag):
        lab_spec['lab']['description']['id'] = lab_spec['lab_id'] = lab_id
        lab_spec['lab_src_url'] = lab_src_url
        lab_spec['lab_repo_name'] =\
            git_commands.construct_repo_name(lab_src_url)
        lab_spec['revision_tag'] = revision_tag
        lab_spec['lab']['runtime_requirements']['hosting'] = 'dedicated'
        logger.debug("lab_repo_name: %s" % (lab_spec['lab_repo_name']))

    def update_state(self, state, deployed_by):
        state['lab_history']['released_by'] = deployed_by
        # state['lab_history']['released_on'] = strftime("%Y-%m-%d %H:%M:%S")
        state['lab_history']['released_on'] = datetime.utcnow()
        self.system.state.append(state)

    def undeploy_lab(self, lab_id):
        logger.debug("undeploy_lab for lab_id %s" % lab_id)
        vmpoolmgr = VMPoolManager.VMPoolManager()
        vmpoolmgr.undeploy_lab(lab_id)
        return "Success"


if __name__ == '__main__':
    c = Controller()
    t = c.test_lab("test@example.com", "data-structures",
                   "https://github.com/Virtual-Labs/data-structures-iiith.git")
    print t
    # print c.test_lab("test@example.com", "ads",
    #                  "https://github.com/vlead/ovpl")
    # print c.undeploy_lab("ovpl01")
    # print c.undeploy_lab("cse02")
