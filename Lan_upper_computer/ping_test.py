import time
from pythonping import ping

def custom_ping():
    count = 0
    host = "192.168.3.11"  # 要ping的主机
    for response in ping(host, count=5, timeout=0.3):
        print(response)
        time.sleep(0.5)
        count += 1
        if count == 5:
            break

    if response.success:
        print(f"\n{host} is reachable.")
    else:
        print(f"\n{host} is unreachable.")


if __name__ == '__main__':

    custom_ping()

