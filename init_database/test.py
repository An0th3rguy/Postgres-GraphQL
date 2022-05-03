# from sqlalchemy.orm import sessionmaker

# # SessionMaker = sessionmaker(bind=engine)
# # session = SessionMaker()

# import random
# import string

# def get_random_string(length):
#     letters = string.ascii_lowercase
#     result = ''.join(random.choice(letters) for i in range(length))
#     return result 

# def randomUser():
#     surNames = [
#         'Novák', 'Nováková', 'Svobodová', 'Svoboda', 'Novotná',
#         'Novotný', 'Dvořáková', 'Dvořák', 'Černá', 'Černý', 
#         'Procházková', 'Procházka', 'Kučerová', 'Kučera', 'Veselá',
#         'Veselý', 'Horáková', 'Krejčí', 'Horák', 'Němcová', 
#         'Marková', 'Němec', 'Pokorná', 'Pospíšilová','Marek'
#     ]

#     names = [
#         'Jiří', 'Jan', 'Petr', 'Jana', 'Marie', 'Josef',
#         'Pavel', 'Martin', 'Tomáš', 'Jaroslav', 'Eva',
#         'Miroslav', 'Hana', 'Anna', 'Zdeněk', 'Václav',
#         'Michal', 'František', 'Lenka', 'Kateřina',
#         'Lucie', 'Jakub', 'Milan', 'Věra', 'Alena'
#     ]

#     name1 = random.choice(names)
#     name2 = random.choice(names)
#     name3 = random.choice(surNames)
#     return {'name': f'{name1} {name2}', 'surname': f'{name3}', 'email': f'{name1}.{name2}.{name3}@university.world'}

# def PopulateUsers(count=10, group=None):
#     for i in range(count):
#         userNames = randomUser()
#         print(userNames)
#         #crudUserCreate(db=session, user=UserModel(**userNames))
        
# # session = SessionMaker()
# PopulateUsers(10)
# # session.close()

price = str(2399)
print(price)

price = f"{(float(price) / 23.5):.0f}"

print(type(price))

print(price)