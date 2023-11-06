from dataclasses import dataclass
from typing import Union, _SpecialForm, _type_check  # , TypeVar, Generic

# T = TypeVar("T")


# @dataclass(frozen=True)
# class Succes(Generic[T]):
#     value: T


@dataclass(frozen=True)
class Fail:
    type: str


@_SpecialForm
def Result(self, parameters):
    """Result type.

    Result[X] is equivalent to Union[Fail, Succes].
    """
    arg = _type_check(parameters, f"{self} requires a single type.")
    return Union[arg, type(Fail)]
