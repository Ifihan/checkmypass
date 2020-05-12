import requests
import hashlib
import sys

def request_api(password_char):
    url = 'https://api.pwnedpasswords.com/range' + password_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}.Check the api and try again.')
    return response

def get_password(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_5, tail = sha1password[:5], sha1password[5:]
    res = request_api(first_5)
    print (res)
    return get_password(response, tail)

def main(args):
    for password in args:
        count = pwned_check(password)
        if count > 10:
            print(f'{password} was found {count} times... you might have to change password')
        else:
            print(f'{password} was NOT found. Carry on!')
    return 'done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
