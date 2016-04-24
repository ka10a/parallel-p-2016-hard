from zipfile import ZipFile
import codecs
import temp


fout = open("top-of-150-users.html", "w", encoding='utf-8')
f_users = codecs.open('Users.xml', encoding='utf-8')
f_comm = codecs.open('Comments.xml', encoding='utf-8')


class User:
    d_name = ''
    age = None
    id_user = None
    comm = 0

    def __init__(self, name, age, id_user):
        self.d_name = name
        self.age = age
        self.id_user = id_user
        self.comm = 0


def del_space(s):
    a = []
    i = 0
    while i < len(s):
        k = i
        while (i != len(s)) and (s[i] != ' '):
            i += 1
        a.append(s[k:i])
        i += 1
    return a


def read_users():
    users = {}
    for new_user in f_users.readlines():
        categories_user = del_space(new_user)
        name = ''
        age = None
        id_user = None

        for i in range(len(categories_user)):
            elem = categories_user[i]

            if elem.startswith('Id='):
                id_user = elem[4:-1]

                if id_user.isdigit():
                    id_user = int(id_user)
                else:
                    id_user = None
                    break

            if elem.startswith('DisplayName='):
                if categories_user[i + 1].startswith('LastAccessDate='):
                    name = elem[13:-1]
                    continue

                name = elem[13:]
                k = i
                while not categories_user[k + 1].startswith('LastAccessDate='):
                    name += " "
                    name += categories_user[k + 1]
                    k += 1
                name = name[:-1]

            if elem.startswith('Age='):
                age = elem[5:-1]

                if age.isdigit():
                    age = int(age)
                else:
                    age = None
                    break

        if (name == '') or (age is None) or (id_user is None):
            continue

        if (20 <= age) and (age <= 25):
            users[id_user] = User(name, age, id_user)

    return users


def read_comments(users):
    for new_comm in f_comm.readlines():
        categories_comm= del_space(new_comm)
        id_user = None

        for elem in categories_comm:
            if elem.startswith('UserId'):
                id_user = int(elem[8:-1])

        if id_user in users:
            users[id_user].comm += 1

    return users


def generate_table(users, rate):
    print(temp.STYLE_TEMPLATE, file=fout)
    print(temp.TABLE_TEMPLATE, file=fout)

    for i in range(150):
        table_user = users[rate[i][1]]
        print("<tr>", file=fout)
        print("<th>{0}</th>".format(i + 1), file=fout)
        print("<th> <a href='https://electronics.stackexchange.com/users/{0}'</a>".format(table_user.id_user),  table_user.d_name, "</th>", sep='', file=fout)
        print("<th>{0}</th>".format(table_user.age), file=fout)
        print("<th>{0}</th>".format(table_user.comm), file=fout)
        print("</tr>", file=fout)

    print(temp.TABLE_END, file=fout)


_users = read_comments(read_users())

_rate = []
for id_us in _users.keys():
    _rate.append((_users[id_us].comm, int(id_us)))
_rate.sort(reverse=True)

generate_table(_users, _rate)
