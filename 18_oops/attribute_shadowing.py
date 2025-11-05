class User:
    name = "Class Level Name"   # Class attribute

u1 = User()
print(u1.name)   # 👉 "Class Level Name" (class se mila)

# Shadowing starts here
u1.name = "Instance Level Name"
print(u1.name)   # 👉 "Instance Level Name" (instance-level ne class-level ko chhupa diya)

# Delete instance attribute
del u1.name
print(u1.name)   # 👉 "Class Level Name" (fallback to class attribute)

# Class Level Name
# Instance Level Name
# Class Level Name