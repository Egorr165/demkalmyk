from dataclasses import dataclass


@dataclass
class UserInfo:
    user_id: int | None
    full_name: str
    role_name: str