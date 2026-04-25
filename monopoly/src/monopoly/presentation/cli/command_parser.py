class CommandParser:
    
    VALID_COMMANDS = {
        "help", "show", "toggle", "roll", "buy", "build", "end", "quit", "bail", "save", "load"
    }

    def parse(self, raw_command: str) -> tuple[str, list[str]]:
        command = raw_command.strip()

        if not command:
            raise ValueError("Command must not be empty.")

        parts = command.split()
        keyword = parts[0].lower()
        arguments = parts[1:]

        if keyword not in self.VALID_COMMANDS:
            raise ValueError(f"Unknown command: {keyword}")

        return keyword, arguments