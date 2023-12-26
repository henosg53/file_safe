def crypt_ui():
    from xcrypt_ui import XCryptUI, XAuth, XConfig
    # app = XCryptUI()
    XAuth()
    # XConfig()


def ui_training():
    from ui_training import TrainingUI, Other
    # app = TrainingUI()
    app = Other()


if __name__ == '__main__':
    crypt_ui()
    # ui_training()
