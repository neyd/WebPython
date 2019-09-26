from werkzeug.security import generate_password_hash, check_password_hash


class UserNow:
    def __init__(self, username, ip):
        secret_key = "seASdwe123asdWqKmnn"
        self.user = username
        self.ip_address = ip
        self.hash_for_user = generate_password_hash("{}{}{}".format(username, ip, secret_key), "sha256")

    def getAll(self):
        return {'username': self.user, 'hash': self.hash_for_user}

    def get_hash(self):
        return self.hash_for_user

    def get_name(self):
        return self.user

    def get_ip(self):
        return self.ip_address
