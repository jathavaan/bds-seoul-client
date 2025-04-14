# Naming- and code conventions

> [!NOTE]  
> To ensure a clean and easy to read codebase it is important to follow naming conventions.

## Naming Conventions

- Variables, functions, and methods: `snake_case`
- Classes and exceptions: `CamelCase`
- Constants: `UPPERCASE_WITH_UNDERSCORES`

## Type Hinting

Type hinting helps with code readability and can assist in catching bugs. Here are examples of how to use type hinting
in function declarations:

```python
def add(a: int, b: int) -> int:
    return a + b

def concatenate(strings: list[str]) -> str:
    return "".join(strings)

def process_data(data: dict[str, int]) -> dict[str, float]:
    return {key: float(value) for key, value in data.items()}
