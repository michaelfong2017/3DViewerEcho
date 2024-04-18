import moderngl as mgl
from PIL import Image, ImageOps
from util import resource_path


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path=resource_path("textures/img.png"))
        self.textures[1] = self.get_texture(path=resource_path("textures/test.png"))
        self.textures[2] = self.get_texture(path=resource_path("textures/img_2.png"))
        self.textures["skybox"] = self.get_texture(
            path=resource_path("textures/skybox1/bottom.png")
        )
        self.textures["test-A2C-transparent"] = self.get_texture(
            path=resource_path("textures/test-A2C-transparent.png")
        )
        self.textures["test-A4C-transparent"] = self.get_texture(
            path=resource_path("textures/test-A4C-transparent.png")
        )
        self.textures["test-ALAX-transparent"] = self.get_texture(
            path=resource_path("textures/test-ALAX-transparent.png")
        )
        # self.textures["test-x=0"] = self.get_texture(
        #     path=resource_path("textures/test-x=0.png")
        # )
        # self.textures["test-y=0"] = self.get_texture(
        #     path=resource_path("textures/test-y=0.png")
        # )
        # self.textures["test-z=0"] = self.get_texture(
        #     path=resource_path("textures/test-z=0.png")
        # )
        # self.textures["test-SAXMV"] = self.get_texture(path="textures/test-SAXMV.png")
        # self.textures["test-SAXM"] = self.get_texture(path="textures/test-SAXM.png")

    def get_texture(self, path):
        # to_transparent('textures/test-A2C.png')
        # to_transparent('textures/test-A4C.png')
        # to_transparent('textures/test-ALAX.png')
        # to_transparent('textures/test-SAXM.png')
        # to_transparent('textures/test-SAXMV.png')

        image = Image.open(path)
        image = image.convert("RGBA")
        image = ImageOps.flip(image)
        image_data = image.tobytes()
        texture = self.ctx.texture(size=image.size, components=4, data=image_data)

        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        return texture

    def get_texture_from_pil(self, image):
        image = image.convert("RGBA")
        image = ImageOps.flip(image)
        image_data = image.tobytes()
        texture = self.ctx.texture(size=image.size, components=4, data=image_data)

        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        return texture
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]


def to_transparent(path):
    # Open the PNG image using Pillow
    image = Image.open(path)

    # Convert the image to RGBA if it's not already in that format
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # Get the pixel data from the image
    pixels = image.load()

    # Iterate over each pixel and convert black pixels to transparent
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            r, g, b, a = pixels[x, y]
            if r == 0 and g == 0 and b == 0:
                pixels[x, y] = (0, 0, 0, 0)

    # Save the modified image
    image.save(f"{path.replace('.png', '-transparent.png')}")
