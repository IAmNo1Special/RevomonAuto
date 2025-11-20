"""
Base client for Revomon data access
"""
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from logging import getLogger

logger = getLogger(__name__)


class BaseDataClient(ABC):
    """
    Abstract base class for Revomon data clients.

    Provides common functionality for loading and accessing JSON data files.
    """

    def __init__(self, data_file: Union[str, Path]):
        """
        Initialize the data client.

        Args:
            data_file: Path to the JSON data file
        """
        self.data_file = Path(data_file)
        self._data: List[Dict[str, Any]] = []
        self._loaded = False

    def load_data(self, force_reload: bool = False) -> bool:
        """
        Load data from the JSON file.

        Args:
            force_reload: If True, reload data even if already loaded

        Returns:
            True if data was loaded successfully, False otherwise
        """
        if self._loaded and not force_reload:
            return True

        if not self.data_file.exists():
            logger.error(f"Data file not found: {self.data_file}")
            return False

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            self._loaded = True
            logger.info(f"Loaded {len(self._data)} records from {self.data_file}")
            return True
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading data from {self.data_file}: {e}")
            return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all data records.

        Returns:
            List of all data records
        """
        self.load_data()
        return self._data.copy()

    def get_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get a record by index.

        Args:
            index: The index of the record to retrieve

        Returns:
            The record at the specified index, or None if not found
        """
        self.load_data()
        if 0 <= index < len(self._data):
            return self._data[index].copy()
        return None

    def find_by_field(self, field: str, value: Any) -> List[Dict[str, Any]]:
        """
        Find records where a field matches a specific value.

        Args:
            field: The field name to search in
            value: The value to match

        Returns:
            List of matching records
        """
        self.load_data()
        return [record.copy() for record in self._data if record.get(field) == value]

    def find_first_by_field(self, field: str, value: Any) -> Optional[Dict[str, Any]]:
        """
        Find the first record where a field matches a specific value.

        Args:
            field: The field name to search in
            value: The value to match

        Returns:
            The first matching record, or None if not found
        """
        self.load_data()
        for record in self._data:
            if record.get(field) == value:
                return record.copy()
        return None

    def count(self) -> int:
        """
        Get the total number of records.

        Returns:
            Number of records in the data
        """
        self.load_data()
        return len(self._data)

    def is_loaded(self) -> bool:
        """
        Check if data has been loaded.

        Returns:
            True if data is loaded, False otherwise
        """
        return self._loaded

    @abstractmethod
    def get_primary_key_field(self) -> str:
        """
        Get the name of the primary key field for this data type.

        Returns:
            The primary key field name
        """
        pass

    def get_by_primary_key(self, key_value: Any) -> Optional[Dict[str, Any]]:
        """
        Get a record by its primary key.

        Args:
            key_value: The primary key value to search for

        Returns:
            The matching record, or None if not found
        """
        primary_key = self.get_primary_key_field()
        return self.find_first_by_field(primary_key, key_value)
