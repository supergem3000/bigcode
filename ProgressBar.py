import time
class ProgressBar:

    def __init__(self, title, total):
        super().__init__()
        self.__title = title
        self.__total = total
        self.__length = 20
        self.__current = -1
        print(title + ':')
        self.progress()

    def progress(self):
        self.__current += 1
        percent = self.__current / self.__total
        show = int(percent * self.__length)
        bar = '[' + ('█' * show) + (' ' * (self.__length - show)) + '] '
        bar = '\r' + bar + str(self.__current) + '/' + str(self.__total)
        print(bar, end='', flush=True)
        if self.__current == self.__total:
            print()

if __name__ == '__main__':
    progressbar = ProgressBar("无内鬼", 37)
    for i in range(0,37):
        time.sleep(0.1)
        progressbar.progress()