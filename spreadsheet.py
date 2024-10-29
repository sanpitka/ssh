
class SpreadSheet:

    def __init__(self):
        self._cells = {}

    def set(self, cell: str, value: str) -> None:
        self._cells[cell] = value

    def get(self, cell: str) -> str:
        return self._cells.get(cell, '')

    def evaluate(self, cell: str, visited=None) -> int | str:
        if visited is None:
            visited = set()

        if cell in visited:
            return "#Circular"

        visited.add(cell)

        value = self.get(cell)
        if value.isdigit():
            return int(value)
        elif value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        elif value.startswith("="):
            if value[1:].isdigit():
                return int(value[1:])
            elif value[1:].startswith("'") and value[1:].endswith("'"):
                return value[2:-1]
            elif value[1:].isidentifier():
                referenced_cell = value[1:]
                if referenced_cell in self._cells:
                    result = self.evaluate(referenced_cell, visited)
                    visited.remove(cell)
                    return result
            else:
                try:
                    # Evaluate the expression safely
                    expression = value[1:].replace('&', '+')
                    if '/' in expression:
                        # Check for division by zero
                        if '/0' in expression:
                            return "#Error"
                    # Replace cell references in the expression with their evaluated results
                    for ref_cell in self._cells:
                        if ref_cell in expression:
                            ref_value = self.evaluate(ref_cell, visited)
                            if isinstance(ref_value, str) and ref_value.startswith("#"):
                                return ref_value
                            expression = expression.replace(ref_cell, str(ref_value))
                    result = eval(expression, {"__builtins__": None}, {})
                    if isinstance(result, float) and not result.is_integer():
                        return "#Error"
                    return int(result)
                except:
                    return "#Error"
        return "#Error"

