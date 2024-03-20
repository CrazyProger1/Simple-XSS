import toml
from pydantic import BaseModel

from ..types import (
    BaseLoader
)
from ..exceptions import FileFormatError


class TOMLLoader(BaseLoader):
    def load(self, file: str, schema: type[BaseModel], **kwargs) -> BaseModel:
        try:
            data: dict = toml.load(file)
            return schema.model_validate(data, **kwargs)
        except toml.TomlDecodeError as e:
            raise FileFormatError(file=file, msg=str(e))

    def save(self, file: str, data: BaseModel, **kwargs):
        with open(file, 'w', encoding='utf-8') as f:
            data: dict = data.model_dump(**kwargs)
            toml.dump(data, f)
