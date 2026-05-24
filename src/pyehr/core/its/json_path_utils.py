from pyehr.core.rm.common.archetyped import PyehrInternalPathPredicateType, PyehrInternalProcessedPath


def json_has_path(js_dict, path) -> bool:
    """Return whether a given path exists in an as_json() dict output"""
    if path is None:
        return True
    proc = PyehrInternalProcessedPath(path)
    if proc.is_self_path():
        return True

    next_el = js_dict[proc.current_node_attribute]

    if isinstance(next_el, list):
        if proc.current_node_predicate_type == PyehrInternalPathPredicateType.POSITIONAL_PARAMETER:
            next_el = next_el[int(proc.current_node_predicate)]
        elif proc.current_node_predicate_type == PyehrInternalPathPredicateType.ARCHETYPE_PATH:
            found_match = False
            for el in next_el:
                if el["archetype_node_id"] == proc.current_node_predicate:
                    found_match = True
                    next_el = el
            if not found_match:
                return False

    return json_has_path(next_el, proc.remaining_path)


def json_get_path(js_dict, path):
    """Navigate to a pyehr path within an as_json() dict output"""
    if path is None:
        return js_dict
    proc = PyehrInternalProcessedPath(path)
    if proc.is_self_path():
        return js_dict

    if proc.current_node_attribute not in js_dict:
        raise ValueError(f"Could not find node matching `{proc.current_node_attribute}`")
    next_el = js_dict[proc.current_node_attribute]

    if isinstance(next_el, list):
        if proc.current_node_predicate_type == PyehrInternalPathPredicateType.POSITIONAL_PARAMETER:
            next_el = next_el[int(proc.current_node_predicate)]
        elif proc.current_node_predicate_type == PyehrInternalPathPredicateType.ARCHETYPE_PATH:
            found_match = False
            for el in next_el:
                if el["archetype_node_id"] == proc.current_node_predicate:
                    found_match = True
                    next_el = el
            if not found_match:
                raise ValueError(f"Could not find node matching `{proc.current_node_predicate}` in list")

    return json_get_path(next_el, proc.remaining_path)