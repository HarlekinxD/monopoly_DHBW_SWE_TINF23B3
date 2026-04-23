class CommandParser:
    
    VALID_COMMANDS = {"help", "show", "toggle", "roll", "buy", "build", "end", "quit", "bail"}

    def parse(self, raw_command: str) -> tuple[str, list[str]]:
        command = raw_command.strip().lower()

        if not command:
            raise ValueError("Command must not be empty.")

        parts = command.split()
        keyword = parts[0]
        arguments = parts[1:]

        if keyword not in self.VALID_COMMANDS:
            raise ValueError(f"Unknown command: {keyword}")

        return keyword, arguments