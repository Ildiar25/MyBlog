import hashlib
from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path
from typing import IO


from PIL import Image, ImageFile
from werkzeug.utils import secure_filename


class Picture(ABC):
    """"""
    @abstractmethod
    def get_name(self) -> str:
        ...

    @abstractmethod
    def crop_image(self) -> None:
        ...


class AvatarImage(Picture):
    """"""
    def __init__(self, stream: IO[bytes] | BytesIO) -> None:
        self.stream = stream
        self.image: ImageFile.ImageFile | None = None

    def open(self) -> "AvatarImage":
        self.image = Image.open(self.stream)
        return self

    def crop_image(self) -> "AvatarImage":
        if not self.image:
            raise ValueError("Can not crop profile pic! Open image first!")

        if self.image.width > self.image.height:
            position = (self.image.width - self.image.height) / 2
            self.image = self.image.crop(box=(position, 0, position + self.image.height, self.image.height))

        elif self.image.width < self.image.height:
            position = (self.image.height - self.image.width) / 2
            self.image = self.image.crop(box=(0, position, self.image.width, position + self.image.width))

        return self

    def with_size(self, size: tuple[int, int]) -> "AvatarImage":
        if not self.image:
            raise ValueError("Can not resize profile pic! Open image first!")

        self.image.thumbnail(size)

        return self

    def get_name(self) -> str:
        if not self.image:
            raise ValueError("Can not get profile pic name! Open image first!")

        name = "avatar"
        hexdigest = self.__hash_file()
        size = min(self.image.size)

        fullname = secure_filename(name + "_" + hexdigest[:12] + "_" + f"{size}.jpg")

        self.image.filename = fullname

        return fullname

    def save(self, new_path: Path) -> None:
        self.get_name()
        self.image.save(new_path.joinpath(self.image.filename))

    def __hash_file(self) -> str:
        self.stream.seek(0)

        hasher = hashlib.sha256()
        hasher.update(self.stream.read())

        return hasher.hexdigest()


class PostImage(Picture):
    pass
