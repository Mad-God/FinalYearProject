tc = int(input(""))
answers = []
for testCase in range(tc):
    nt = int(input(""))

    tweet = []
    users = []
    uset = []
    ans = {}
    for i in range(nt):
        t = input("")
        tweet.append(t)
        users.append(tweet[-1].split(" ")[0])

    user = set(users)
    c = 0
    while len(users):
        u = max(users, key = users.count)
        c2 = users.count(u)
        if c2 >= c:
            ans[u] = c2
            c = c2
        users.remove(u)
        

    uset = list(ans.keys())
    uset.sort()
    for i in uset:
            answers.append(i + " " + str(ans[i]))

for i in answers:
    print(i)