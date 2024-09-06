import requests

if __name__ == '__main__':
    print("Hello World!")
    r = requests.get("https://www.charlotte.edu/")
    if r.status_code != 200:
        print("Something went wrong!")