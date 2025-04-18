from pwn import *

#context.log_level = 'debug'

p = remote("localhost", 9007) #connecting to the challenge with port 9007

line = p.recvline().decode()
while ' - Ready? starting in 3 sec... -' not in line:
    line = p.recvline().decode()  #receiving until we get to the line before 'N = ...   C = ...'

p.recvline().decode() #receving the empty line
line = p.recvline().decode() #the line we want.

#calculating n and c
N = int(line.split('N=')[1].split(' ')[0])
C = int(line.split('C=')[1])
print(f"N = {N}   C = {C}")

left, right = 0, N
mid = left + (right-left) // 2


#binary search!! r, l and mid pointers. each attempt we gonna send half of the the numbers and receive the result, if it's even, the target coin
#is in the other half, so we adjust the left ptr to the mid, if it's odd we adjust the right pointer.
for _ in range(100):

    for i in range(C):
        attempt = b""
        for j in range(left, mid):
            attempt += f"{j} ".encode()
        p.sendline(attempt)
        res = int(p.recvline().decode())
        if res % 2 == 0: #the right coing is not on the left half
            left = mid
        else:
            right = mid

        mid = left + (right-left) // 2

    p.sendline(str(left).encode()) #sending the result
    print(p.recvline().decode())



    line = p.recvline().decode()
    if 'N=' not in line:  #if it's the last one we want to break and receive the flag
        break

    N = int(line.split('N=')[1].split(' ')[0])
    C = int(line.split('C=')[1])
    print(f"N = {N}   C = {C}")

    left, right = 0, N
    mid = left + (right-left) // 2



print(p.recv().decode())
