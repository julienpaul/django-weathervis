from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        based on https://stackoverflow.com/a/19961911

        Args:
            name ([type]): [description]
            max_length ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        self.delete(name)
        return super().get_available_name(name, max_length)
