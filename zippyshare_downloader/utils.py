# zippyshare-downloader
# utils.py

def getStartandEndvalue(value: str, sub: str, second_sub=None):
    v = value[value.find(sub)+1:]
    if second_sub is not None:
        return v[:v.find(second_sub)]
    else:
        return v[:v.find(sub)]