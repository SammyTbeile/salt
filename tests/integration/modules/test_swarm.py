"""
Integration tests for the docker swarm modules
"""

import sys
import salt.utils.path
from tests.support.case import ModuleCase
from tests.support.helpers import destructiveTest, slowTest
from tests.support.mixins import SaltReturnAssertsMixin
from tests.support.unit import skipIf


@destructiveTest
@skipIf(
    not any(salt.utils.path.which(exe) for exe in ("dockerd", "docker")),
    "Docker not installed",
)
class SwarmCallTestCase(ModuleCase, SaltReturnAssertsMixin):
    """
    Test docker swarm states
    """

    def setUp(self):
       """
       setup a swarm for testing
       """
       self.run_function("swarm.swarm_init", ["127.0.0.1", "0.0.0.0", False])


    def tearDown(self):
       """
       teardown docker swarm
       """
       self.run_function("swarm.leave_swarm", [True])

#    @slowTest
#    def test_swarm_init(self):
#        """
#        check that swarm.swarm_init works when a swarm exists
#        """
#        ret = self.run_function("swarm.swarm_init", ["127.0.0.1", "0.0.0.0", False#])
#        expected = {
#            "Comment": 'This node is already part of a swarm. Use "docker swarm leave" to leave this swarm and join another one.',
#            "result": False,
#        }
#        self.assertEqual(expected, ret)

    @slowTest
    def test_swarm_info(self):
       """
       Check that swarm.swarm_info works when the service exists
       """
       self.image_tag = sys.version_info[0]
       first_ret = self.run_function( "swarm.service_create",image="python:3",name="test_swarm_info_service",command="tail -f /dev/null",hostname="swarm_test",replicas=1,target_port=8080,published_port=8080)
       ret = self.run_function("swarm.swarm_service_info", [ "test_swarm_info_service" ])

       self.assertReturnSaltType(ret)
