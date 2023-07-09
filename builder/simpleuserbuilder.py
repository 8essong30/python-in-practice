def main():
    user = UserBuilder() \
        .set_username('john') \
        .set_password('1234') \
        .set_email('john@example.com') \
        .set_first_name('John') \
        .set_last_name('Doe') \
        .build()

    print(user)  # username: john, password: 1234, email: john@example


class User:
    def __init__(self):
        self.username = None
        self.password = None
        self.email = None
        self.first_name = None
        self.last_name = None

    def __str__(self):
        return f"username: {self.username}, password: {self.password}, email: {self.email}, first_name: {self.first_name}, last_name: {self.last_name}"


class UserBuilder:
    def __init__(self):
        self.user = User()

    def set_username(self, username):
        self.user.username = username
        return self

    def set_password(self, password):
        self.user.password = password
        return self

    def set_email(self, email):
        self.user.email = email
        return self

    def set_first_name(self, first_name):
        self.user.first_name = first_name
        return self

    def set_last_name(self, last_name):
        self.user.last_name = last_name
        return self

    def build(self):
        return self.user


if __name__ == "__main__":
    main()
