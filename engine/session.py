from .popup import *


class g_session():
    def __init__(self):
        self.session = session

    def get(self, url):
        """
         - requests
        :param url: url
        :return:
        """
        try:
            r = self.session.get(url)
            if r.status_code != 200:
                print("problem status_code", r.status_code)
        except Exception as e:
            print(e)

        return r

    def post(self, url, payload=None, xhr=False):
        """
        - request.post
        :param url: url need post
        :param payload: data
        :param xhr: xhr
        :return: r
        """
        if xhr:
            self.session.headers['X-Requested-With'] = 'XMLHttpRequest'

        try:
            if payload:
                r = self.session.post(url, data=payload)
            else:
                r = self.session.post(url)

            if r.status_code != 200:
                print('Loi dang nhap: status_code', r.status_code)
        except Exception as e:
            print('Loi: {} - url: {}'.format(e, url))

        if xhr:
            del self.session.headers['X-Requested-With']

        return r

    def logout(self):
        r = self.session.get(url=url_logout)
        return

    def close(self):
        r = self.session.close()
