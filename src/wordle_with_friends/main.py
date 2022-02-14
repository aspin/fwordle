from src.wordle_with_friends import server


def main():
    app = server.build()
    app.run()


if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(main())
    main()
