from pydantic import AliasGenerator, BaseModel, ConfigDict, alias_generators


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=alias_generators.to_camel),
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
