from locust import HttpLocust, TaskSet, task
import json


class WebsiteTasks(TaskSet):

    comment_id = None

    def on_start(self):
        '''
        This code executes before starting virtual users
        login should be done here
        '''

    def get_headers(self):
        headers = {
            'content-type': 'application/json',
        }
        return headers

    @task
    def create_comment(self):
        url = '/comments/'
        comment_data = {
            'content': 'some content',
            'entity_class': 'Event',
            'entity_id': 1,
            'user': {
                'first_name': 'First',
                'last_name': 'Last',
                'email': 'first@last.com',
                'user_id': 1,
            }
        }
        response = self.client.post(url, json=comment_data, headers=self.get_headers())
        data = json.loads(response.text)
        self.comment_id = data['id']

    @task
    def comment_list(self):
        entity_class = 'Event'
        entity_id = 1

        url = '/comments/?entity_class=%s&entity_id=%s' % (
            entity_class,
            entity_id
        )
        self.client.get(url, headers=self.get_headers())

    @task
    def comment_edit(self):
        put_data = {
            'content': 'edited content'
        }

        url = '/comments/%s/' % (
            self.comment_id,
        )
        self.client.put(url, json=put_data, headers=self.get_headers())

class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000
