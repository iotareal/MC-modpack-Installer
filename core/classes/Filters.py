from enum import Enum

class Filters:
    def __init__(self):
        self._active_filters = {}

    def add_filter(self, facet_name: str, value):
        if facet_name not in self._active_filters:
            self._active_filters[facet_name] = set()
        
        self._active_filters[facet_name].add(value)
        print(f"Added filter: {facet_name}={value}")

    def remove_filter(self, facet_name: str, value):
        if facet_name in self._active_filters and value in self._active_filters[facet_name]:
            self._active_filters[facet_name].remove(value)
            # If the set becomes empty, remove the facet key itself
            if not self._active_filters[facet_name]:
                del self._active_filters[facet_name]
            print(f"Removed filter: {facet_name}={value}")

    def clear(self):
        self._active_filters.clear()
        print("All filters cleared.")

    def apply(self) -> list:
        final_facets = []
        for name, values in self._active_filters.items():
            or_group = []
            for value in values:
                str_value = value.value if isinstance(value, Enum) else str(value)
                or_group.append(f"{name}:{str_value}")
            
            final_facets.append(or_group)
            
        return final_facets