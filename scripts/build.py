import sys
from hangulify import build_fonts


def print_usage():
    """사용법 안내 메시지를 출력합니다."""
    print(f"python {sys.argv[0]} <subcommand>\n")
    print("subcommand:")
    print("    build  : 폰트를 병합하고 출력합니다.")


def main():
    if len(sys.argv) != 2 or sys.argv[1] != "build":
        print_usage()
        exit(1)

    build_fonts()


if __name__ == "__main__":
    main()
