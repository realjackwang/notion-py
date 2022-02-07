import json
import requests


class Notion:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.notion_version = "2021-08-16"
        self.headers = {
            "Authorization": "Bearer " + self.secret_key,
            "Notion-Version": self.notion_version,
            "Content-Type": "application/json"
        }
        self.baseurl = "https://api.notion.com/v1/"

    def retrieve_page(self, page_id: str) -> dict:
        url = self.baseurl + "pages/" + page_id
        res = requests.get(url, headers=self.headers)
        return json.loads(res.content.decode())

    def create_page(self, parent: dict, properties: dict) -> dict:
        url = self.baseurl + "pages"
        data = json.dumps({"parent": parent, "properties": properties})
        res = requests.post(url, headers=self.headers, data=data)
        return json.loads(res.content.decode())

    def update_page(self, page_id: str, properties: dict) -> dict:
        url = self.baseurl + "pages/" + page_id
        data = json.dumps({"properties": properties})
        res = requests.patch(url, headers=self.headers, data=data)
        return json.loads(res.content.decode())

    def archive_page(self, page_id: str, archived: bool = True) -> dict:
        url = self.baseurl + "pages/" + page_id
        data = json.dumps({"archived": archived})
        res = requests.patch(url, headers=self.headers, data=data)
        return json.loads(res.content.decode())

    def retrieve_database(self, database_id: str) -> dict:
        url = self.baseurl + "databases/" + database_id
        res = requests.get(url, headers=self.headers)
        return json.loads(res.content.decode())

    def query_database(self, database_id: str, start_cursor=None) -> dict:
        # todo 修改云函数的这里
        url = self.baseurl + "databases/" + database_id + "/query"
        if start_cursor:
            res = requests.post(url, headers=self.headers, json={'start_cursor': start_cursor})
        else:
            res = requests.post(url, headers=self.headers)
        res_json = json.loads(res.content.decode())
        data = res_json['results']
        if res_json['has_more']:
            data = data + self.query_database(database_id, res_json['next_cursor'])
        return data

    def list_databases(self, start_cursor=None, page_size=None):
        pass

    def create_database(self, parent, properties, title=None):
        pass

    def update_database(self, database_id, title=None, properties=None):
        pass

    def retrieve_block(self, block_id):
        url = self.baseurl + "blocks/" + block_id
        res = requests.get(url, headers=self.headers)
        return json.loads(res.content.decode())

    def update_block(self, block_id, data):
        url = self.baseurl + "blocks/" + block_id
        res = requests.patch(url, headers=self.headers, json=data)
        return json.loads(res.content.decode())

    def del_block(self, block_id, archived: bool = True):
        pass

    def retrieve_block_children(self):
        pass

    def append_block_children(self):
        pass

    def retrieve_user(self):
        pass

    def list_users(self):
        pass

    @staticmethod
    def title(content: str):
        return {'title': [{'text': {'content': content}}]}

    @staticmethod
    def rich_text(content: str, link=None):
        return {'rich_text': [{'text': {'content': content, 'link': link}}]}

    @staticmethod
    def number(number: float):
        return {'number': number}

    @staticmethod
    def select(select_name: str):
        return {'select': {'name': select_name}}

    @staticmethod
    def multi_select(select_names: list):
        return {'multi_select': [{'name': select_name} for select_name in select_names]}

    @staticmethod
    def date(start: str, end=None):
        if end:
            return {'date': {'start': start, 'end': end}}
        return {'date': {'start': start}}

    @staticmethod
    def files(files):
        # 此版本的NotionAPI并不支持文件上传与下载
        return {'files': [{'name': file, 'type': 'external', 'external': {'url': file}} for file in files]}

    @staticmethod
    def checkbox(check=True):
        return {'checkbox': check}

    @staticmethod
    def url(url: str):
        return {'url': url}

    @staticmethod
    def dumps(data):
        """
        将Pages的Properties中的指定参数解码出来
        :param data:
        :return:
        """
        try:
            if data['type'] == 'title':
                return data['title'][0]['text']['content']
            elif data['type'] == 'rich_text':
                return data['rich_text'][0]['text']['content']
            elif data['type'] == 'number':
                return data['url']
            elif data['type'] == 'select':
                return data['select']['name']
            elif data['type'] == 'multi_select':
                return [name['name'] for name in data['multi_select']]
            elif data['type'] == 'date':
                return None
            elif data['type'] == 'checkbox':
                return data['checkbox']
            elif data['type'] == 'files':
                return None
            elif data['type'] == 'url':
                return data['url']
        except (AttributeError, IndexError):
            return None
