import subprocess


def main():
    subprocess.run(["black", "./nad_ch"])
    subprocess.run(["black", "./alembic"])
    subprocess.run(["black", "./tests"])


if __name__ == "__main__":
    main()
