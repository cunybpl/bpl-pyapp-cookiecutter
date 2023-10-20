import orjson


def orjson_serializer(obj: object) -> str:
    """Override internal serializer to handle numpy

    Args:
        obj (object): Any obj

    Returns:
        str: serialized string
    """
    return orjson.dumps(obj, option=orjson.OPT_SERIALIZE_NUMPY).decode()
