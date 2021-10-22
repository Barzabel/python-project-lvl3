from page_loader.pageloader import page_loader
from page_loader.cli import parser_argument


def main():
    args = parser_argument()
    print(page_loader(args.url, args.output))


if __name__ == '__main__':
    main()
