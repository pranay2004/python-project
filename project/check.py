def roll():
    text=input("enter a text:")
    n=int(input("enter number of repetitions:"))
    for i in range(n):
        print(text)
roll()
text=input("do you want to run it again?(y/n):")
if text=="y" or "Y":
    for i in range(0):
        roll()
