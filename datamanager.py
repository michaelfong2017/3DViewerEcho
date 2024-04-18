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

        self.frame_index_to_center_images = {} # for planes x=0, y=0 and z=0

        self._dicom_number_of_frames: int = -1
        self._dicom_average_frame_time_in_ms: float = 60.0
        self._dicom_fps: float = -1.0
        self._dicom_total_duration_in_s: float = -1.0

        self._data_3d_padded_max_length: int = -1   # e.g. data_4d_padded.shape is (42, 213, 213, 213)

        self._highlighted_view: str = ""

        self._server_base_url = "http://localhost:8000/"

    @property
    def dicom_number_of_frames(self):
        return self._dicom_number_of_frames
    @dicom_number_of_frames.setter
    def dicom_number_of_frames(self, value):
        self._dicom_number_of_frames = value

    @property
    def dicom_average_frame_time_in_ms(self):
        return self._dicom_average_frame_time_in_ms
    @dicom_average_frame_time_in_ms.setter
    def dicom_average_frame_time_in_ms(self, value):
        self._dicom_average_frame_time_in_ms = value

    @property
    def dicom_fps(self):
        return self._dicom_fps
    @dicom_fps.setter
    def dicom_fps(self, value):
        self._dicom_fps = value

    @property
    def dicom_total_duration_in_s(self):
        return self._dicom_total_duration_in_s
    @dicom_total_duration_in_s.setter
    def dicom_total_duration_in_s(self, value):
        self._dicom_total_duration_in_s = value
        
    @property
    def data_3d_padded_max_length(self):
        return self._data_3d_padded_max_length
    @data_3d_padded_max_length.setter
    def data_3d_padded_max_length(self, value):
        self._data_3d_padded_max_length = value

    @property
    def highlighted_view(self):
        return self._highlighted_view
    @highlighted_view.setter
    def highlighted_view(self, value):
        self._highlighted_view = value

    @property
    def server_base_url(self):
        return self._server_base_url
    @server_base_url.setter
    def server_base_url(self, value):
        self._server_base_url = value

    def get_pred_result(self, frame_index: int):
        return self.frame_index_to_pred_result.get(frame_index)

    def update_pred_result(self, frame_index: int, all_results):
        self.frame_index_to_pred_result.update({frame_index: all_results})

    def remove_pred_result(self, frame_index: int):
        self.frame_index_to_pred_result.pop(frame_index)

    def clear_all_results(self):
        self.frame_index_to_pred_result.clear()

    def get_center_images(self, frame_index: int):
        return self.frame_index_to_center_images.get(frame_index)

    def update_center_images(self, frame_index: int, all_center_images):
        self.frame_index_to_center_images.update({frame_index: all_center_images})

    def get_result_width(self, view):
        return self.view_to_pred_result_width.get(view)

    def update_result_width(self, view, width):
        self.view_to_pred_result_width.update({view: width})

    def remove_result_width(self, view):
        self.view_to_pred_result_width.pop(view)