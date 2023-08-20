from PIL import Image
import numpy as np
import cv2 as cv


# =======================================================================================================================


def valid_input(
    image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]
) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    print("\n")
    try:
        print("PARAMS -> ", image_size, tile_size)
        # ------------------
        x_tiles: tuple[int, int] = divmod(image_size[0], tile_size[0])
        print("X TILES -> ", x_tiles)
        assert x_tiles[1] == 0
        # ------------------
        y_tiles: tuple[int, int] = divmod(image_size[1], tile_size[1])
        print("Y TILES -> ", y_tiles)
        # assert y_tiles[1] == 0
        # ------------------
        tiles: bool = len(ordering) == (tile_count := (x_tiles[0] * y_tiles[0]))
        print("TILES -> ", tiles, tile_count)
        assert tiles
        # tiles.append(tile_count)
        # ------------------
        max_idx: bool = (size := max(ordering) - (x_tiles[0] * y_tiles[0] - 1)) == 0
        print("MAX ORDERING -> ", max_idx, size)
        assert max_idx
        # -------------
        print("RESULT -> ", "TRUE")
        return True
    except AssertionError as e:
        print("ERROR -> ", e)
        print("RESULT -> ", "FALSE")
        return False


# =======================================================================================================================


def rearrange_tiles(
    image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str
) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    print("\n", "\n", "Rearranging image...")
    with Image.open(fp=image_path) as img:
        img_array: np.ndarray = np.asarray(img)
        # img = img.convert("RGBA")

    print("Image Size -> ", img.size)

    try:
        assert valid_input(img.size, tile_size, ordering)
    except AssertionError:
        raise ValueError("The tile size or ordering are not valid for the given image")
    # --------------
    print("Shape -> ", img_array.shape)
    # --------------
    img_reshaped = np.reshape(
        a=img_array, newshape=(len(ordering), tile_size[0], tile_size[1], 4)
    )
    print("New Shape -> ", img_reshaped.shape)
    # --------------
    try:
        # out_array = [(img_array[ordering[i]]) for i in ordering]
        out_array = np.take(a=img_reshaped, indices=ordering, axis=0)
        out_array = np.reshape(a=out_array, newshape=img_array.shape)
        print("Out Shape -> ", out_array.shape)
    except IndexError:
        raise IndexError("The tile size or ordering are not valid for the given image")
    # -------------
    # save image

    new_img: Image = Image.fromarray(obj=out_array, mode="RGB")
    new_img.save(out_path)



if __name__ == "__main__":
    image_path: str = "test.png"
    tile_size: tuple[int, int] = (256, 256)
    ordering: list[int] = [1,0,2,3]
    rearrange_tiles(image_path=image_path, tile_size=tile_size, ordering=ordering, out_path="out_test.png")