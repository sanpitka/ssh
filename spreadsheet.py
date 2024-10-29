
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
                # Handle cell reference after "="
                referenced_cell = value[1:]
                if referenced_cell in self._cells:
                    result = self.evaluate(referenced_cell, visited)
                    visited.remove(cell)
                    return result
            else:
                try:
                    # Evaluate arithmetic expressions
                    expression = value[1:]
                    # Replace cell references in the expression with their evaluated results
                    for part in self._cells:
                        if part in expression:
                            evaluated_value = self.evaluate(part, visited)
                            if isinstance(evaluated_value, str) and evaluated_value.startswith("#"):
                                return evaluated_value
                            expression = expression.replace(part, str(evaluated_value))
                    # Evaluate the expression using eval
                    result = eval(expression)
                    if isinstance(result, int):
                        return result
                except:
                    return "#Error"
        return "#Error"

