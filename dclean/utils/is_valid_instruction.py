from dclean.utils.types import Instruction


def is_valid_instruction(value: str) -> bool:
    try:
        Instruction(value)
        return True
    except ValueError:
        return False
