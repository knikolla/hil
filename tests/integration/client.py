# Copyright 2017 Massachusetts Open Cloud Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from abc import ABCMeta, abstractmethod
import json
import subprocess
import uuid

import pytest

from haas.client import client
from haas.test_common import fail_on_log_warnings

fail_on_log_warnings = pytest.fixture(autouse=True)(fail_on_log_warnings)


class ClientTest(object):
    __metaclass__ = ABCMeta

    @pytest.fixture()
    def project(self, request):
        project_name = uuid.uuid4().hex
        self.project_create(project_name)
        assert project_name in self.project_list()

        def finalizer():
            self.project_delete(project_name)
        request.addfinalizer(finalizer)

        return project_name

    @pytest.skip()
    def test_network_crud(self, project):
        network_name = uuid.uuid4().hex
        net_id = 'vlan/native'

        networks = self.network_list()
        assert network_name not in networks
        size = len(networks)

        self.network_create(network_name, project, project, net_id)
        networks = self.network_list()
        assert network_name in networks
        assert len(networks) == size + 1

        network = self.network_show(network_name)
        assert network['label'] == network_name
        assert network['owner'] == project
        assert network['access'] == project
        assert network['net_id'] == net_id

        self.network_delete(network_name)
        networks = self.network_list()
        assert network_name not in networks
        assert len(networks) == size

    def test_project_crud(self):
        """ Test the CRUD operations on projects from the CLI.

        The project list does not need to be empty before running the test."""
        project1 = uuid.uuid4().hex
        project2 = uuid.uuid4().hex

        projects = self.project_list()
        assert project1 not in projects
        assert project2 not in projects
        size = len(projects)

        self.project_create(project1)
        projects = self.project_list()
        assert project1 in projects
        assert project2 not in projects
        assert len(projects) == size + 1

        self.project_delete()
        projects = self.project_list()
        assert project1 not in projects
        assert project2 not in projects
        assert len(projects) == size

    @abstractmethod
    def network_create(self, network, owner, access, net_id):
        pass

    @abstractmethod
    def network_show(self, network):
        pass

    @abstractmethod
    def network_list(self):
        pass

    @abstractmethod
    def network_delete(self):
        pass

    @abstractmethod
    def project_create(self, project):
        pass

    @abstractmethod
    def project_list(self):
        pass

    @abstractmethod
    def project_delete(self, project):
        pass


#######################################################################
# CLI Tests
#######################################################################

class TestCLI(ClientTest):
    def network_create(self, network):
        pass

    def network_show(self, network):
        pass

    def network_list(self):
        pass

    def network_delete(self, owner, access, net_id):
        pass

    def project_create(self, project):
        subprocess.check_call(['haas', 'project_create', project])

    def project_list(self):
        output = subprocess.check_output(['haas', 'list_projects'])
        # Output is presented in the form ' %d Projects : [ ... ]')
        output = output.strip('\n').split('Projects :')[1]
        projects = json.loads(output)
        return projects

    def project_delete(self, project):
        subprocess.check_call(['haas', 'project_delete', project])


#######################################################################
# Client Library Tests
#######################################################################

    class TestClientLibrary(ClientTest):
        def __init__(self):
            self.client = client.Client(
                endpoint='http://127.0.0.1',
                httpClient=client.RequestsHTTPClient()
            )

        def network_create(self, network, owner, access, net_id):
            self.client.network.create(network, owner, access, net_id)

        def network_show(self, network):
            return self.client.network.show(network)

        def network_list(self):
            return self.client.network.list()

        def network_delete(self, network):
            self.client.network.delete(network)

        def project_create(self, project):
            self.client.project.create(project)

        def project_list(self):
            return self.client.project.list()

        def project_delete(self, project):
            self.client.project.delete(project)
