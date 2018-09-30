from engine.popup import *
from engine.session import *
from engine.extract import *


def login(username, password, organization, url_login):
    """
     - login webste with username and password throught prganization
    :param username:
    :param password:
    :param organization:
    :return: true or false
    """
    seasurf = ''
    r = g_session().get(url_login)
    for line in r.text.split('\n'):
        line = line.strip()
        if 'seasurf' in line:
            seasurf = re.findall(r'value=\"(.*?)\"', line)[0]
            break
    data = {
        'libraryCardNumber': username,
        'libraryCardPin': password,
        'org': organization,
        'currentView': 'login',
        'seasurf': seasurf
    }
    r = g_session().post(url=url_login, payload=data)
    if r.url != 'https://www.lynda.com/':
        return False
    return True


def main():
    os.system('cls')
    for line in Banner().split('\n'):
        print(line)
        time.sleep(0.07)
    username = input('\t   Username: ')
    password = input('\t   Password: ')
    organication_login = input('\t   Url organication: ')
    urlCourses = []
    while True:
        url = input('\t   Url course: ')
        if url.startswith('https://www.lynda.com'):
            urlCourses.append(url)
        elif url == '':
            break
        else:
            continue
    organication = re.findall(r'org=(.*)', organication_login)[0]
    print(fg + sd + '\t[' + fr + sd + '-' + fg + sd + ']' + ' Trying to login to ...... ' + fm + '$' + organication)
    if login(username=username, password=password, organization=organication, url_login=organication_login) is True:
        print(fg + sd + '\t[' + fr + sd + '-' + fg + sd + ']' + ' Login is True')
    else:
        print(fg + sd + '\t[' + fr + sd + '-' + fg + sd + ']' + ' Login is False')
    for link in urlCourses:
        extract = Extract_info_of_Courses(urlCourses=link)
        extract.GetInfoOfLession()
        extract.download_video_and_subtitle()
    g_session().logout()
    g_session().close()
    print(fg + sd + '\t\t[' + fm + '-' + fg + '] Download .... Done')
    time.sleep(60)
    sys.exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(fc + sd + "\n\t[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "User Interrupted.....")
        sys.exit(0)
