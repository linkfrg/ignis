from dataclasses import dataclass, fields
from . import arg_types


@dataclass
class RecorderConfig:
    source: arg_types.Source
    path: arg_types.Path
    resolution_limit: arg_types.ResolutionLimit = None
    region: arg_types.Region = None
    framerate: arg_types.Framerate = None
    audio_devices: arg_types.AudioDevices = None
    quality: arg_types.Quality = None
    video_codec: arg_types.VideoCodec = None
    audio_codec: arg_types.AudioCodec = None
    audio_bitrate: arg_types.AudioBitrate = None
    framerate_mode: arg_types.FramerateMode = None
    bitrate_mode: arg_types.BitrateMode = None
    color_range: arg_types.ColorRange = None
    cursor: arg_types.Cursor = None
    encoder: arg_types.Encoder = None

    @classmethod
    def from_options(cls: type["RecorderConfig"]) -> "RecorderConfig":
        from ignis.options import options

        init_kwargs = {}

        for f in fields(cls):
            init_kwargs[f.name] = getattr(options.recorder, f"default_{f.name}")

        return cls(**init_kwargs)
