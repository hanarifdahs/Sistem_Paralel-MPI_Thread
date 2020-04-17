import os
import requests
import threading
import urllib.request, urllib.error, urllib.parse
import time

url = "https://apod.nasa.gov/apod/image/1901/LOmbradellaTerraFinazzi.jpg"


def buildRange(value, numsplits):
    lst = []
    for i in range(numsplits):
        #ubah data jadi 0 - split yang pertama
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
        # split pertama + 1 - split kedua, dan seterusnya
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0),0)), int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
    print(lst)
    return lst

class SplitBufferThreads(threading.Thread):
    """ Splits the buffer to ny number of threads
        thereby, concurrently downloading through
        ny number of threads.
    """
    def __init__(self, url, byteRange):
        super(SplitBufferThreads, self).__init__()
        # assignment tiap argument ke variabel di self
        self.__url = url
        self.__byteRange = byteRange
        self.req = None

    def run(self):
        # method utama
        # request berdasarkan url dan range byte yang sudah ditentukan
        self.req = urllib.request.Request(self.__url,  headers={'Range': 'bytes=%s' % self.__byteRange})

    def getFileData(self):
        # download
        return urllib.request.urlopen(self.req).read()


def main(url=None, splitBy=3):
    # catat waktu mulai
    start_time = time.time()

    # cek url ada isinya atau nggak
    if not url:
        print("Please Enter some url to begin download.")
        return

    # pisah url berdasarkan /, menjadi list
    fileName = url.split('/')[-1]

    # minta headers http dari url yang isinya 'content-length' atau size dari file
    sizeInBytes = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)

    # output size
    print("%s bytes to download." % sizeInBytes)
    if not sizeInBytes:
        print("Size cannot be determined.")
        return

    # file size dibagi 3, dan masing masing dibuat threadnya
    dataLst = []
    for idx in range(splitBy):
        # bagi 3
        # sangat tidak efektif, buat apa manggil method buildrange berkali kali? cukup panggil buildrange sekali di sebelum for, ke var x
        # lalu disini tinggal assignment byterange = x[idx]
        byteRange = buildRange(int(sizeInBytes), splitBy)[idx]
        # bikin thread
        bufTh = SplitBufferThreads(url, byteRange)
        # mulai
        bufTh.start()
        # wait
        bufTh.join()
        # masukkin hasil read ke dataLst
        dataLst.append(bufTh.getFileData())

    # gabung isi dataLst, ubah jadi byte
    content = b''.join(dataLst)

    if dataLst:
        # hapus kalo ada filenya nama sama
        if os.path.exists(fileName):
            os.remove(fileName)
        # output waktu
        print("--- %s seconds ---" % str(time.time() - start_time))
        # write
        with open(fileName, 'wb') as fh:
            fh.write(content)
        print("Finished Writing file %s" % fileName)

if __name__ == '__main__':
    main(url)