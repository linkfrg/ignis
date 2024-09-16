PIPELINE_TEMPLATE = """
    pipewiresrc path={node_id} do-timestamp=true keepalive-time=1000 resend-last=true !
    videoconvert chroma-mode=none dither=none matrix-mode=output-only n-threads={n_threads} !
    queue !
    x264enc bitrate={bitrate} threads={n_threads} !
    queue !
    h264parse !
    mp4mux fragment-duration=500 fragment-mode=first-moov-then-finalise name=mux !
    filesink location={path}
    """

MAIN_AUDIO_PIPELINE = """
    pulsesrc device={device} !
    queue !
    audioconvert !
    audioresample !
    audiomixer name=mix !
    queue !
    opusenc !
    mux.
"""

AUDIO_DEVICE_PIPELINE = """
    pulsesrc device={device} !
    queue !
    audioconvert !
    audioresample !
    mix.
"""
