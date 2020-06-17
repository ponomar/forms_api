_ATTR_TYPE = 'type'
_ATTR_ID = 'id'
_ATTR_NAME = 'name'
_ATTR_VALUE = 'value'
_ATTR_CHECKED = 'checked'


def _process_attributes(attributes):
    mapping = {}
    for key, value in attributes.items():
        key = key.rstrip('_')
        if key in (_ATTR_TYPE, _ATTR_ID, _ATTR_NAME):
            raise ValueError(f'`{key}` is prohibited attribute')

        mapping[key] = value

    return [(k_, v_) for k_, v_ in mapping.items()]


def _join_attributes(attribute_tuples):
    def get_value(x):
        if x is not None:
            return x

        return ''

    return ' '.join(f'{k_}="{get_value(v_)}"' for k_, v_ in attribute_tuples)


def generate_input(input_type, key, value, **attributes) -> str:
    attribute_tuples = [
        (_ATTR_TYPE, input_type),
        (_ATTR_NAME, key),
        (_ATTR_ID, key),
        (_ATTR_VALUE, value),
    ]
    attribute_tuples.extend(_process_attributes(attributes))

    return f'<input {_join_attributes(attribute_tuples)}>'


def generate_checkbox(key, value, **attributes) -> str:
    attribute_tuples = [(_ATTR_NAME, key), (_ATTR_ID, key)]
    if value:
        attribute_tuples.append((_ATTR_CHECKED, 'checked'))

    attribute_tuples.extend(_process_attributes(attributes))

    return f'<input type="checkbox" {_join_attributes(attribute_tuples)}>'


def generate_textarea(key, value, **attributes) -> str:
    attribute_tuples = [(_ATTR_NAME, key), (_ATTR_ID, key)]
    attribute_tuples.extend(_process_attributes(attributes))

    if value is None:
        value = ''

    return f'<textarea {_join_attributes(attribute_tuples)}>{value}</textarea>'


def generate_select(key, options, multiple: bool = False, **attributes) -> str:
    attribute_tuples = [(_ATTR_NAME, key), (_ATTR_ID, key)]
    attribute_tuples.extend(_process_attributes(attributes))

    options_ready = []
    for k_, v_, s_ in options:
        if k_ is None:
            k_ = ''

        if s_:
            selected = ' selected="selected"'
        else:
            selected = ''

        options_ready.append(f'<option value="{k_}"{selected}>{v_}</option>')

    multiple = ' multiple' if multiple else ''

    return (
        f'<select {_join_attributes(attribute_tuples)}{multiple}>'
        f'{"".join(options_ready)}'
        f'</select>'
    )


def generate_submit(key, **attributes) -> str:
    attribute_tuples = [(_ATTR_NAME, key), (_ATTR_ID, key)]
    attribute_tuples.extend(_process_attributes(attributes))

    return f'<input type="submit" {_join_attributes(attribute_tuples)}>'


def html(field, **attributes) -> str:
    if field['input_type'] == 'textarea':
        return generate_textarea(
            key=field['key'],
            value=field['value'],
            **attributes
        )
    elif field['input_type'] == 'checkbox':
        return generate_checkbox(
            key=field['key'],
            value=field['value'],
            **attributes
        )
    elif field['input_type'] == 'select':
        return generate_select(
            key=field['key'],
            value=field['value'],
            options=field['options'],
            multiple=field['type'] == 'select_multiple',
            **attributes
        )
    elif field['input_type'] == '':
        return generate_submit(
            key=field['key'],
            **attributes
        )
    else:
        return generate_input(
            input_type=field['input_type'],
            key=field['key'],
            value=field['value'],
            **attributes
        )
