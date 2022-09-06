import random
exec(open("network.py").read())

def unparse(S):
    out = ""
    for s in S:
        for c in s:
            out += c
    
    return out.title()

def gen():
    last_start = 0
    out = []
    t = (" ", " ")
    n = "."
    while n != " ":
        space_score = 1
        word_length = len(out) - last_start
        if word_length <= 3:
            space_score = 0
        elif word_length >= 8:
            space_score = (word_length-6)**2
        cnt = 10000
        for x in [" ", "-"]:
            if x in network[t]:
                cnt += (space_score-1) * network[t][x]

        if cnt < 1:
            n = " "
        else:
            pick = random.randint(1, cnt)
            passed = 0
            for i in network[t].keys():
                if i in [" ", "-"]:
                    passed += space_score * network[t][i]
                else:
                    passed += network[t][i]
                if passed < pick:
                    continue
                n = i
                break
        out.append(n)
        t = (t[1], n)
        if n in [" ", "-"]:
            last_start = len(out)
    return unparse(out).strip()

def import_data():
    f = open("data.txt", "r")
    out = []
    for x in f:
        out.append(x.strip())
    f.close()
    return out

def game():
        real_names = import_data()
        out = ""
        real = True
        if random.random() < 0.5:
            while (out := gen()) in real_names:
                pass
            real = False
        else:
            out = random.choice(real_names)

        print(out)

        ans_str = input()
        ans = True

        if ans_str.lower() in ["y", "t", "yes", "tak"]:
            ans = True
        else:
            ans = False

        return ans == real

def multigame():
    print("You will be given 20 names of cities of Poland, some of which are artificially generated. Can you guess which ones are those?")
    print("Instructions: after each name write y/yes, if you think it's real and n/no otherwise.")
    score = 0
    for i in range(20):
        if game():
            score += 1

    print("You have guessed correctly", score, "cities out of 20.", sep=" ", end=" ")
    if score >= 15:
        print("Well done!")
    else:
        print("Better next time!")

multigame()
