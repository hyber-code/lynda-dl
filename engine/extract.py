from .popup import *
from .session import *
from .ffmpeg import FFmpeg
_spin = itertools.cycle(['▲', '►', '▼', '◄'])


def _spinner(text):
    spin = _spin.__next__()
    sys.stdout.write(text + spin)
    sys.stdout.flush()
    time.sleep(0.02)


def NoAccentVietNam(arr):
    """
    - Convert a string
    :param arr: a string
    :return: a string converted
    """
    INTAB = ['ạảãàáâậầấẩẫăắằặẳẵ', 'óòọõỏôộổỗồốơờớợởỡ', 'éèẻẹẽêếềệểễ', 'úùụủũưựữửừứ', 'íìịỉĩ', 'ýỳỷỵỹ', 'đ',
             'ẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴ', 'ÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠ', 'ÉÈẺẸẼÊẾỀỆỂỄ', 'ÚÙỤỦŨƯỰỮỬỪỨ', 'ÍÌỊỈĨ', 'ÝỲỶỴỸ', 'Đ']
    intab2 = ['a', 'o', 'e', 'u', 'i', 'y', 'd', 'A', 'O', 'E', 'U', 'I', 'Y', 'D']
    for i in arr:
        for j in INTAB:
            for k in j:
                if i == k:
                    arr = re.sub(i, intab2[INTAB.index(j)], arr)
    return (''.join(arr.split(' ')))


def removeCharacters(value, deletechars='#<>:"/\|?*'):
    """
    - Remove Character, orgin is '#<>:"/\|?*' if dont want, you can put something in there to remove
    :param value: a string
    :param deletechars: character
    :return: a string removed character
    """
    for c in deletechars:
        value = value.replace(c, '')
    return value


class Extract_info_of_Courses():
    def __init__(self, urlCourses):
        self.urlCourses = urlCourses
        self.infoCourses = dict()

    def GetInfoOfLession(self):
        """
         - Get id of lession and url of lession
        :return: dict have url lession and id lession
        """
        self.count_Lession = 0
        r = g_session().get(url=self.urlCourses)
        self.idCourses = str()
        for line in r.text.split('\n'):
            line = line.strip()
            if 'item-name video-name ga' in line:
                urlLession = re.findall(r'href=\"(.*?)\"', line)[0]
                idLession = re.findall(r'data-ga-value=\"(.*?)\"', line)[0]
                nameLession = urlLession.split('/')[4]
                self.idCourses = urlLession.split('/')[5]
                self.infoCourses[NoAccentVietNam(removeCharacters(nameLession))] = [urlLession, idLession]
                self.count_Lession += 1
            elif '<title>' in line:
                self.nameCourses = re.findall(r"[a-z]\>(.*?)\<", line)[0]
        print(fg + sn + '\n   |' + fr + sn + '+' + fg + sn + '| Course: {}  ( Have {} lession ).\n'.format(
            self.nameCourses,
            self.count_Lession))
        self.DirDownload = os.path.join(currentDir, NoAccentVietNam(removeCharacters(self.nameCourses)))
        if not os.path.exists(self.DirDownload):
            os.mkdir(self.DirDownload)

    def download_video_and_subtitle(self):
        count = 1
        translator = Translator(service_urls=[
            'translate.google.com'
        ])
        header = {}
        for name, lession in self.infoCourses.items():
            print(fg + sd + '   [' + fm + sd + '*' + fg + sd + ']' + '  Downloading ..... {}  ({} of {})'.format(name,
                                                                                                                 count,
                                                                                                                 self.count_Lession))
            if os.path.exists('{}\{}-{}.mp4'.format(self.DirDownload, count, name)) is True:
                print(fg + sd + '\t [' + fr + sd + '-' + fg + sd + ']' + ' Already Download.\n')
            else:
                header = {
                    'Referer': lession[0]
                }
                urlLession = ajax_lession + self.idCourses + '/' + lession[1] + '/play'
                r = session.get(urlLession)
                video = ''
                try:
                    item = re.findall(r'"720":\"(.*?)\"', r.text)
                    video = item[0]
                    r = session.get(item[0])
                    if r.status_code != 200:
                        video = item[1]
                    # print(video)
                    ff = FFmpeg(inputs={'{}'.format(video): None}, outputs={
                        '{}/{}-{}.mp4'.format(self.DirDownload, count, name): '-c copy -bsf:a aac_adtstoasc'})
                    progress = ff.run(stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    for line in progress.stdout:
                        if 'Duration' in line:
                            try:
                                duration = re.findall(r':\s(.*?)\,', line)
                                h = int(duration[0][0:2])
                                m = int(duration[0][3:5])
                                s = int(duration[0][6:8])
                                t = int(duration[0][9:11])
                                x = h + m / 60 + s / 60 / 60
                                print(fg + '\n\t [' + fr + '+' + fg + '] Duration   ..... ' + Fore.BLUE + duration[0])
                                print()
                            except Exception as e:
                                pass
                        if 'frame' in line:
                            try:
                                time = re.findall(r'time=(.*?)\s', line)
                                speed = re.findall(r'bitrate=(.*?)\ss', line)
                                a = fg + '\t [' + fr + '+' + fg + '] Downloaded ..... '
                                hh = int(time[0][0:2])
                                mm = int(time[0][3:5])
                                ss = int(time[0][6:8])
                                tt = int(time[0][9:11])
                                y = hh + mm / 60 + ss / 60 / 60
                                percent = int((y / x) * 40)
                                print(Fore.GREEN + '\r{}'.format(a), end='')
                                print(Fore.GREEN + '╢', end='')
                                print(Fore.RED + '▓' * percent, end='')
                                print(Fore.GREEN + '-' * (40 - percent), end='')
                                print(Fore.GREEN + '╟', end='')
                                print(Fore.CYAN + ' - {} %'.format(round((y / x) * 100, 2)), end='')
                                print(Fore.MAGENTA + '   [{}] '.format(speed[0]), end='')
                            except Exception as e:
                                pass
                        if line.startswith('video:'):
                            try:
                                a = fg + '\t [' + fr + '+' + fg + '] Downloaded ..... '
                                y = x
                                percent = int((y / x) * 40)
                                print(Fore.GREEN + '\r{}'.format(a), end='')
                                print(Fore.GREEN + '╢', end='')
                                print(Fore.RED + '▓' * percent, end='')
                                print(Fore.GREEN + '-' * (40 - percent), end='')
                                print(Fore.GREEN + '╟', end='')
                                print(Fore.CYAN + ' - {} %'.format(100), end='')
                                print(Fore.MAGENTA + '   [{}]   '.format(speed[0]), end='')
                            except Exception as e:
                                pass
                    print()
                except Exception as e:
                    pass
            print()
            text = fg + sd + '\r\t [' + fr + sd + '-' + fg + sd + ']' + ' Downloading video subtitle ..... '
            subtitle = ajax_subtitle + 'courseId=' + self.idCourses + '&videoId=' + lession[1]
            if os.path.exists('{}\{}-{}-en.srt'.format(self.DirDownload, count, name)) is True:
                print(fg + sd + '\t [' + fr + sd + '-' + fg + sd + ']' + ' Already Download subtitle.\n')
                pass
            else:
                file_sub = open('{}\{}-{}-en.srt'.format(self.DirDownload, count, name), 'w', encoding='utf-8')
                r = session.get(subtitle, headers=header)
                try:
                    file_sub.write(r.text)
                except Exception as e:
                    pass
                file_sub.close()
                print(
                    fg + sd + '\r\t [' + fm + sd + '-' + fg + sd + ']' + ' Downloading video subtitle ..... ' + fm + sd + '$(done).\n')
            count += 1
