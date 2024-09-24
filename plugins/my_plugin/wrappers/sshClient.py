class sshClient:
    def __init__(self, ip, credentials, *args, **kwargs):
        print(f"Created connection {ip=}")

    def get_os(self):
        return "Uname executed"
