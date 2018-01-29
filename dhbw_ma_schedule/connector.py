from http.client import HTTPSConnection

from bs4 import BeautifulSoup


class Connector:
    def __init__(self, uid: str):
        self.uid = uid

    def fetch(self, date: str = '') -> BeautifulSoup:
        connection = HTTPSConnection('vorlesungsplan.dhbw-mannheim.de')
        connection.request(
            'GET',
            '/index.php?action=view&uid=%s&date=%s'%(self.uid, date)
        )
        response = connection.getresponse()

        response_status = response.getcode()
        if response_status != 200:
            raise RuntimeError('Server reported Status %s' % (response_status))

        return BeautifulSoup(response.read().decode().encode('utf-8'), 'html.parser')
