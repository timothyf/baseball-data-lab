"""Player information model."""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class PlayerInfo:
    mlbam_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    link: Optional[str] = None
    active: Optional[bool] = None
    primary_position: Optional[str] = None
    use_name: Optional[str] = None

    @classmethod
    def from_mlb_info(cls, mlb_player_info: Dict[str, Any]) -> "PlayerInfo":
        """Create a ``PlayerInfo`` instance from MLB API data."""
        return cls(
            mlbam_id=mlb_player_info.get("id"),
            first_name=mlb_player_info.get("firstName"),
            last_name=mlb_player_info.get("lastName"),
            link=mlb_player_info.get("link"),
            active=mlb_player_info.get("active"),
            primary_position=mlb_player_info.get("primaryPosition", {}).get("abbreviation"),
            use_name=mlb_player_info.get("useName"),
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "mlbam_id": self.mlbam_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "link": self.link,
            "active": self.active,
            "primary_position": self.primary_position,
            "use_name": self.use_name,
        }

