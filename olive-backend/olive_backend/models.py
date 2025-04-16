from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Dog:
    breed: str
    image: Optional[str] = None
    
    def from_json(json_data: dict) -> "Dog":
        """
        Create a Dog instance from JSON data.
        """
        return Dog(**json_data)

@dataclass
class DogResponse:
    data: List[Dog] = field(default_factory=list)
    page: int = 1
    next_page: Optional[int] = None
    total: int = 0
