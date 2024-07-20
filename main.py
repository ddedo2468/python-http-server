import sys
from server import HTTPServer


def main():
    print("Logs from your program will appear here!")

    if len(sys.argv) > 1 and sys.argv[1] == "--directory" and len(sys.argv) > 2:
        directory = sys.argv[2]
    else:
        directory = "/tmp"

    server = HTTPServer("localhost", 4221, directory)
    server.start()


if __name__ == "__main__":
    main()
