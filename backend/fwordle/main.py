from fwordle import server, config


def main():
    app = server.build()
    app.run()


if __name__ == "__main__":
    config.setup_logger()
    main()