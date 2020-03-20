import requests

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# 十进制转62进制
def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """

    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

# 62进制转十进制
def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
    idx += 1

    return num

# 62进制转十进制网址版
def url_to_mid(url):
    url = str(url)[::-1]
    size = len(url) / 4 if len(url) % 4 == 0 else len(url) / 4 + 1
    result = []
    for i in range(size):
        s = url[i * 4: (i + 1) * 4][::-1]
        s = str(base62_decode(str(s)))
        s_len = len(s)
        if i < size - 1 and s_len < 7:
            s = (7 - s_len) * '0' + s
        result.append(s)
    result.reverse()
    return int(''.join(result))

# 十进制转62进制网址版
def mid_to_url(midint):
    # mid_to_url(3501756485200075) 'z0JH2lOMb'
    # midint = str(midint)[::-1]
    midint = midint[::-1]
    size = int(len(midint) / 7) if len(midint) % 7 == 0 else int(len(midint) / 7) + 1
    result = []
    for i in range(size):
        s = midint[i * 7: (i + 1) * 7][::-1]
        s = base62_encode(int(s))
        s_len = len(s)
        if i < size - 1 and len(s) < 4:
            s = '0' * (4 - s_len) + s
        result.append(s)
    result.reverse()
    return ''.join(result)

# input: 移动版网址
# output: 网页版网址
def midurl_to_weburl(midurl):
    midintstr = midurl.split('/')[-1]
    if midintstr[-1] == '?':
        midintstr = midintstr[:-1]
    c = requests.get(midurl).text
    user_id = (c.split("user")[5]).split('"profile_image_url"')[-2].split('"id": ')[-1].split(",")[-3] #user id
    weburl = 'https://www.weibo.com/' + user_id + '/' + mid_to_url(midintstr)
    return weburl
