from zipfile import ZipFile
import codecs
import temp


fout = open("top-of-85-users.html", "w", encoding='utf-8')
f_users = codecs.open('Users.xml', encoding='utf-8')
f_comm = codecs.open('Comments.xml', encoding='utf-8')
f_posts = codecs.open('Posts.xml', encoding='utf-8')
TOP_USERS = 85


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


def read_posts():
    posts = set()

    for post in f_posts.readlines():
        categories_post = del_space(post)
        score = None
        post_id = None

        for elem in categories_post:
            if elem.startswith('Score='):
                score = elem[7:-1]

                if score.isdigit():
                    score = int(score)
                else:
                    score = None
                    break

            if elem.startswith('Id='):
                post_id = elem[4:-1]

                if post_id.isdigit():
                    post_id = int(post_id)
                else:
                    post_id = None
                    break

        if (score is None) or (score <= 20) or (post_id is None):
            continue

        posts.add(post_id)

    return posts


def read_comments(users, posts):
    for new_comm in f_comm.readlines():
        categories_comm = del_space(new_comm)
        user_id = None
        post_id = None

        for elem in categories_comm:
            if elem.startswith('UserId='):
                user_id = int(elem[8:-1])

            if elem.startswith('PostId='):
                post_id = int(elem[8:-1])

        if (user_id in users.keys()) and (post_id in posts):
            users[user_id].comm += 1

    return users


def generate_table(users, rate):
    print(temp.STYLE_TEMPLATE, file=fout)
    print(temp.TABLE_TEMPLATE, file=fout)

    for i in range(TOP_USERS):
        table_user = users[rate[i][1]]
        print("<tr>", file=fout)
        print("<th>{0}</th>".format(i + 1), file=fout)
        print("<th> <a href='https://electronics.stackexchange.com/users/{0}'</a>".format(table_user.id_user),  table_user.d_name, "</th>", sep='', file=fout)
        print("<th>{0}</th>".format(table_user.age), file=fout)
        print("<th>{0}</th>".format(table_user.comm), file=fout)
        print("</tr>", file=fout)

    print(temp.TABLE_END, file=fout)


_users = read_comments(read_users(), read_posts())

_rate = []
for id_us in _users.keys():
    _rate.append((_users[id_us].comm, int(id_us)))
_rate.sort(reverse=True)

generate_table(_users, _rate)
