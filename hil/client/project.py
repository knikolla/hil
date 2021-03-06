"""Client support for project related api calls."""
import json
from hil.client.base import ClientBase


class Project(ClientBase):
        """Consists of calls to query and manipulate project related

        objects and relations.
        """

        def list(self):
            """Lists all projects under HIL """

            url = self.object_url('/projects')
            return self.check_response(self.httpClient.request("GET", url))

        def nodes_in(self, project_name):
            """Lists nodes allocated to project <project_name> """
            url = self.object_url('project', project_name, 'nodes')
            return self.check_response(self.httpClient.request("GET", url))

        def networks_in(self, project_name):
            """Lists nodes allocated to project <project_name> """
            url = self.object_url(
                    'project', project_name, 'networks'
                    )
            return self.check_response(self.httpClient.request("GET", url))

        def create(self, project_name):
            """Creates a project named <project_name> """
            url = self.object_url('project', project_name)
            return self.check_response(self.httpClient.request("PUT", url))

        def delete(self, project_name):
            """Deletes a project named <project_name> """
            url = self.object_url('project', project_name)
            return self.check_response(self.httpClient.request("DELETE", url))

        def connect(self, project_name, node_name):
            """Adds a node to a project. """
            url = self.object_url(
                    'project', project_name, 'connect_node'
                    )
            self.payload = json.dumps({'node': node_name})
            return self.check_response(
                    self.httpClient.request("POST", url, data=self.payload)
                    )

        def detach(self, project_name, node_name):
            """Detaches a node from a project. """
            url = self.object_url('project', project_name, 'detach_node')
            self.payload = json.dumps({'node': node_name})
            return self.check_response(
                    self.httpClient.request("POST", url, data=self.payload)
                    )
