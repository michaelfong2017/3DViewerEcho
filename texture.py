from PySide2 import QtGui
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path="textures/img.png")
        self.textures[1] = self.get_texture(path="textures/img.png")
        self.textures[2] = self.get_texture(path="textures/img.png")

    def get_texture(self, path):
        image = QtGui.QImage(path)
        if image.isNull():
            return
        image = image.convertToFormat(
            QtGui.QImage.Format_RGB888
        )  # Convert image to RGB888 format
        image = image.mirrored(False, True)
        width = image.width()
        height = image.height()
        # image.fill("red")
        data = image.bits().tobytes()
        texture = self.ctx.texture(size=(width, height), components=3, data=data)
        return texture
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]