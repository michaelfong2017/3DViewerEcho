from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # cube vao
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['cube']
        )

        # quad vao
        self.vaos['quad'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['quad']
        )

        # line vao
        self.vaos['line'] = self.get_vao(
            program=self.program.programs['line'],
            vbo = self.vbo.vbos['line']
        )

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao
    
    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()