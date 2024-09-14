import enum

from typing import Callable

from gi.repository import GObject
from gi.repository import Gio


MIXER_UI_DEVICE_INVALID: int = 0
_lock = ... # FIXME Constant
_namespace: str = "Gvc"
_version: str = "1.0"

class ChannelMap(GObject.Object):
    """
    :Constructors:

    ::

        ChannelMap(**properties)
        new() -> Gvc.ChannelMap

    Object GvcChannelMap

    Signals from GvcChannelMap:
      volume-changed (gboolean)

    Signals from GObject:
      notify (GParam)
    """
    parent: GObject.Object = ...
    priv: ChannelMapPrivate = ...
    def can_balance(self) -> bool: ...
    def can_fade(self) -> bool: ...
    def do_volume_changed(self, set: bool) -> None: ...
    def get_mapping(self) -> str: ...
    def get_num_channels(self) -> int: ...
    def get_volume(self) -> float: ...
    @classmethod
    def new(cls) -> ChannelMap: ...


class ChannelMapClass(GObject.GPointer):
    """
    :Constructors:

    ::

        ChannelMapClass()
    """
    parent_class: GObject.ObjectClass = ...
    volume_changed: Callable[[ChannelMap, bool], None] = ...

class ChannelMapPrivate(GObject.GPointer): ...

class MixerCard(GObject.Object):
    """
    :Constructors:

    ::

        MixerCard(**properties)

    Object GvcMixerCard

    Properties from GvcMixerCard:
      id -> gulong: id
        The id for this card
      pa-context -> gpointer: PulseAudio context
        The PulseAudio context for this card
      index -> gulong: Index
        The index for this card
      name -> gchararray: Name
        Name to display for this card
      icon-name -> gchararray: Icon Name
        Name of icon to display for this card
      profile -> gchararray: Profile
        Name of current profile for this card
      human-profile -> gchararray: Profile (Human readable)
        Name of current profile for this card in human readable form

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        human_profile: str
        icon_name: str
        id: int
        index: int
        name: str
        pa_context: None
        profile: str
    props: Props = ...
    parent: GObject.Object = ...
    priv: MixerCardPrivate = ...
    def __init__(self, icon_name: str = ...,
                 id: int = ...,
                 index: int = ...,
                 name: str = ...,
                 pa_context: None = ...,
                 profile: str = ...): ...
    def change_profile(self, profile: str | None = None) -> bool: ...
    def get_gicon(self) -> Gio.Icon: ...
    def get_icon_name(self) -> str: ...
    def get_id(self) -> int: ...
    def get_index(self) -> int: ...
    def get_name(self) -> str: ...
    def get_ports(self) -> list[MixerCardPort]: ...
    def get_profiles(self) -> list[MixerCardProfile]: ...
    def set_icon_name(self, name: str) -> bool: ...
    def set_name(self, name: str) -> bool: ...
    def set_ports(self, ports: list[MixerCardPort]) -> bool: ...
    def set_profile(self, profile: str) -> bool: ...
    def set_profiles(self, profiles: list[MixerCardProfile]) -> bool: ...


class MixerCardClass(GObject.GPointer):
    """
    :Constructors:

    ::

        MixerCardClass()
    """
    parent_class: GObject.ObjectClass = ...

class MixerCardPort(GObject.GPointer):
    """
    :Constructors:

    ::

        MixerCardPort()
    """
    port: str = ...
    human_port: str = ...
    icon_name: str = ...
    priority: int = ...
    available: int = ...
    direction: int = ...
    profiles: list[None] = ...

class MixerCardPrivate(GObject.GPointer): ...

class MixerCardProfile(GObject.GPointer):
    """
    :Constructors:

    ::

        MixerCardProfile()
    """
    profile: str = ...
    human_profile: str = ...
    status: str = ...
    priority: int = ...
    n_sinks: int = ...
    n_sources: int = ...
    def compare(self, b: MixerCardProfile) -> int: ...


class MixerControl(GObject.Object):
    """
    :Constructors:

    ::

        MixerControl(**properties)
        new(name:str) -> Gvc.MixerControl

    Object GvcMixerControl

    Signals from GvcMixerControl:
      state-changed (guint)
      stream-added (guint)
      stream-removed (guint)
      stream-changed (guint)
      audio-device-selection-needed (guint, gboolean, guint)
      card-added (guint)
      card-removed (guint)
      default-sink-changed (guint)
      default-source-changed (guint)
      active-output-update (guint)
      active-input-update (guint)
      output-added (guint)
      input-added (guint)
      output-removed (guint)
      input-removed (guint)

    Properties from GvcMixerControl:
      name -> gchararray: Name
        Name to display for this mixer control

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        name: str
    props: Props = ...
    parent: GObject.Object = ...
    priv: MixerControlPrivate = ...
    def __init__(self, name: str = ...): ...
    def change_input(self, input: MixerUIDevice) -> None: ...
    def change_output(self, output: MixerUIDevice) -> None: ...
    def change_profile_on_selected_device(self, device: MixerUIDevice, profile: str | None = None) -> bool: ...
    def close(self) -> bool: ...
    def do_active_input_update(self, id: int) -> None: ...
    def do_active_output_update(self, id: int) -> None: ...
    def do_audio_device_selection_needed(self, id: int, show_dialog: bool, choices: HeadsetPortChoice) -> None: ...
    def do_card_added(self, id: int) -> None: ...
    def do_card_removed(self, id: int) -> None: ...
    def do_default_sink_changed(self, id: int) -> None: ...
    def do_default_source_changed(self, id: int) -> None: ...
    def do_input_added(self, id: int) -> None: ...
    def do_input_removed(self, id: int) -> None: ...
    def do_output_added(self, id: int) -> None: ...
    def do_output_removed(self, id: int) -> None: ...
    def do_state_changed(self, new_state: MixerControlState) -> None: ...
    def do_stream_added(self, id: int) -> None: ...
    def do_stream_changed(self, id: int) -> None: ...
    def do_stream_removed(self, id: int) -> None: ...
    def get_cards(self) -> list[MixerCard]: ...
    def get_default_sink(self) -> MixerStream: ...
    def get_default_source(self) -> MixerStream: ...
    def get_event_sink_input(self) -> MixerStream: ...
    def get_sink_inputs(self) -> list[MixerSinkInput]: ...
    def get_sinks(self) -> list[MixerSink]: ...
    def get_source_outputs(self) -> list[MixerSourceOutput]: ...
    def get_sources(self) -> list[MixerSource]: ...
    def get_state(self) -> MixerControlState: ...
    def get_stream_from_device(self, device: MixerUIDevice) -> MixerStream: ...
    def get_streams(self) -> list[MixerStream]: ...
    def get_vol_max_amplified(self) -> float: ...
    def get_vol_max_norm(self) -> float: ...
    def lookup_card_id(self, id: int) -> MixerCard: ...
    def lookup_device_from_stream(self, stream: MixerStream) -> MixerUIDevice: ...
    def lookup_input_id(self, id: int) -> MixerUIDevice: ...
    def lookup_output_id(self, id: int) -> MixerUIDevice: ...
    def lookup_stream_id(self, id: int) -> MixerStream: ...
    @classmethod
    def new(cls, name: str) -> MixerControl: ...
    def open(self) -> bool: ...
    def set_default_sink(self, stream: MixerStream) -> bool: ...
    def set_default_source(self, stream: MixerStream) -> bool: ...
    def set_headset_port(self, id: int, choices: HeadsetPortChoice) -> None: ...


class MixerControlClass(GObject.GPointer):
    """
    :Constructors:

    ::

        MixerControlClass()
    """
    parent_class: GObject.ObjectClass = ...
    state_changed: Callable[[MixerControl, MixerControlState], None] = ...
    stream_added: Callable[[MixerControl, int], None] = ...
    stream_changed: Callable[[MixerControl, int], None] = ...
    stream_removed: Callable[[MixerControl, int], None] = ...
    card_added: Callable[[MixerControl, int], None] = ...
    card_removed: Callable[[MixerControl, int], None] = ...
    default_sink_changed: Callable[[MixerControl, int], None] = ...
    default_source_changed: Callable[[MixerControl, int], None] = ...
    active_output_update: Callable[[MixerControl, int], None] = ...
    active_input_update: Callable[[MixerControl, int], None] = ...
    output_added: Callable[[MixerControl, int], None] = ...
    input_added: Callable[[MixerControl, int], None] = ...
    output_removed: Callable[[MixerControl, int], None] = ...
    input_removed: Callable[[MixerControl, int], None] = ...
    audio_device_selection_needed: Callable[[MixerControl, int, bool, HeadsetPortChoice], None] = ...

class MixerControlPrivate(GObject.GPointer): ...

class MixerEventRole(MixerStream):
    """
    :Constructors:

    ::

        MixerEventRole(**properties)

    Object GvcMixerEventRole

    Properties from GvcMixerEventRole:
      device -> gchararray: Device
        Device

    Properties from GvcMixerStream:
      id -> gulong: id
        The id for this stream
      pa-context -> gpointer: PulseAudio context
        The PulseAudio context for this stream
      channel-map -> GvcChannelMap: channel map
        The channel map for this stream
      index -> gulong: Index
        The index for this stream
      name -> gchararray: Name
        Name to display for this stream
      description -> gchararray: Description
        Description to display for this stream
      application-id -> gchararray: Application identifier
        Application identifier for this stream
      icon-name -> gchararray: Icon Name
        Name of icon to display for this stream
      form-factor -> gchararray: Form Factor
        Device form factor for this stream, as reported by PulseAudio
      sysfs-path -> gchararray: Sysfs path
        Sysfs path for the device associated with this stream
      volume -> gulong: Volume
        The volume for this stream
      decibel -> gdouble: Decibel
        The decibel level for this stream
      is-muted -> gboolean: is muted
        Whether stream is muted
      can-decibel -> gboolean: can decibel
        Whether stream volume can be converted to decibel units
      is-event-stream -> gboolean: is event stream
        Whether stream's role is to play an event
      is-virtual -> gboolean: is virtual stream
        Whether the stream is virtual
      card-index -> glong: Card index
        The index of the card for this stream
      port -> gchararray: Port
        The name of the current port for this stream
      state -> GvcMixerStreamState: State
        The current state of this stream

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        device: str
        application_id: str
        can_decibel: bool
        card_index: int
        channel_map: ChannelMap
        decibel: float
        description: str
        form_factor: str
        icon_name: str
        id: int
        index: int
        is_event_stream: bool
        is_muted: bool
        is_virtual: bool
        name: str
        pa_context: None
        port: str
        state: MixerStreamState
        sysfs_path: str
        volume: int
    props: Props = ...
    parent: MixerStream = ...
    priv: MixerEventRolePrivate = ...
    def __init__(self, device: str = ...,
                 application_id: str = ...,
                 can_decibel: bool = ...,
                 card_index: int = ...,
                 channel_map: ChannelMap = ...,
                 decibel: float = ...,
                 description: str = ...,
                 form_factor: str = ...,
                 icon_name: str = ...,
                 id: int = ...,
                 index: int = ...,
                 is_event_stream: bool = ...,
                 is_muted: bool = ...,
                 is_virtual: bool = ...,
                 name: str = ...,
                 pa_context: None = ...,
                 port: str = ...,
                 state: MixerStreamState = ...,
                 sysfs_path: str = ...,
                 volume: int = ...): ...

class MixerEventRoleClass(GObject.GPointer):
    """
    :Constructors:

    ::

        MixerEventRoleClass()
    """
    parent_class: MixerStreamClass = ...

class MixerEventRolePrivate(GObject.GPointer): ...

class MixerSink(MixerStream):
    """
    :Constructors:

    ::

        MixerSink(**properties)

    Object GvcMixerSink

    Properties from GvcMixerStream:
      id -> gulong: id
        The id for this stream
      pa-context -> gpointer: PulseAudio context
        The PulseAudio context for this stream
      channel-map -> GvcChannelMap: channel map
        The channel map for this stream
      index -> gulong: Index
        The index for this stream
      name -> gchararray: Name
        Name to display for this stream
      description -> gchararray: Description
        Description to display for this stream
      application-id -> gchararray: Application identifier
        Application identifier for this stream
      icon-name -> gchararray: Icon Name
        Name of icon to display for this stream
      form-factor -> gchararray: Form Factor
        Device form factor for this stream, as reported by PulseAudio
      sysfs-path -> gchararray: Sysfs path
        Sysfs path for the device associated with this stream
      volume -> gulong: Volume
        The volume for this stream
      decibel -> gdouble: Decibel
        The decibel level for this stream
      is-muted -> gboolean: is muted
        Whether stream is muted
      can-decibel -> gboolean: can decibel
        Whether stream volume can be converted to decibel units
      is-event-stream -> gboolean: is event stream
        Whether stream's role is to play an event
      is-virtual -> gboolean: is virtual stream
        Whether the stream is virtual
      card-index -> glong: Card index
        The index of the card for this stream
      port -> gchararray: Port
        The name of the current port for this stream
      state -> GvcMixerStreamState: State
        The current state of this stream

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        application_id: str
        can_decibel: bool
        card_index: int
        channel_map: ChannelMap
        decibel: float
        description: str
        form_factor: str
        icon_name: str
        id: int
        index: int
        is_event_stream: bool
        is_muted: bool
        is_virtual: bool
        name: str
        pa_context: None
        port: str
        state: MixerStreamState
        sysfs_path: str
        volume: int
    props: Props = ...
    parent: MixerStream = ...
    priv: MixerSinkPrivate = ...
    def __init__(self, application_id: str = ...,
                 can_decibel: bool = ...,
                 card_index: int = ...,
                 channel_map: ChannelMap = ...,
                 decibel: float = ...,
                 description: str = ...,
                 form_factor: str = ...,
                 icon_name: str = ...,
                 id: int = ...,
                 index: int = ...,
                 is_event_stream: bool = ...,
                 is_muted: bool = ...,
                 is_virtual: bool = ...,
                 name: str = ...,
                 pa_context: None = ...,
                 port: str = ...,
                 state: MixerStreamState = ...,
                 sysfs_path: str = ...,
                 volume: int = ...): ...

class MixerSinkClass(GObject.GPointer):
    """
    :Constructors:

    ::

        MixerSinkClass()
    """
    parent_class: MixerStreamClass = ...

class MixerSinkInput(MixerStream):
    """
    :Constructors:

    ::

        MixerSinkInput(**properties)

    Object GvcMixerSinkInput

    Properties from GvcMixerStream:
      id -> gulong: id
        The id for this stream
      pa-context -> gpointer: PulseAudio context
        The PulseAudio context for this stream
      channel-map -> GvcChannelMap: channel map
        The channel map for this stream
      index -> gulong: Index
        The index for this stream
      name -> gchararray: Name
        Name to display for this stream
      description -> gchararray: Description
        Description to display for this stream
      application-id -> gchararray: Application identifier
        Application identifier for this stream
      icon-name -> gchararray: Icon Name
        Name of icon to display for this stream
      form-factor -> gchararray: Form Factor
        Device form factor for this stream, as reported by PulseAudio
      sysfs-path -> gchararray: Sysfs path
        Sysfs path for the device associated with this stream
      volume -> gulong: Volume
        The volume for this stream
      decibel -> gdouble: Decibel
        The decibel level for this stream
      is-muted -> gboolean: is muted
        Whether stream is muted
      can-decibel -> gboolean: can decibel
        Whether stream volume can be converted to decibel units
      is-event-stream -> gboolean: is event stream
        Whether stream's role is to play an event
      is-virtual -> gboolean: is virtual stream
        Whether the stream is virtual
      card-index -> glong: Card index
        The index of the card for this stream
      port -> gchararray: Port
        The name of the current port for this stream
      state -> GvcMixerStreamState: State
        The current state of this stream

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        application_id: str
        can_decibel: bool
        card_index: int
        channel_map: ChannelMap
        decibel: float
        description: str
        form_factor: str
        icon_name: str
        id: int
        index: int
        is_event_stream: bool
        is_muted: bool
        is_virtual: bool
        name: str
        pa_context: None
        port: str
        state: MixerStreamState
        sysfs_path: str
        volume: int
    props: Props = ...
    parent: MixerStream = ...
    priv: MixerSinkInputPrivate = ...
    def __init__(self, application_id: str = ...,
                 can_decibel: bool = ...,
                 card_index: int = ...,
                 channel_map: ChannelMap = ...,
                 decibel: float = ...,
                 description: str = ...,
                 form_factor: str = ...,
                 icon_name: str = ...,
                 id: int = ...,
                 index: int = ...,
                 is_event_stream: bool = ...,
                 is_muted: bool = ...,
                 is_virtual: bool = ...,
                 name: str = ...,
                 pa_context: None = ...,
                 port: str = ...,
                 state: MixerStreamState = ...,
                 sysfs_path: str = ...,
                 volume: int = ...): ...

class MixerSinkInputClass(GObject.GPointer):
    """
    :Constructors:

    ::

        MixerSinkInputClass()
    """
    parent_class: MixerStreamClass = ...

class MixerSinkInputPrivate(GObject.GPointer): ...

class MixerSinkPrivate(GObject.GPointer): ...

class MixerSource(MixerStream):
    """
    :Constructors:

    ::

        MixerSource(**properties)

    Object GvcMixerSource

    Properties from GvcMixerStream:
      id -> gulong: id
        The id for this stream
      pa-context -> gpointer: PulseAudio context
        The PulseAudio context for this stream
      channel-map -> GvcChannelMap: channel map
        The channel map for this stream
      index -> gulong: Index
        The index for this stream
      name -> gchararray: Name
        Name to display for this stream
      description -> gchararray: Description
        Description to display for this stream
      application-id -> gchararray: Application identifier
        Application identifier for this stream
      icon-name -> gchararray: Icon Name
        Name of icon to display for this stream
      form-factor -> gchararray: Form Factor
        Device form factor for this stream, as reported by PulseAudio
      sysfs-path -> gchararray: Sysfs path
        Sysfs path for the device associated with this stream
      volume -> gulong: Volume
        The volume for this stream
      decibel -> gdouble: Decibel
        The decibel level for this stream
      is-muted -> gboolean: is muted
        Whether stream is muted
      can-decibel -> gboolean: can decibel
        Whether stream volume can be converted to decibel units
      is-event-stream -> gboolean: is event stream
        Whether stream's role is to play an event
      is-virtual -> gboolean: is virtual stream
        Whether the stream is virtual
      card-index -> glong: Card index
        The index of the card for this stream
      port -> gchararray: Port
        The name of the current port for this stream
      state -> GvcMixerStreamState: State
        The current state of this stream

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        application_id: str
        can_decibel: bool
        card_index: int
        channel_map: ChannelMap
        decibel: float
        description: str
        form_factor: str
        icon_name: str
        id: int
        index: int
        is_event_stream: bool
        is_muted: bool
        is_virtual: bool
        name: str
        pa_context: None
        port: str
        state: MixerStreamState
        sysfs_path: str
        volume: int
    props: Props = ...
    parent: MixerStream = ...
    priv: MixerSourcePrivate = ...
    def __init__(self, application_id: str = ...,
                 can_decibel: bool = ...,
                 card_index: int = ...,
                 channel_map: ChannelMap = ...,
                 decibel: float = ...,
                 description: str = ...,
                 form_factor: str = ...,
                 icon_name: str = ...,
                 id: int = ...,
                 index: int = ...,
                 is_event_stream: bool = ...,
                 is_muted: bool = ...,
                 is_virtual: bool = ...,
                 name: str = ...,
                 pa_context: None = ...,
                 port: str = ...,
                 state: MixerStreamState = ...,
                 sysfs_path: str = ...,
                 volume: int = ...): ...

class MixerSourceClass(GObject.GPointer):
    """
    :Constructors:

    ::

        MixerSourceClass()
    """
    parent_class: MixerStreamClass = ...

class MixerSourceOutput(MixerStream):
    """
    :Constructors:

    ::

        MixerSourceOutput(**properties)

    Object GvcMixerSourceOutput

    Properties from GvcMixerStream:
      id -> gulong: id
        The id for this stream
      pa-context -> gpointer: PulseAudio context
        The PulseAudio context for this stream
      channel-map -> GvcChannelMap: channel map
        The channel map for this stream
      index -> gulong: Index
        The index for this stream
      name -> gchararray: Name
        Name to display for this stream
      description -> gchararray: Description
        Description to display for this stream
      application-id -> gchararray: Application identifier
        Application identifier for this stream
      icon-name -> gchararray: Icon Name
        Name of icon to display for this stream
      form-factor -> gchararray: Form Factor
        Device form factor for this stream, as reported by PulseAudio
      sysfs-path -> gchararray: Sysfs path
        Sysfs path for the device associated with this stream
      volume -> gulong: Volume
        The volume for this stream
      decibel -> gdouble: Decibel
        The decibel level for this stream
      is-muted -> gboolean: is muted
        Whether stream is muted
      can-decibel -> gboolean: can decibel
        Whether stream volume can be converted to decibel units
      is-event-stream -> gboolean: is event stream
        Whether stream's role is to play an event
      is-virtual -> gboolean: is virtual stream
        Whether the stream is virtual
      card-index -> glong: Card index
        The index of the card for this stream
      port -> gchararray: Port
        The name of the current port for this stream
      state -> GvcMixerStreamState: State
        The current state of this stream

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        application_id: str
        can_decibel: bool
        card_index: int
        channel_map: ChannelMap
        decibel: float
        description: str
        form_factor: str
        icon_name: str
        id: int
        index: int
        is_event_stream: bool
        is_muted: bool
        is_virtual: bool
        name: str
        pa_context: None
        port: str
        state: MixerStreamState
        sysfs_path: str
        volume: int
    props: Props = ...
    parent: MixerStream = ...
    priv: MixerSourceOutputPrivate = ...
    def __init__(self, application_id: str = ...,
                 can_decibel: bool = ...,
                 card_index: int = ...,
                 channel_map: ChannelMap = ...,
                 decibel: float = ...,
                 description: str = ...,
                 form_factor: str = ...,
                 icon_name: str = ...,
                 id: int = ...,
                 index: int = ...,
                 is_event_stream: bool = ...,
                 is_muted: bool = ...,
                 is_virtual: bool = ...,
                 name: str = ...,
                 pa_context: None = ...,
                 port: str = ...,
                 state: MixerStreamState = ...,
                 sysfs_path: str = ...,
                 volume: int = ...): ...

class MixerSourceOutputClass(GObject.GPointer):
    """
    :Constructors:

    ::

        MixerSourceOutputClass()
    """
    parent_class: MixerStreamClass = ...

class MixerSourceOutputPrivate(GObject.GPointer): ...

class MixerSourcePrivate(GObject.GPointer): ...

class MixerStream(GObject.Object):
    """
    :Constructors:

    ::

        MixerStream(**properties)

    Object GvcMixerStream

    Properties from GvcMixerStream:
      id -> gulong: id
        The id for this stream
      pa-context -> gpointer: PulseAudio context
        The PulseAudio context for this stream
      channel-map -> GvcChannelMap: channel map
        The channel map for this stream
      index -> gulong: Index
        The index for this stream
      name -> gchararray: Name
        Name to display for this stream
      description -> gchararray: Description
        Description to display for this stream
      application-id -> gchararray: Application identifier
        Application identifier for this stream
      icon-name -> gchararray: Icon Name
        Name of icon to display for this stream
      form-factor -> gchararray: Form Factor
        Device form factor for this stream, as reported by PulseAudio
      sysfs-path -> gchararray: Sysfs path
        Sysfs path for the device associated with this stream
      volume -> gulong: Volume
        The volume for this stream
      decibel -> gdouble: Decibel
        The decibel level for this stream
      is-muted -> gboolean: is muted
        Whether stream is muted
      can-decibel -> gboolean: can decibel
        Whether stream volume can be converted to decibel units
      is-event-stream -> gboolean: is event stream
        Whether stream's role is to play an event
      is-virtual -> gboolean: is virtual stream
        Whether the stream is virtual
      card-index -> glong: Card index
        The index of the card for this stream
      port -> gchararray: Port
        The name of the current port for this stream
      state -> GvcMixerStreamState: State
        The current state of this stream

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        application_id: str
        can_decibel: bool
        card_index: int
        channel_map: ChannelMap
        decibel: float
        description: str
        form_factor: str
        icon_name: str
        id: int
        index: int
        is_event_stream: bool
        is_muted: bool
        is_virtual: bool
        name: str
        pa_context: None
        port: str
        state: MixerStreamState
        sysfs_path: str
        volume: int
    props: Props = ...
    parent: GObject.Object = ...
    priv: MixerStreamPrivate = ...
    def __init__(self, application_id: str = ...,
                 can_decibel: bool = ...,
                 card_index: int = ...,
                 channel_map: ChannelMap = ...,
                 decibel: float = ...,
                 description: str = ...,
                 form_factor: str = ...,
                 icon_name: str = ...,
                 id: int = ...,
                 index: int = ...,
                 is_event_stream: bool = ...,
                 is_muted: bool = ...,
                 is_virtual: bool = ...,
                 name: str = ...,
                 pa_context: None = ...,
                 port: str = ...,
                 state: MixerStreamState = ...,
                 sysfs_path: str = ...,
                 volume: int = ...): ...
    def change_is_muted(self, is_muted: bool) -> bool: ...
    def change_port(self, port: str) -> bool: ...
    def do_change_is_muted(self, is_muted: bool) -> bool: ...
    def do_change_port(self, port: str) -> bool: ...
    def do_push_volume(self, operation: None) -> bool: ...
    def get_application_id(self) -> str: ...
    def get_base_volume(self) -> int: ...
    def get_can_decibel(self) -> bool: ...
    def get_card_index(self) -> int: ...
    def get_channel_map(self) -> ChannelMap: ...
    def get_decibel(self) -> float: ...
    def get_description(self) -> str: ...
    def get_form_factor(self) -> str: ...
    def get_gicon(self) -> Gio.Icon: ...
    def get_icon_name(self) -> str: ...
    def get_id(self) -> int: ...
    def get_index(self) -> int: ...
    def get_is_muted(self) -> bool: ...
    def get_name(self) -> str: ...
    def get_port(self) -> MixerStreamPort: ...
    def get_ports(self) -> list[MixerStreamPort]: ...
    def get_state(self) -> MixerStreamState: ...
    def get_sysfs_path(self) -> str: ...
    def get_volume(self) -> int: ...
    def is_event_stream(self) -> bool: ...
    def is_running(self) -> bool: ...
    def is_virtual(self) -> bool: ...
    def push_volume(self) -> bool: ...
    def set_application_id(self, application_id: str) -> bool: ...
    def set_base_volume(self, base_volume: int) -> bool: ...
    def set_can_decibel(self, can_decibel: bool) -> bool: ...
    def set_card_index(self, card_index: int) -> bool: ...
    def set_decibel(self, db: float) -> bool: ...
    def set_description(self, description: str) -> bool: ...
    def set_form_factor(self, form_factor: str) -> bool: ...
    def set_icon_name(self, name: str) -> bool: ...
    def set_is_event_stream(self, is_event_stream: bool) -> bool: ...
    def set_is_muted(self, is_muted: bool) -> bool: ...
    def set_is_virtual(self, is_event_stream: bool) -> bool: ...
    def set_name(self, name: str) -> bool: ...
    def set_port(self, port: str) -> bool: ...
    def set_ports(self, ports: list[MixerStreamPort]) -> bool: ...
    def set_state(self, state: MixerStreamState) -> bool: ...
    def set_sysfs_path(self, sysfs_path: str) -> bool: ...
    def set_volume(self, volume: int) -> bool: ...


class MixerStreamClass(GObject.GPointer):
    """
    :Constructors:

    ::

        MixerStreamClass()
    """
    parent_class: GObject.ObjectClass = ...
    push_volume: Callable[[MixerStream, None], bool] = ...
    change_is_muted: Callable[[MixerStream, bool], bool] = ...
    change_port: Callable[[MixerStream, str], bool] = ...

class MixerStreamPort(GObject.GBoxed):
    """
    :Constructors:

    ::

        MixerStreamPort()
    """
    port: str = ...
    human_port: str = ...
    priority: int = ...
    available: bool = ...

class MixerStreamPrivate(GObject.GPointer): ...

class MixerUIDevice(GObject.Object):
    """
    :Constructors:

    ::

        MixerUIDevice(**properties)

    Object GvcMixerUIDevice

    Properties from GvcMixerUIDevice:
      description -> gchararray: Description construct prop
        Set first line description
      origin -> gchararray: origin construct prop
        Set second line description name
      card -> gpointer: Card from pulse
        Set/Get card
      port-name -> gchararray: port-name construct prop
        Set port-name
      stream-id -> guint: stream id assigned by gvc-stream
        Set/Get stream id
      type -> guint: ui-device type
        determine whether its an input and output
      port-available -> gboolean: available
        determine whether this port is available
      icon-name -> gchararray: Icon Name
        Name of icon to display for this card

    Signals from GObject:
      notify (GParam)
    """
    class Props:
        card: None
        description: str
        icon_name: str
        origin: str
        port_available: bool
        port_name: str
        stream_id: int
        type: int
    props: Props = ...
    parent_instance: GObject.Object = ...
    priv: MixerUIDevicePrivate = ...
    def __init__(self, card: None = ...,
                 description: str = ...,
                 icon_name: str = ...,
                 origin: str = ...,
                 port_available: bool = ...,
                 port_name: str = ...,
                 stream_id: int = ...,
                 type: int = ...): ...
    def get_active_profile(self) -> str: ...
    def get_best_profile(self, selected: str | None, current: str) -> str: ...
    def get_description(self) -> str: ...
    def get_gicon(self) -> Gio.Icon: ...
    def get_icon_name(self) -> str: ...
    def get_id(self) -> int: ...
    def get_matching_profile(self, profile: str) -> str: ...
    def get_origin(self) -> str: ...
    def get_port(self) -> str: ...
    def get_profiles(self) -> list[MixerCardProfile]: ...
    def get_stream_id(self) -> int: ...
    def get_supported_profiles(self) -> list[MixerCardProfile]: ...
    def get_top_priority_profile(self) -> str: ...
    def get_user_preferred_profile(self) -> str: ...
    def has_ports(self) -> bool: ...
    def invalidate_stream(self) -> None: ...
    def is_output(self) -> bool: ...
    def set_profiles(self, in_profiles: list[MixerCardProfile]) -> None: ...
    def set_user_preferred_profile(self, profile: str) -> None: ...
    def should_profiles_be_hidden(self) -> bool: ...


class MixerUIDeviceClass(GObject.GPointer):
    """
    :Constructors:

    ::

        MixerUIDeviceClass()
    """
    parent_class: GObject.ObjectClass = ...

class MixerUIDevicePrivate(GObject.GPointer): ...

class HeadsetPortChoice(enum.Enum):
    HEADPHONES = 1
    HEADSET = 2
    MIC = 4
    NONE = 0

class MixerControlState(enum.Enum):
    CLOSED = 0
    CONNECTING = 2
    FAILED = 3
    READY = 1

class MixerStreamState(enum.Enum):
    IDLE = 2
    INVALID = 0
    RUNNING = 1
    SUSPENDED = 3

class MixerUIDeviceDirection(enum.Enum):
    INPUT = 0
    OUTPUT = 1


