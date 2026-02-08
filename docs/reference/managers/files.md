# File Manager

Upload, download, and delete files (product pictures, recipe pictures, equipment manuals, etc.).

Access via `grocy.files`.

```python
# Upload a file
with open("photo.jpg", "rb") as f:
    grocy.files.upload(group="productpictures", file_name="photo.jpg", data=f)

# Download a file
data = grocy.files.download(group="productpictures", file_name="photo.jpg")

# Delete a file
grocy.files.delete(group="productpictures", file_name="photo.jpg")
```

## Class Reference

::: grocy.managers.files.FileManager
    options:
      members_order: source
      show_source: false
