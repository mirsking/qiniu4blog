import os, time, sys
import qiniu
from mimetypes import MimeTypes
import sys
from AppKit import NSPasteboard, NSArray # macos

mime = MimeTypes()
bucket = "your-bucket"
accessKey = "your-accessKey"
secretKey = "your-secretKey"
path_to_watch = '/Users/leeyoung/Desktop/up2qiniu'

def set_clipboard(url_list):
    pb = NSPasteboard.generalPasteboard()
    pb.clearContents()
    for url in url_list:
        a = NSArray.arrayWithObject_(url)
        pb.writeObjects_(a)
def parseRet(retData, respInfo):
    if retData != None:
        print("Upload file success!")
        print("Hash: " + retData["hash"])
        print("Key: " + retData["key"])
        for k, v in retData.items():
            if k[:2] == "x:":
                print(k + ":" + v)
        for k, v in retData.items():
            if k[:2] == "x:" or k == "hash" or k == "key":
                continue
            else:
                print(k + ":" + str(v))
    else:
        print("Upload file failed!")
        print("Error: " + respInfo.text_body)
def upload_without_key(bucket, filePath, uploadname):
    auth = qiniu.Auth(accessKey, secretKey)
    upToken = auth.upload_token(bucket, key=None)
    key = uploadname
    retData, respInfo = qiniu.put_file(upToken, key, filePath, mime_type=mime.guess_type(filePath)[0])
    parseRet(retData, respInfo)

if __name__ == "__main__":
    print "running ... ..."
    # path_to_watch = sys.argv[1] if len(sys.argv) > 1 else '.'
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while 1:
        time.sleep(1)
        after = dict([(f, None) for f in os.listdir(path_to_watch)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            print "Added Files: ", ", ".join(added)
            # print added
            url_list = []
            for i in added:
                upload_without_key(bucket, os.path.join(path_to_watch, i), i)
                url = 'http://' + bucket + '.qiniudn.com/' + i
                url_list.append(url)

            with open('image_markdown.txt', 'w') as f:
                for url in url_list:
                    image = '![' + url + ']' + '(' + url + ')' + '\n'
                    f.write(image)
            print "image url [markdown] is save in image_markdwon.txt"

            set_clipboard(url_list)
        if removed:
            print "Removed Files: ", ", ".join(removed)
            print  removed
        before = after
