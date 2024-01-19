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
        self.view_to_pred_result_width = {}

    def get_pred_result(self, frame_index: int):
        return self.frame_index_to_pred_result.get(frame_index)

    def update_pred_result(self, frame_index: int, all_results):
        self.frame_index_to_pred_result.update({frame_index: all_results})

    def remove_pred_result(self, frame_index: int):
        self.frame_index_to_pred_result.pop(frame_index)

    def get_result_width(self, view):
        return self.view_to_pred_result_width.get(view)

    def update_result_width(self, view, width):
        self.view_to_pred_result_width.update({view: width})

    def remove_result_width(self, view):
        self.view_to_pred_result_width.pop(view)