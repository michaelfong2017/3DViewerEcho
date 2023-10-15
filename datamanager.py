class DataManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True

        self.time_index_to_annotated_qimage = {}

    def get_annotated_qimage(self, time_index):
        return self.time_index_to_annotated_qimage.get(time_index)

    def update_annotated_qimage(self, time_index, annotated_qimage):
        self.time_index_to_annotated_qimage.update({time_index: annotated_qimage})

    def remove_annotated_qimage(self, time_index):
        self.time_index_to_annotated_qimage.pop(time_index)
