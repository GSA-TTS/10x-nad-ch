import subprocess


def main():
    subprocess.run(["black", "./nad_ch", "./alembic", "./tests"])

if __name__ == "__main__":
    main()
