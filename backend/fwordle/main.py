from fwordle import server, config
from fwordle.config import cli


def main():
    app = server.build(cli.parse_args())
    app.run()


if __name__ == "__main__":
    config.setup_logger()
    main()
