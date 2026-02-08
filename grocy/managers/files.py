from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class FileManager:
    """Manage file uploads and downloads in Grocy.

    Access via ``grocy.files``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def upload(self, group: str, file_name: str, data):
        """Upload a file.

        Args:
            group: File group (e.g. ``"recipepictures"``).
            file_name: Name for the file in Grocy.
            data: File content as bytes or a file-like object.
        """
        return self._api.upload_file(group, file_name, data)

    def download(self, group: str, file_name: str):
        """Download a file.

        Args:
            group: File group (e.g. ``"recipepictures"``).
            file_name: Name of the file in Grocy.
        """
        return self._api.download_file(group, file_name)

    def delete(self, group: str, file_name: str):
        """Delete a file.

        Args:
            group: File group (e.g. ``"recipepictures"``).
            file_name: Name of the file in Grocy.
        """
        return self._api.delete_file(group, file_name)
