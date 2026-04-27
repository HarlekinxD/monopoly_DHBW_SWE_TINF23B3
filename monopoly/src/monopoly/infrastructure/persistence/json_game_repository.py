from __future__ import annotations

import json
from pathlib import Path

from monopoly.application.ports.game_repository import GameRepository
from monopoly.domain.entities.game import Game
from monopoly.infrastructure.persistence.game_deserializer import GameDeserializer
from monopoly.infrastructure.persistence.game_serializer import GameSerializer


class JsonGameRepository(GameRepository):
    def __init__(self, file_path: str | Path) -> None:
        # Ziel datei fuer savegames
        self._file_path = Path(file_path)
        self._serializer = GameSerializer()
        self._deserializer = GameDeserializer()

    def save(self, game: Game) -> None:
        # In dict wandeln und als JSON wegschreiben
        payload = self._serializer.serialize(game)
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        self._file_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def load(self) -> Game | None:
        # Wenn nix da ist -> None, damit UseCase entscheiden kann
        if not self._file_path.exists():
            return None

        payload = json.loads(self._file_path.read_text(encoding="utf-8"))
        return self._deserializer.deserialize(payload)
