class User:
    count = 0

    @staticmethod
    def increase():
        User.count += 1   

User.increase()
print(User.count)  # 1
