from ssl_check import SSLCheck
import csv
from pathlib import Path
import concurrent.futures


HOST_URL_FILE = Path(__file__).parent / '../files/hosts.csv'

def main():
    print("Main function")
    hosts = get_host_urls()
    get_hosts_certificate_info(hosts)

def get_host_urls():

    hosts = []
    with open(HOST_URL_FILE) as csv_file:
        csv_read = csv.reader(csv_file,delimiter=",")
        next(csv_read,None)
        hosts = [tuple(row) for row in csv_read]
        # for row in csv_read:
        #     print(row)
    return hosts


def get_hosts_certificate_info(hosts):
    # for host in hosts:
    #     sslcheck = SSLCheck(host[0], int(host[1]))
    #     sslcheck.print_host_info()

    ssl_check_objs = [SSLCheck(host[0], int(host[1])) for host in hosts]

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for ssl_check in ssl_check_objs:
            executor.submit(ssl_check.print_host_info())


if __name__ == "__main__":
    main()
