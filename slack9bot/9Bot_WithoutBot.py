from getPosts import checkCommand

command = input("Entrer sections: ")
posts = checkCommand(command)
for p in posts:
    print(p)
