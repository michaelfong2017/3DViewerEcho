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

        self.frame_index_to_pred_result = {}

    def get_pred_result(self, frame_index):
        return self.frame_index_to_pred_result.get(frame_index)

    def update_pred_result(self, frame_index, pred_image, pred_rotated_coords):
        self.frame_index_to_pred_result.update({frame_index: (pred_image, pred_rotated_coords)})

    def remove_pred_result(self, frame_index):
        self.frame_index_to_pred_result.pop(frame_index)
