import argparse
from zippyshare_downloader import Zippyshare
from zippyshare_downloader.utils import check_valid_zippyshare_url

def main():
    parser = argparse.ArgumentParser(description='Download file from zippyshare directly from python')
    parser.add_argument('ZIPPYSHARE_URL', type=check_valid_zippyshare_url, help='Zippyshare URL')
    parser.add_argument('--no-download', action='store_true', help='No download file')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose')
    parser.add_argument('--replace', action='store_true', help='Replace file if exist')
    parser.add_argument('--progress-bar', action='store_true', help='Enable progress bar')
    args = parser.parse_args()
    z = Zippyshare(
        progress_bar=args.progress_bar,
        replace=args.replace,
        verbose=args.verbose
    )
    if args.no_download:
        print(z.extract_info(args.ZIPPYSHARE_URL, download=False))
    else:
        print(z.extract_info(args.ZIPPYSHARE_URL, download=True))

if __name__ == "__main__":
    main()


