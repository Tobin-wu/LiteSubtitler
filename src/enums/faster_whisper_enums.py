# coding: utf8
from enum import Enum


class FasterWhisperModelEnum(Enum):
    # TINY = "tiny"
    # BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE_V1 = "large-v1"
    LARGE_V2 = "large-v2"
    LARGE_V3 = "large-v3"


class FasterWhisperDeviceEnum(Enum):
    AUTO = "auto"
    CDUA = "cuda"
    CPU = "cpu"


class VadMethodEnum(Enum):
    """ VAD方法 """
    SILERO_V3 = "silero_v3"
    SILERO_V4 = "silero_v4"
    PYANNOTE_V3 = "pyannote_v3"
    PYANNOTE_ONNX_V3 = "pyannote_onnx_v3"
    AUDITOK = "auditok"
    WEBRTC = "webrtc"
    NONE = ""
