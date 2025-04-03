class Server:
    def __init__(self, env):
        self.reqres = {
            "dev": "https://reqres.in",
            "rc": "http://127.0.0.1:8002",
        }[env]
