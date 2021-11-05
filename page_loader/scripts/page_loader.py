from page_loader.pageloader import page_loader
from page_loader.cli import parser_argument
from http.client import HTTPException
import sys


def main():
    args = parser_argument()
    print(page_loader(args.url, args.output))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
    except OSError:
        sys.exit(3)
    except HTTPException:
        sys.exit(4)
