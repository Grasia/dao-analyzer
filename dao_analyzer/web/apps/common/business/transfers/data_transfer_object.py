import inspect

# Slighly based from https://stackoverflow.com/questions/750908/auto-repr-method
class DataTransferObject:
    """ Indicates that this is a DataTransferObject

    Classes that inherit from this class should have the properties inside the
    `__init__` function with the same name, or prepended with an underscore (_).

    example:
    ```
    @datatransferobject
    class A:
        def __init__(self, a, b):
            self.a = a
            self._b = b
    ```
    """

    def __repr__(obj):
        items = []

        for p in inspect.signature(obj.__init__).parameters:
            if hasattr(obj, p):
                value = getattr(obj, p)
            else:
                value = getattr(obj, f'_{p}')
            
            item = f"{p} = {repr(value)}"

            items.append(item)

        return f"{obj.__class__.__name__}({', '.join(items)})"
