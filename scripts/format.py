import subprocess


def main():
    subprocess.run(["black", "./alembic", "./nad_ch", "./scripts", "./tests"])


if __name__ == "__main__":
    main()
