python script:

*****************************************************************************
import hashlib
import itertools
import string

def find_md5_prefix(target_prefix):
    chars = string.ascii_letters + string.digits  # Possible characters to try
    for length in range(1, 10):  # Adjust the range for longer searches
        for candidate in itertools.product(chars, repeat=length):
            candidate_str = ''.join(candidate)
            md5_hash = hashlib.md5(candidate_str.encode()).hexdigest()
            if md5_hash.startswith(target_prefix):
                return candidate_str, md5_hash

result = find_md5_prefix("537500")
print("Matching String:", result[0])
print("MD5 Hash:", result[1])

****************************************************************************

this python script gives an input that generate an md5 hash that start with 537500.
537500 bytes:
\x53\x75\x00

\x00 is a null-terminator, which mean the end of a string. when strmcp wil compare the 2 hashes, it will stop at the null terminator. we'll run the script and get: "bzaEp". if we run the challenge:

nc pwnable.co.il 9006, and provide the input it won't work, because when we provide the input the code use theread function to gets it, the problem is - when we press enter, at the end our string a new-line character is appended, we don't want that. so we'll use the echo command with '-n', so no additinal character will be addd:

echo -n "bzaEp" | nc pwnable.co.il 9006

Flag MD5:
537500469ddfc5b29e9379cdcc2f3c86
Enter your guess: Congrats!!!
PWNIL{How_the_hell_did_you_find_this_collision?30105270}


boom!! got the flag :)
