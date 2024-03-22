from enum import Enum

from pydantic import (
    BaseModel,
    Field
)

from simplexss.utils.arguments import SchemedArgumentParser


def test_parse_str_args():
    class Schema1(BaseModel):
        test: str = Field(description='Hello, World!')

    parser = SchemedArgumentParser(
        schema=Schema1
    )
    args = parser.parse_schemed_args(['--test', '123'])

    assert args.test == '123'


def test_parse_int_args():
    class Schema2(BaseModel):
        test: int = Field(description='Hello, World!')

    parser = SchemedArgumentParser(
        schema=Schema2
    )
    args = parser.parse_schemed_args(['--test', '123'])

    assert args.test == 123


def test_parse_str_enum_args():
    class StrEnum(str, Enum):
        A = 'a'
        B = 'b'
        C = 'c'

    class Schema3(BaseModel):
        test: StrEnum

    parser = SchemedArgumentParser(
        schema=Schema3
    )
    args = parser.parse_schemed_args(['--test', 'c'])

    assert args.test == StrEnum.C


def test_parse_int_enum_args():
    class IntEnum1(int, Enum):
        ONE = 1
        TWO = 2
        THREE = 3

    class Schema4(BaseModel):
        test: IntEnum1

    parser = SchemedArgumentParser(
        schema=Schema4
    )
    args = parser.parse_schemed_args(['--test', '2'])

    assert args.test == IntEnum1.TWO


def test_parse_positional_args():
    class Schema5(BaseModel):
        abc: str

    parser = SchemedArgumentParser(
        schema=Schema5,
        positional_arguments=('abc',)
    )

    args = parser.parse_schemed_args(['321'])

    assert args.abc == '321'


def test_parse_short_aliases():
    class Schema6(BaseModel):
        test: str

    parser = SchemedArgumentParser(
        schema=Schema6,
        short_aliases={
            'test': 'b'
        }
    )

    args = parser.parse_schemed_args(['-b', '4444'])
    assert args.test == '4444'


def test_parse_field_aliases():
    class Schema7(BaseModel):
        test: str = Field(alias='ttt')

    parser = SchemedArgumentParser(
        schema=Schema7
    )

    args = parser.parse_schemed_args(['--ttt', '4444'])
    assert args.test == '4444'
