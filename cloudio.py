import os
import requests
import binascii

path = r'user_data.bin'
dct = {1: ['rafam', 'rafamanuel'], 2: ['luciaf', 'Franco!!!2']}


def login(number):
    """login to username
    :param number: the number of the user in the dict
    :return: the login message
    """
    payload = {'username': dct[number][0],
               'password': dct[number][1]}
    url = 'http://52.51.189.241/api/login'
    r = requests.post(url, json=payload)
    return r.text


def get_api_key(r):
    """getting the api key of the user
    :param r: the login message
    :return: aki key
    """
    # r is the response from the login
    r_s = str(r)
    api_key_s = r_s.find("api_key")  # start of api_key
    r3 = r_s[api_key_s + 9::]
    api_key_e = r3.find(",")  # end of api_key
    api_key = (r3[1:api_key_e - 1])
    return api_key


def get_user_id(r):
    """getting the user id
    :param r: the login message
    :return: user id
    """
    r_s = str(r)
    user_id_s = r_s.find('user_id')
    r3 = r_s[user_id_s + 9::]
    user_id_e = r3.find("}")
    user_id = r3[0:user_id_e]
    return user_id


def convert_id_hex(user_id):
    """convert the id to hexa
    :param user_id: the id of the user
    :return: the user id in hexa
    """
    h = hex(int(user_id))
    h2 = str(h)
    h3 = h2[2::]
    len_zero = 8 - len(h3)
    s = ""
    for i in range(len_zero):
        s += '0'
    s += h2[2::]

    return binascii.unhexlify(s)


def binary_file(path, u_id, api_key):
    """writing the required information to binary file
    :param path: the path of the binary file
    :param u_id: the user id
    :param api_key: the api key
    """
    binary = str(api_key)
    print(binary)
    with open(path, 'wb') as f:
        f.write(u_id)
    with open(path, 'ab') as f:
        f.write(bytes(binary.encode()))


def get_photos_list(api_key):
    """getting the photos list of the specific user
    :param api_key: the api key of the user we get the image for
    :return: the image list
    """
    url = 'http://52.51.189.241/api/get_filelist'
    d_api_key = {"x-api-key": api_key}
    print(d_api_key)
    r = requests.post(url, headers=d_api_key)
    imgs = r.text
    return str(imgs)


def arrange_imgs(img_list):
    """get the image list and arrange it
    :param img_list: the image list of the user
    :return: arranged list
    """
    s = img_list.find("[")
    e = img_list.find("]")
    # .strip('][').split(', ')
    lst = img_list[s + 1:e].split(",")
    return lst


for i in range(len(dct.keys())):

    r = login(i+1)
    print(r)
    log = get_api_key(r)
    print(log)
    u_id = convert_id_hex(get_user_id(r))
    print(u_id)
    api_key = get_api_key(r)
    binary_file(path, u_id, api_key)
    lst_images = arrange_imgs(get_photos_list(api_key))
    print(lst_images)
    for curr_file in lst_images:
        os.system(
            'cmd /c "cloudio_file_client --settings settings.ini --userdata user_data.bin --filename "' + curr_file)
