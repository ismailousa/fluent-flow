import streamlit.web.cli as stcli
import sys


def main():
    sys.argv = ["streamlit", "run", "src/fluent_flow/streamlit/app.py"]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
