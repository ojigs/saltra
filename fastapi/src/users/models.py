from pydantic_core import core_schema
from bson.objectid import ObjectId
from typing import Callable, Any

# Custom objectid handling for pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_convert_objectid(input_value):
            if isinstance(input_value, ObjectId):
                return input_value
            if isinstance(input_value, str):
                return ObjectId(input_value)
            raise ValueError("Invalid ObjectId")

        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.no_info_plain_validator_function(validate_convert_objectid)
        ])