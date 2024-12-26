class DataItem:
    """A class representing a data item for oncology data collection."""

    def __init__(self, name: str, value: int, description: str):
        """
        Initialize a new DataItem.

        Args:
            name (str): The name of the data item.
            value (int): The value associated with the data item.
            description (str): A description of the data item.
        """
        self.name = name
        self.value = value
        self.description = description
