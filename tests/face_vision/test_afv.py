from access_client.face_vision.client import AFV


def test_afv():
    afv = AFV(None)
    afv._encode_image('D:\\data\\face-recognition\\Majeed Khan\\Majeed_Khan_01.jpg')


if __name__ == '__main__':
    test_afv()