from src.mapper.form8_mapper import map_to_form8
from src.mapper.template2_mapper import map_to_template2


MAPPERS = {
    "form8": map_to_form8,
    "template2": map_to_template2
}


def map_cv(data, template):

    mapper = MAPPERS.get(template)

    if not mapper:
        raise ValueError(
            f"No mapper found for {template}"
        )

    return mapper(data)