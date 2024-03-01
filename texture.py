import moderngl as mgl
from PIL import Image, ImageOps


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path="textures/img.png")
        self.textures[1] = self.get_texture(path="textures/test.png")
        self.textures[2] = self.get_texture(path="textures/img_2.png")
        self.textures["test-ALAX"] = self.get_texture(path="textures/test-ALAX.png")
        self.textures["test-A2C"] = self.get_texture(path="textures/test-A2C.png")
        self.textures["test-A4C"] = self.get_texture(path="textures/test-A4C.png")
        # self.textures["test-SAXMV"] = self.get_texture(path="textures/test-SAXMV.png")
        # self.textures["test-SAXM"] = self.get_texture(path="textures/test-SAXM.png")

    def get_texture(self, path):
        image = Image.open(path)
        image = image.convert('RGB')
        image = ImageOps.flip(image)
        image_data = image.tobytes()
        texture = self.ctx.texture(size=image.size, components=3, data=image_data)
        
        # mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # AF
        texture.anisotropy = 32.0
        return texture
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]