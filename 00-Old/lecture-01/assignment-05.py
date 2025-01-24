user_dic = {
    'username' : 'bariserkus',
    'name' : 'Baris',
    'email' : 'baris@hotmail.com',
}

print (user_dic)
print (user_dic.get('username'))

user_dic['married'] = True
print (user_dic)

print (len(user_dic))

for key, value in user_dic.items():
    print (key, " : ", value)

print (user_dic.values())

print (user_dic.keys())
