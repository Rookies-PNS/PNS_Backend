import dataclasses


@dataclasses.dataclass(frozen=True)
class Password:
    pw: str
