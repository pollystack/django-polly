from fabric import Connection


class Connector:

    def __init__(self, host, user, port, key_path):
        self.host = host
        self.user = user
        self.port = port
        self.key_path = key_path

    def start(self):
        conn = Connection(
            host=self.host,
            user=self.user,
            port=self.port,
            connect_kwargs={
                "key_filename": self.key_path
            }
        )
        result = conn.run('uname -s', hide=True)
        msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
        print(msg.format(result))
        return conn
