import argparse


def parser_argument():
    parser = argparse.ArgumentParser(
        prog='page-loader',
        usage='%(prog)s [options] <url>',
        description='PageLoader is a command \
        line utility that downloads pages from \
        the Internet and stores them on your computer.'
    )
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output',
                        type=str,
                        default="",
                        help='output dir (default: current directory)')
    args = parser.parse_args()
    return args
