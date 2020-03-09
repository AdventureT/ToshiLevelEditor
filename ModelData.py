class ModelData:
    class MeshData:
        def __init__(self, vertices, faces, normals, uvs):
            self.vertices = vertices
            self.faces = faces
            self.normals = normals
            self.uvs = uvs
    def __init__(self, modelName, meshNames):
        self.modelName = modelName
        self.meshNames = meshNames
        self.meshData = []

class TerrainData:
    def __init__(self, modelName, position):
        self.modelName = modelName
        self.position = position
