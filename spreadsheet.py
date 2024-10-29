
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
                    # Check if all parts of the expression are valid integers or operators
                    if all(part.strip().replace('.', '', 1).isdigit() or part.strip() in {'+', '-', '*', '/'} for part in expression.replace('+', ' + ').replace('-', ' - ').replace('*', ' * ').replace('/', ' / ').split()):
                        result = eval(expression)
                        if isinstance(result, int):
                            return result
                        else:
                            return "#Error"
                    else:
                        return "#Error"
                except:
                    return "#Error"
        return "#Error"

