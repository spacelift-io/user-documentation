#!/usr/bin/env python3
import json
import requests

def get_example_value(field_name, field_schema, depth=0):
    """
    Generate example values based on field schema.
    Returns descriptive strings for all field types.
    """
    # Get description if available
    description = field_schema.get('description', f'value for {field_name}')

    # Handle references first
    if '$ref' in field_schema:
        ref_path = field_schema['$ref']
        ref_name = ref_path.split('/')[-1]
        return f"string - see {ref_name} definition - {description}"

    # Handle anyOf (union types)
    if 'anyOf' in field_schema:
        for option in field_schema['anyOf']:
            if option.get('type') != 'null':
                return get_example_value(field_name, option, depth)
        return None

    # Handle allOf (combined schemas)
    if 'allOf' in field_schema:
        result = {}
        for sub_schema in field_schema['allOf']:
            sub_value = get_example_value(field_name, sub_schema, depth)
            if isinstance(sub_value, dict):
                result.update(sub_value)
        return result if result else f"string - {description}"

    # Handle oneOf (mutually exclusive)
    if 'oneOf' in field_schema:
        # Return the first option as example
        return get_example_value(field_name, field_schema['oneOf'][0], depth)

    field_type = field_schema.get('type')

    # Handle array types
    if isinstance(field_type, list):
        # Multiple possible types, prefer non-null
        for t in field_type:
            if t != 'null':
                field_type = t
                break

    if field_type == 'object':
        if 'properties' in field_schema:
            obj = {}
            for prop_name, prop_schema in field_schema['properties'].items():
                prop_value = get_example_value(prop_name, prop_schema, depth + 1)
                if prop_value is not None:
                    obj[prop_name] = prop_value
            return obj
        else:
            return f"object - {description}"
    elif field_type == 'array':
        items_schema = field_schema.get('items', {})
        item_example = get_example_value('item', items_schema, depth + 1)
        return [item_example] if item_example else []
    elif field_type == 'string':
        if 'enum' in field_schema:
            return f"string - {description} - one of: {', '.join(field_schema['enum'])}"
        elif 'const' in field_schema:
            return field_schema['const']
        return f"string - {description}"
    elif field_type == 'boolean':
        return f"boolean - {description}"
    elif field_type == 'integer':
        return f"integer - {description}"
    elif field_type == 'number':
        return f"number - {description}"
    else:
        return f"string - {description}"


def resolve_ref(schema, ref_path):
    """Resolve a $ref path in the schema."""
    parts = ref_path.split('/')
    current = schema
    for part in parts:
        if part == '#':
            current = schema
        elif part == '$defs':
            current = current.get('$defs', {})
        else:
            current = current.get(part, {})
    return current


def generate_example_from_schema(policy_name, policy_schema, full_schema):
    """Generate example input for a policy type."""
    input_schema = policy_schema.get('input', {})

    # Start building the example
    example = {}

    # Handle allOf at the top level
    if 'allOf' in input_schema:
        for sub_schema in input_schema['allOf']:
            sub_example = process_schema_level(sub_schema, full_schema, policy_name)
            if isinstance(sub_example, dict):
                # Merge dictionaries
                for key, value in sub_example.items():
                    if key not in example:
                        example[key] = value

    # Handle properties at the top level
    if 'properties' in input_schema:
        props_example = process_properties(input_schema['properties'], full_schema)
        example.update(props_example)

    # Handle oneOf at the top level (choose first option for example)
    if 'oneOf' in input_schema:
        first_option = process_schema_level(input_schema['oneOf'][0], full_schema, policy_name)
        if isinstance(first_option, dict):
            example.update(first_option)

    return example


def process_schema_level(schema, full_schema, context=""):
    """Process a schema level and return example data."""
    result = {}

    # Handle oneOf - choose first option
    if 'oneOf' in schema:
        return process_schema_level(schema['oneOf'][0], full_schema, context)

    # Handle allOf - merge all
    if 'allOf' in schema:
        for sub_schema in schema['allOf']:
            sub_result = process_schema_level(sub_schema, full_schema, context)
            if isinstance(sub_result, dict):
                result.update(sub_result)
        return result

    # Handle properties
    if 'properties' in schema:
        props = process_properties(schema['properties'], full_schema)
        result.update(props)

    return result


def process_properties(properties, full_schema):
    """Process properties and generate example values."""
    result = {}
    for prop_name, prop_schema in properties.items():
        value = generate_value(prop_name, prop_schema, full_schema)
        if value is not None:
            result[prop_name] = value
    return result


def generate_value(field_name, schema, full_schema):
    """Generate a value for a field based on its schema."""
    # Handle $ref
    if '$ref' in schema:
        ref_path = schema['$ref']
        resolved = resolve_ref(full_schema, ref_path)
        ref_name = ref_path.split('/')[-1]

        # For complex objects, expand them
        if 'properties' in resolved:
            return process_properties(resolved['properties'], full_schema)
        else:
            # Recursively handle the resolved schema to get the correct type
            return generate_value(field_name, resolved, full_schema)

    # Handle anyOf - prefer non-null
    if 'anyOf' in schema:
        for option in schema['anyOf']:
            if option.get('type') != 'null':
                return generate_value(field_name, option, full_schema)
        return None

    # Handle allOf - merge
    if 'allOf' in schema:
        result = {}
        for sub_schema in schema['allOf']:
            value = generate_value(field_name, sub_schema, full_schema)
            if isinstance(value, dict):
                result.update(value)
        return result if result else None

    # Handle oneOf - choose first
    if 'oneOf' in schema:
        return generate_value(field_name, schema['oneOf'][0], full_schema)

    field_type = schema.get('type')
    description = schema.get('description', f'{field_name}')

    # Handle union types
    if isinstance(field_type, list):
        for t in field_type:
            if t != 'null':
                field_type = t
                break

    # Generate value based on type
    if field_type == 'object':
        if 'properties' in schema:
            return process_properties(schema['properties'], full_schema)
        else:
            return f"object - {description}"
    elif field_type == 'array':
        items_schema = schema.get('items', {})
        if not items_schema:
            return []
        item_example = generate_value('item', items_schema, full_schema)
        return [item_example] if item_example is not None else []
    elif field_type == 'string':
        if 'enum' in schema:
            return f"string - {description} - one of: {', '.join(str(e) for e in schema['enum'])}"
        elif 'const' in schema:
            return schema['const']
        return f"string - {description}"
    elif field_type == 'boolean':
        return f"boolean - {description}"
    elif field_type == 'integer':
        return f"integer - {description}"
    elif field_type == 'number':
        return f"number - {description}"
    else:
        return f"string - {description}"


def main():
    # Fetch the schema from the URL
    print("Fetching policy contract schema from https://app.spacelift.io/.well-known/policy-contract.json...")

    response = requests.get("https://app.spacelift.io/.well-known/policy-contract.json")
    response.raise_for_status()

    schema = response.json()
    print("Schema loaded successfully.")

    policy_types = schema['policyTypes']

    # Generate example for each policy type
    for policy_name, policy_schema in policy_types.items():
        print(f"Generating example for {policy_name} policy...")

        example = generate_example_from_schema(policy_name, policy_schema, schema)

        # Write to file
        output_file = f'policy_inputs/{policy_name.lower()}_input.json'
        with open(output_file, 'w') as f:
            json.dump(example, f, indent=2)

        print(f"  Created {output_file}")

    print("\nAll policy input examples created successfully!")


if __name__ == '__main__':
    main()
