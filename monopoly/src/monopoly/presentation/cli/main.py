from monopoly.presentation.cli.menu_controller import MenuController


def main() -> None:
    print("=== Monopoly CLI ===")
    controller = MenuController()
    controller.run()


if __name__ == "__main__":
    main()