import enum
from typing import Any, Callable, Sequence

from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gio

ACCESS_POINT_BANDWIDTH: str = "bandwidth"
ACCESS_POINT_BSSID: str = "bssid"
ACCESS_POINT_FLAGS: str = "flags"
ACCESS_POINT_FREQUENCY: str = "frequency"
ACCESS_POINT_HW_ADDRESS: str = "hw-address"
ACCESS_POINT_LAST_SEEN: str = "last-seen"
ACCESS_POINT_MAX_BITRATE: str = "max-bitrate"
ACCESS_POINT_MODE: str = "mode"
ACCESS_POINT_RSN_FLAGS: str = "rsn-flags"
ACCESS_POINT_SSID: str = "ssid"
ACCESS_POINT_STRENGTH: str = "strength"
ACCESS_POINT_WPA_FLAGS: str = "wpa-flags"
ACTIVE_CONNECTION_CONNECTION: str = "connection"
ACTIVE_CONNECTION_CONTROLLER: str = "controller"
ACTIVE_CONNECTION_DEFAULT: str = "default"
ACTIVE_CONNECTION_DEFAULT6: str = "default6"
ACTIVE_CONNECTION_DEVICES: str = "devices"
ACTIVE_CONNECTION_DHCP4_CONFIG: str = "dhcp4-config"
ACTIVE_CONNECTION_DHCP6_CONFIG: str = "dhcp6-config"
ACTIVE_CONNECTION_ID: str = "id"
ACTIVE_CONNECTION_IP4_CONFIG: str = "ip4-config"
ACTIVE_CONNECTION_IP6_CONFIG: str = "ip6-config"
ACTIVE_CONNECTION_MASTER: str = "master"
ACTIVE_CONNECTION_SPECIFIC_OBJECT_PATH: str = "specific-object-path"
ACTIVE_CONNECTION_STATE: str = "state"
ACTIVE_CONNECTION_STATE_FLAGS: str = "state-flags"
ACTIVE_CONNECTION_TYPE: str = "type"
ACTIVE_CONNECTION_UUID: str = "uuid"
ACTIVE_CONNECTION_VPN: str = "vpn"
BRIDGE_VLAN_VID_MAX: int = 4094
BRIDGE_VLAN_VID_MIN: int = 1
CHECKPOINT_CREATED: str = "created"
CHECKPOINT_DEVICES: str = "devices"
CHECKPOINT_ROLLBACK_TIMEOUT: str = "rollback-timeout"
CLIENT_ACTIVATING_CONNECTION: str = "activating-connection"
CLIENT_ACTIVE_CONNECTIONS: str = "active-connections"
CLIENT_ACTIVE_CONNECTION_ADDED: str = "active-connection-added"
CLIENT_ACTIVE_CONNECTION_REMOVED: str = "active-connection-removed"
CLIENT_ALL_DEVICES: str = "all-devices"
CLIENT_ANY_DEVICE_ADDED: str = "any-device-added"
CLIENT_ANY_DEVICE_REMOVED: str = "any-device-removed"
CLIENT_CAN_MODIFY: str = "can-modify"
CLIENT_CAPABILITIES: str = "capabilities"
CLIENT_CHECKPOINTS: str = "checkpoints"
CLIENT_CONNECTIONS: str = "connections"
CLIENT_CONNECTION_ADDED: str = "connection-added"
CLIENT_CONNECTION_REMOVED: str = "connection-removed"
CLIENT_CONNECTIVITY: str = "connectivity"
CLIENT_CONNECTIVITY_CHECK_AVAILABLE: str = "connectivity-check-available"
CLIENT_CONNECTIVITY_CHECK_ENABLED: str = "connectivity-check-enabled"
CLIENT_CONNECTIVITY_CHECK_URI: str = "connectivity-check-uri"
CLIENT_DBUS_CONNECTION: str = "dbus-connection"
CLIENT_DBUS_NAME_OWNER: str = "dbus-name-owner"
CLIENT_DEVICES: str = "devices"
CLIENT_DEVICE_ADDED: str = "device-added"
CLIENT_DEVICE_REMOVED: str = "device-removed"
CLIENT_DNS_CONFIGURATION: str = "dns-configuration"
CLIENT_DNS_MODE: str = "dns-mode"
CLIENT_DNS_RC_MANAGER: str = "dns-rc-manager"
CLIENT_HOSTNAME: str = "hostname"
CLIENT_INSTANCE_FLAGS: str = "instance-flags"
CLIENT_METERED: str = "metered"
CLIENT_NETWORKING_ENABLED: str = "networking-enabled"
CLIENT_NM_RUNNING: str = "nm-running"
CLIENT_PERMISSIONS_STATE: str = "permissions-state"
CLIENT_PERMISSION_CHANGED: str = "permission-changed"
CLIENT_PRIMARY_CONNECTION: str = "primary-connection"
CLIENT_RADIO_FLAGS: str = "radio-flags"
CLIENT_STARTUP: str = "startup"
CLIENT_STATE: str = "state"
CLIENT_VERSION: str = "version"
CLIENT_VERSION_INFO: str = "version-info"
CLIENT_WIMAX_ENABLED: str = "wimax-enabled"
CLIENT_WIMAX_HARDWARE_ENABLED: str = "wimax-hardware-enabled"
CLIENT_WIRELESS_ENABLED: str = "wireless-enabled"
CLIENT_WIRELESS_HARDWARE_ENABLED: str = "wireless-hardware-enabled"
CLIENT_WWAN_ENABLED: str = "wwan-enabled"
CLIENT_WWAN_HARDWARE_ENABLED: str = "wwan-hardware-enabled"
CONNECTION_CHANGED: str = "changed"
CONNECTION_NORMALIZE_PARAM_IP4_CONFIG_METHOD: str = "ip4-config-method"
CONNECTION_NORMALIZE_PARAM_IP6_CONFIG_METHOD: str = "ip6-config-method"
CONNECTION_SECRETS_CLEARED: str = "secrets-cleared"
CONNECTION_SECRETS_UPDATED: str = "secrets-updated"
DBUS_INTERFACE: str = "org.freedesktop.NetworkManager"
DBUS_INTERFACE_DNS_MANAGER: str = "org.freedesktop.NetworkManager.DnsManager"
DBUS_INTERFACE_SETTINGS: str = "org.freedesktop.NetworkManager.Settings"
DBUS_INTERFACE_SETTINGS_CONNECTION: str = (
    "org.freedesktop.NetworkManager.Settings.Connection"
)
DBUS_INTERFACE_SETTINGS_CONNECTION_SECRETS: str = (
    "org.freedesktop.NetworkManager.Settings.Connection.Secrets"
)
DBUS_INTERFACE_VPN: str = "org.freedesktop.NetworkManager.VPN.Manager"
DBUS_INTERFACE_VPN_CONNECTION: str = "org.freedesktop.NetworkManager.VPN.Connection"
DBUS_INVALID_VPN_CONNECTION: str = (
    "org.freedesktop.NetworkManager.VPNConnections.InvalidVPNConnection"
)
DBUS_NO_ACTIVE_VPN_CONNECTION: str = (
    "org.freedesktop.NetworkManager.VPNConnections.NoActiveVPNConnection"
)
DBUS_NO_VPN_CONNECTIONS: str = (
    "org.freedesktop.NetworkManager.VPNConnections.NoVPNConnections"
)
DBUS_PATH: str = "/org/freedesktop/NetworkManager"
DBUS_PATH_AGENT_MANAGER: str = "/org/freedesktop/NetworkManager/AgentManager"
DBUS_PATH_DNS_MANAGER: str = "/org/freedesktop/NetworkManager/DnsManager"
DBUS_PATH_SECRET_AGENT: str = "/org/freedesktop/NetworkManager/SecretAgent"
DBUS_PATH_SETTINGS: str = "/org/freedesktop/NetworkManager/Settings"
DBUS_PATH_SETTINGS_CONNECTION: str = (
    "/org/freedesktop/NetworkManager/Settings/Connection"
)
DBUS_PATH_VPN: str = "/org/freedesktop/NetworkManager/VPN/Manager"
DBUS_PATH_VPN_CONNECTION: str = "/org/freedesktop/NetworkManager/VPN/Connection"
DBUS_SERVICE: str = "org.freedesktop.NetworkManager"
DBUS_VPN_ALREADY_STARTED: str = "AlreadyStarted"
DBUS_VPN_ALREADY_STOPPED: str = "AlreadyStopped"
DBUS_VPN_BAD_ARGUMENTS: str = "BadArguments"
DBUS_VPN_ERROR_PREFIX: str = "org.freedesktop.NetworkManager.VPN.Error"
DBUS_VPN_INTERACTIVE_NOT_SUPPORTED: str = "InteractiveNotSupported"
DBUS_VPN_SIGNAL_CONNECT_FAILED: str = "ConnectFailed"
DBUS_VPN_SIGNAL_IP4_CONFIG: str = "IP4Config"
DBUS_VPN_SIGNAL_IP_CONFIG_BAD: str = "IPConfigBad"
DBUS_VPN_SIGNAL_LAUNCH_FAILED: str = "LaunchFailed"
DBUS_VPN_SIGNAL_LOGIN_BANNER: str = "LoginBanner"
DBUS_VPN_SIGNAL_LOGIN_FAILED: str = "LoginFailed"
DBUS_VPN_SIGNAL_STATE_CHANGE: str = "StateChange"
DBUS_VPN_SIGNAL_VPN_CONFIG_BAD: str = "VPNConfigBad"
DBUS_VPN_STARTING_IN_PROGRESS: str = "StartingInProgress"
DBUS_VPN_STOPPING_IN_PROGRESS: str = "StoppingInProgress"
DBUS_VPN_WRONG_STATE: str = "WrongState"
DEVICE_6LOWPAN_HW_ADDRESS: str = "hw-address"
DEVICE_6LOWPAN_PARENT: str = "parent"
DEVICE_ACTIVE_CONNECTION: str = "active-connection"
DEVICE_ADSL_CARRIER: str = "carrier"
DEVICE_AUTOCONNECT: str = "autoconnect"
DEVICE_AVAILABLE_CONNECTIONS: str = "available-connections"
DEVICE_BOND_CARRIER: str = "carrier"
DEVICE_BOND_HW_ADDRESS: str = "hw-address"
DEVICE_BOND_SLAVES: str = "slaves"
DEVICE_BRIDGE_CARRIER: str = "carrier"
DEVICE_BRIDGE_HW_ADDRESS: str = "hw-address"
DEVICE_BRIDGE_SLAVES: str = "slaves"
DEVICE_BT_CAPABILITIES: str = "bt-capabilities"
DEVICE_BT_HW_ADDRESS: str = "hw-address"
DEVICE_BT_NAME: str = "name"
DEVICE_CAPABILITIES: str = "capabilities"
DEVICE_DEVICE_TYPE: str = "device-type"
DEVICE_DHCP4_CONFIG: str = "dhcp4-config"
DEVICE_DHCP6_CONFIG: str = "dhcp6-config"
DEVICE_DRIVER: str = "driver"
DEVICE_DRIVER_VERSION: str = "driver-version"
DEVICE_DUMMY_HW_ADDRESS: str = "hw-address"
DEVICE_ETHERNET_CARRIER: str = "carrier"
DEVICE_ETHERNET_HW_ADDRESS: str = "hw-address"
DEVICE_ETHERNET_PERMANENT_HW_ADDRESS: str = "perm-hw-address"
DEVICE_ETHERNET_S390_SUBCHANNELS: str = "s390-subchannels"
DEVICE_ETHERNET_SPEED: str = "speed"
DEVICE_FIRMWARE_MISSING: str = "firmware-missing"
DEVICE_FIRMWARE_VERSION: str = "firmware-version"
DEVICE_GENERIC_HW_ADDRESS: str = "hw-address"
DEVICE_GENERIC_TYPE_DESCRIPTION: str = "type-description"
DEVICE_HSR_MULTICAST_SPEC: str = "multicast-spec"
DEVICE_HSR_PORT1: str = "port1"
DEVICE_HSR_PORT2: str = "port2"
DEVICE_HSR_PRP: str = "prp"
DEVICE_HSR_SUPERVISION_ADDRESS: str = "supervision-address"
DEVICE_HW_ADDRESS: str = "hw-address"
DEVICE_INFINIBAND_CARRIER: str = "carrier"
DEVICE_INFINIBAND_HW_ADDRESS: str = "hw-address"
DEVICE_INTERFACE: str = "interface"
DEVICE_INTERFACE_FLAGS: str = "interface-flags"
DEVICE_IP4_CONFIG: str = "ip4-config"
DEVICE_IP4_CONNECTIVITY: str = "ip4-connectivity"
DEVICE_IP6_CONFIG: str = "ip6-config"
DEVICE_IP6_CONNECTIVITY: str = "ip6-connectivity"
DEVICE_IP_INTERFACE: str = "ip-interface"
DEVICE_IP_TUNNEL_ENCAPSULATION_LIMIT: str = "encapsulation-limit"
DEVICE_IP_TUNNEL_FLAGS: str = "flags"
DEVICE_IP_TUNNEL_FLOW_LABEL: str = "flow-label"
DEVICE_IP_TUNNEL_FWMARK: str = "fwmark"
DEVICE_IP_TUNNEL_INPUT_KEY: str = "input-key"
DEVICE_IP_TUNNEL_LOCAL: str = "local"
DEVICE_IP_TUNNEL_MODE: str = "mode"
DEVICE_IP_TUNNEL_OUTPUT_KEY: str = "output-key"
DEVICE_IP_TUNNEL_PARENT: str = "parent"
DEVICE_IP_TUNNEL_PATH_MTU_DISCOVERY: str = "path-mtu-discovery"
DEVICE_IP_TUNNEL_REMOTE: str = "remote"
DEVICE_IP_TUNNEL_TOS: str = "tos"
DEVICE_IP_TUNNEL_TTL: str = "ttl"
DEVICE_LLDP_NEIGHBORS: str = "lldp-neighbors"
DEVICE_MACSEC_CIPHER_SUITE: str = "cipher-suite"
DEVICE_MACSEC_ENCODING_SA: str = "encoding-sa"
DEVICE_MACSEC_ENCRYPT: str = "encrypt"
DEVICE_MACSEC_ES: str = "es"
DEVICE_MACSEC_HW_ADDRESS: str = "hw-address"
DEVICE_MACSEC_ICV_LENGTH: str = "icv-length"
DEVICE_MACSEC_INCLUDE_SCI: str = "include-sci"
DEVICE_MACSEC_PARENT: str = "parent"
DEVICE_MACSEC_PROTECT: str = "protect"
DEVICE_MACSEC_REPLAY_PROTECT: str = "replay-protect"
DEVICE_MACSEC_SCB: str = "scb"
DEVICE_MACSEC_SCI: str = "sci"
DEVICE_MACSEC_VALIDATION: str = "validation"
DEVICE_MACSEC_WINDOW: str = "window"
DEVICE_MACVLAN_HW_ADDRESS: str = "hw-address"
DEVICE_MACVLAN_MODE: str = "mode"
DEVICE_MACVLAN_NO_PROMISC: str = "no-promisc"
DEVICE_MACVLAN_PARENT: str = "parent"
DEVICE_MACVLAN_TAP: str = "tap"
DEVICE_MANAGED: str = "managed"
DEVICE_METERED: str = "metered"
DEVICE_MODEM_APN: str = "apn"
DEVICE_MODEM_CURRENT_CAPABILITIES: str = "current-capabilities"
DEVICE_MODEM_DEVICE_ID: str = "device-id"
DEVICE_MODEM_MODEM_CAPABILITIES: str = "modem-capabilities"
DEVICE_MODEM_OPERATOR_CODE: str = "operator-code"
DEVICE_MTU: str = "mtu"
DEVICE_NM_PLUGIN_MISSING: str = "nm-plugin-missing"
DEVICE_OLPC_MESH_ACTIVE_CHANNEL: str = "active-channel"
DEVICE_OLPC_MESH_COMPANION: str = "companion"
DEVICE_OLPC_MESH_HW_ADDRESS: str = "hw-address"
DEVICE_OVS_BRIDGE_SLAVES: str = "slaves"
DEVICE_OVS_PORT_SLAVES: str = "slaves"
DEVICE_PATH: str = "path"
DEVICE_PHYSICAL_PORT_ID: str = "physical-port-id"
DEVICE_PORTS: str = "ports"
DEVICE_PRODUCT: str = "product"
DEVICE_REAL: str = "real"
DEVICE_STATE: str = "state"
DEVICE_STATE_REASON: str = "state-reason"
DEVICE_TEAM_CARRIER: str = "carrier"
DEVICE_TEAM_CONFIG: str = "config"
DEVICE_TEAM_HW_ADDRESS: str = "hw-address"
DEVICE_TEAM_SLAVES: str = "slaves"
DEVICE_TUN_GROUP: str = "group"
DEVICE_TUN_HW_ADDRESS: str = "hw-address"
DEVICE_TUN_MODE: str = "mode"
DEVICE_TUN_MULTI_QUEUE: str = "multi-queue"
DEVICE_TUN_NO_PI: str = "no-pi"
DEVICE_TUN_OWNER: str = "owner"
DEVICE_TUN_VNET_HDR: str = "vnet-hdr"
DEVICE_UDI: str = "udi"
DEVICE_VENDOR: str = "vendor"
DEVICE_VETH_PEER: str = "peer"
DEVICE_VLAN_CARRIER: str = "carrier"
DEVICE_VLAN_HW_ADDRESS: str = "hw-address"
DEVICE_VLAN_PARENT: str = "parent"
DEVICE_VLAN_VLAN_ID: str = "vlan-id"
DEVICE_VRF_TABLE: str = "table"
DEVICE_VXLAN_AGEING: str = "ageing"
DEVICE_VXLAN_CARRIER: str = "carrier"
DEVICE_VXLAN_DST_PORT: str = "dst-port"
DEVICE_VXLAN_GROUP: str = "group"
DEVICE_VXLAN_HW_ADDRESS: str = "hw-address"
DEVICE_VXLAN_ID: str = "id"
DEVICE_VXLAN_L2MISS: str = "l2miss"
DEVICE_VXLAN_L3MISS: str = "l3miss"
DEVICE_VXLAN_LEARNING: str = "learning"
DEVICE_VXLAN_LIMIT: str = "limit"
DEVICE_VXLAN_LOCAL: str = "local"
DEVICE_VXLAN_PARENT: str = "parent"
DEVICE_VXLAN_PROXY: str = "proxy"
DEVICE_VXLAN_RSC: str = "rsc"
DEVICE_VXLAN_SRC_PORT_MAX: str = "src-port-max"
DEVICE_VXLAN_SRC_PORT_MIN: str = "src-port-min"
DEVICE_VXLAN_TOS: str = "tos"
DEVICE_VXLAN_TTL: str = "ttl"
DEVICE_WIFI_ACCESS_POINTS: str = "access-points"
DEVICE_WIFI_ACTIVE_ACCESS_POINT: str = "active-access-point"
DEVICE_WIFI_BITRATE: str = "bitrate"
DEVICE_WIFI_CAPABILITIES: str = "wireless-capabilities"
DEVICE_WIFI_HW_ADDRESS: str = "hw-address"
DEVICE_WIFI_LAST_SCAN: str = "last-scan"
DEVICE_WIFI_MODE: str = "mode"
DEVICE_WIFI_P2P_HW_ADDRESS: str = "hw-address"
DEVICE_WIFI_P2P_PEERS: str = "peers"
DEVICE_WIFI_P2P_WFDIES: str = "wfdies"
DEVICE_WIFI_PERMANENT_HW_ADDRESS: str = "perm-hw-address"
DEVICE_WIMAX_ACTIVE_NSP: str = "active-nsp"
DEVICE_WIMAX_BSID: str = "bsid"
DEVICE_WIMAX_CENTER_FREQUENCY: str = "center-frequency"
DEVICE_WIMAX_CINR: str = "cinr"
DEVICE_WIMAX_HW_ADDRESS: str = "hw-address"
DEVICE_WIMAX_NSPS: str = "nsps"
DEVICE_WIMAX_RSSI: str = "rssi"
DEVICE_WIMAX_TX_POWER: str = "tx-power"
DEVICE_WIREGUARD_FWMARK: str = "fwmark"
DEVICE_WIREGUARD_LISTEN_PORT: str = "listen-port"
DEVICE_WIREGUARD_PUBLIC_KEY: str = "public-key"
DEVICE_WPAN_HW_ADDRESS: str = "hw-address"
DHCP_CONFIG_FAMILY: str = "family"
DHCP_CONFIG_OPTIONS: str = "options"
ETHTOOL_OPTNAME_CHANNELS_COMBINED: str = "channels-combined"
ETHTOOL_OPTNAME_CHANNELS_OTHER: str = "channels-other"
ETHTOOL_OPTNAME_CHANNELS_RX: str = "channels-rx"
ETHTOOL_OPTNAME_CHANNELS_TX: str = "channels-tx"
ETHTOOL_OPTNAME_COALESCE_ADAPTIVE_RX: str = "coalesce-adaptive-rx"
ETHTOOL_OPTNAME_COALESCE_ADAPTIVE_TX: str = "coalesce-adaptive-tx"
ETHTOOL_OPTNAME_COALESCE_PKT_RATE_HIGH: str = "coalesce-pkt-rate-high"
ETHTOOL_OPTNAME_COALESCE_PKT_RATE_LOW: str = "coalesce-pkt-rate-low"
ETHTOOL_OPTNAME_COALESCE_RX_FRAMES: str = "coalesce-rx-frames"
ETHTOOL_OPTNAME_COALESCE_RX_FRAMES_HIGH: str = "coalesce-rx-frames-high"
ETHTOOL_OPTNAME_COALESCE_RX_FRAMES_IRQ: str = "coalesce-rx-frames-irq"
ETHTOOL_OPTNAME_COALESCE_RX_FRAMES_LOW: str = "coalesce-rx-frames-low"
ETHTOOL_OPTNAME_COALESCE_RX_USECS: str = "coalesce-rx-usecs"
ETHTOOL_OPTNAME_COALESCE_RX_USECS_HIGH: str = "coalesce-rx-usecs-high"
ETHTOOL_OPTNAME_COALESCE_RX_USECS_IRQ: str = "coalesce-rx-usecs-irq"
ETHTOOL_OPTNAME_COALESCE_RX_USECS_LOW: str = "coalesce-rx-usecs-low"
ETHTOOL_OPTNAME_COALESCE_SAMPLE_INTERVAL: str = "coalesce-sample-interval"
ETHTOOL_OPTNAME_COALESCE_STATS_BLOCK_USECS: str = "coalesce-stats-block-usecs"
ETHTOOL_OPTNAME_COALESCE_TX_FRAMES: str = "coalesce-tx-frames"
ETHTOOL_OPTNAME_COALESCE_TX_FRAMES_HIGH: str = "coalesce-tx-frames-high"
ETHTOOL_OPTNAME_COALESCE_TX_FRAMES_IRQ: str = "coalesce-tx-frames-irq"
ETHTOOL_OPTNAME_COALESCE_TX_FRAMES_LOW: str = "coalesce-tx-frames-low"
ETHTOOL_OPTNAME_COALESCE_TX_USECS: str = "coalesce-tx-usecs"
ETHTOOL_OPTNAME_COALESCE_TX_USECS_HIGH: str = "coalesce-tx-usecs-high"
ETHTOOL_OPTNAME_COALESCE_TX_USECS_IRQ: str = "coalesce-tx-usecs-irq"
ETHTOOL_OPTNAME_COALESCE_TX_USECS_LOW: str = "coalesce-tx-usecs-low"
ETHTOOL_OPTNAME_EEE_ENABLED: str = "eee-enabled"
ETHTOOL_OPTNAME_FEATURE_ESP_HW_OFFLOAD: str = "feature-esp-hw-offload"
ETHTOOL_OPTNAME_FEATURE_ESP_TX_CSUM_HW_OFFLOAD: str = "feature-esp-tx-csum-hw-offload"
ETHTOOL_OPTNAME_FEATURE_FCOE_MTU: str = "feature-fcoe-mtu"
ETHTOOL_OPTNAME_FEATURE_GRO: str = "feature-gro"
ETHTOOL_OPTNAME_FEATURE_GSO: str = "feature-gso"
ETHTOOL_OPTNAME_FEATURE_HIGHDMA: str = "feature-highdma"
ETHTOOL_OPTNAME_FEATURE_HW_TC_OFFLOAD: str = "feature-hw-tc-offload"
ETHTOOL_OPTNAME_FEATURE_L2_FWD_OFFLOAD: str = "feature-l2-fwd-offload"
ETHTOOL_OPTNAME_FEATURE_LOOPBACK: str = "feature-loopback"
ETHTOOL_OPTNAME_FEATURE_LRO: str = "feature-lro"
ETHTOOL_OPTNAME_FEATURE_MACSEC_HW_OFFLOAD: str = "feature-macsec-hw-offload"
ETHTOOL_OPTNAME_FEATURE_NTUPLE: str = "feature-ntuple"
ETHTOOL_OPTNAME_FEATURE_RX: str = "feature-rx"
ETHTOOL_OPTNAME_FEATURE_RXHASH: str = "feature-rxhash"
ETHTOOL_OPTNAME_FEATURE_RXVLAN: str = "feature-rxvlan"
ETHTOOL_OPTNAME_FEATURE_RX_ALL: str = "feature-rx-all"
ETHTOOL_OPTNAME_FEATURE_RX_FCS: str = "feature-rx-fcs"
ETHTOOL_OPTNAME_FEATURE_RX_GRO_HW: str = "feature-rx-gro-hw"
ETHTOOL_OPTNAME_FEATURE_RX_GRO_LIST: str = "feature-rx-gro-list"
ETHTOOL_OPTNAME_FEATURE_RX_UDP_GRO_FORWARDING: str = "feature-rx-udp-gro-forwarding"
ETHTOOL_OPTNAME_FEATURE_RX_UDP_TUNNEL_PORT_OFFLOAD: str = (
    "feature-rx-udp_tunnel-port-offload"
)
ETHTOOL_OPTNAME_FEATURE_RX_VLAN_FILTER: str = "feature-rx-vlan-filter"
ETHTOOL_OPTNAME_FEATURE_RX_VLAN_STAG_FILTER: str = "feature-rx-vlan-stag-filter"
ETHTOOL_OPTNAME_FEATURE_RX_VLAN_STAG_HW_PARSE: str = "feature-rx-vlan-stag-hw-parse"
ETHTOOL_OPTNAME_FEATURE_SG: str = "feature-sg"
ETHTOOL_OPTNAME_FEATURE_TLS_HW_RECORD: str = "feature-tls-hw-record"
ETHTOOL_OPTNAME_FEATURE_TLS_HW_RX_OFFLOAD: str = "feature-tls-hw-rx-offload"
ETHTOOL_OPTNAME_FEATURE_TLS_HW_TX_OFFLOAD: str = "feature-tls-hw-tx-offload"
ETHTOOL_OPTNAME_FEATURE_TSO: str = "feature-tso"
ETHTOOL_OPTNAME_FEATURE_TX: str = "feature-tx"
ETHTOOL_OPTNAME_FEATURE_TXVLAN: str = "feature-txvlan"
ETHTOOL_OPTNAME_FEATURE_TX_CHECKSUM_FCOE_CRC: str = "feature-tx-checksum-fcoe-crc"
ETHTOOL_OPTNAME_FEATURE_TX_CHECKSUM_IPV4: str = "feature-tx-checksum-ipv4"
ETHTOOL_OPTNAME_FEATURE_TX_CHECKSUM_IPV6: str = "feature-tx-checksum-ipv6"
ETHTOOL_OPTNAME_FEATURE_TX_CHECKSUM_IP_GENERIC: str = "feature-tx-checksum-ip-generic"
ETHTOOL_OPTNAME_FEATURE_TX_CHECKSUM_SCTP: str = "feature-tx-checksum-sctp"
ETHTOOL_OPTNAME_FEATURE_TX_ESP_SEGMENTATION: str = "feature-tx-esp-segmentation"
ETHTOOL_OPTNAME_FEATURE_TX_FCOE_SEGMENTATION: str = "feature-tx-fcoe-segmentation"
ETHTOOL_OPTNAME_FEATURE_TX_GRE_CSUM_SEGMENTATION: str = (
    "feature-tx-gre-csum-segmentation"
)
ETHTOOL_OPTNAME_FEATURE_TX_GRE_SEGMENTATION: str = "feature-tx-gre-segmentation"
ETHTOOL_OPTNAME_FEATURE_TX_GSO_LIST: str = "feature-tx-gso-list"
ETHTOOL_OPTNAME_FEATURE_TX_GSO_PARTIAL: str = "feature-tx-gso-partial"
ETHTOOL_OPTNAME_FEATURE_TX_GSO_ROBUST: str = "feature-tx-gso-robust"
ETHTOOL_OPTNAME_FEATURE_TX_IPXIP4_SEGMENTATION: str = "feature-tx-ipxip4-segmentation"
ETHTOOL_OPTNAME_FEATURE_TX_IPXIP6_SEGMENTATION: str = "feature-tx-ipxip6-segmentation"
ETHTOOL_OPTNAME_FEATURE_TX_NOCACHE_COPY: str = "feature-tx-nocache-copy"
ETHTOOL_OPTNAME_FEATURE_TX_SCATTER_GATHER: str = "feature-tx-scatter-gather"
ETHTOOL_OPTNAME_FEATURE_TX_SCATTER_GATHER_FRAGLIST: str = (
    "feature-tx-scatter-gather-fraglist"
)
ETHTOOL_OPTNAME_FEATURE_TX_SCTP_SEGMENTATION: str = "feature-tx-sctp-segmentation"
ETHTOOL_OPTNAME_FEATURE_TX_TCP6_SEGMENTATION: str = "feature-tx-tcp6-segmentation"
ETHTOOL_OPTNAME_FEATURE_TX_TCP_ECN_SEGMENTATION: str = "feature-tx-tcp-ecn-segmentation"
ETHTOOL_OPTNAME_FEATURE_TX_TCP_MANGLEID_SEGMENTATION: str = (
    "feature-tx-tcp-mangleid-segmentation"
)
ETHTOOL_OPTNAME_FEATURE_TX_TCP_SEGMENTATION: str = "feature-tx-tcp-segmentation"
ETHTOOL_OPTNAME_FEATURE_TX_TUNNEL_REMCSUM_SEGMENTATION: str = (
    "feature-tx-tunnel-remcsum-segmentation"
)
ETHTOOL_OPTNAME_FEATURE_TX_UDP_SEGMENTATION: str = "feature-tx-udp-segmentation"
ETHTOOL_OPTNAME_FEATURE_TX_UDP_TNL_CSUM_SEGMENTATION: str = (
    "feature-tx-udp_tnl-csum-segmentation"
)
ETHTOOL_OPTNAME_FEATURE_TX_UDP_TNL_SEGMENTATION: str = "feature-tx-udp_tnl-segmentation"
ETHTOOL_OPTNAME_FEATURE_TX_VLAN_STAG_HW_INSERT: str = "feature-tx-vlan-stag-hw-insert"
ETHTOOL_OPTNAME_PAUSE_AUTONEG: str = "pause-autoneg"
ETHTOOL_OPTNAME_PAUSE_RX: str = "pause-rx"
ETHTOOL_OPTNAME_PAUSE_TX: str = "pause-tx"
ETHTOOL_OPTNAME_RING_RX: str = "ring-rx"
ETHTOOL_OPTNAME_RING_RX_JUMBO: str = "ring-rx-jumbo"
ETHTOOL_OPTNAME_RING_RX_MINI: str = "ring-rx-mini"
ETHTOOL_OPTNAME_RING_TX: str = "ring-tx"
IP_ADDRESS_ATTRIBUTE_LABEL: str = "label"
IP_CONFIG_ADDRESSES: str = "addresses"
IP_CONFIG_DOMAINS: str = "domains"
IP_CONFIG_FAMILY: str = "family"
IP_CONFIG_GATEWAY: str = "gateway"
IP_CONFIG_NAMESERVERS: str = "nameservers"
IP_CONFIG_ROUTES: str = "routes"
IP_CONFIG_SEARCHES: str = "searches"
IP_CONFIG_WINS_SERVERS: str = "wins-servers"
IP_ROUTE_ATTRIBUTE_ADVMSS: str = "advmss"
IP_ROUTE_ATTRIBUTE_CWND: str = "cwnd"
IP_ROUTE_ATTRIBUTE_FROM: str = "from"
IP_ROUTE_ATTRIBUTE_INITCWND: str = "initcwnd"
IP_ROUTE_ATTRIBUTE_INITRWND: str = "initrwnd"
IP_ROUTE_ATTRIBUTE_LOCK_ADVMSS: str = "lock-advmss"
IP_ROUTE_ATTRIBUTE_LOCK_CWND: str = "lock-cwnd"
IP_ROUTE_ATTRIBUTE_LOCK_INITCWND: str = "lock-initcwnd"
IP_ROUTE_ATTRIBUTE_LOCK_INITRWND: str = "lock-initrwnd"
IP_ROUTE_ATTRIBUTE_LOCK_MTU: str = "lock-mtu"
IP_ROUTE_ATTRIBUTE_LOCK_WINDOW: str = "lock-window"
IP_ROUTE_ATTRIBUTE_MTU: str = "mtu"
IP_ROUTE_ATTRIBUTE_ONLINK: str = "onlink"
IP_ROUTE_ATTRIBUTE_QUICKACK: str = "quickack"
IP_ROUTE_ATTRIBUTE_RTO_MIN: str = "rto_min"
IP_ROUTE_ATTRIBUTE_SCOPE: str = "scope"
IP_ROUTE_ATTRIBUTE_SRC: str = "src"
IP_ROUTE_ATTRIBUTE_TABLE: str = "table"
IP_ROUTE_ATTRIBUTE_TOS: str = "tos"
IP_ROUTE_ATTRIBUTE_TYPE: str = "type"
IP_ROUTE_ATTRIBUTE_WEIGHT: str = "weight"
IP_ROUTE_ATTRIBUTE_WINDOW: str = "window"
LLDP_ATTR_CHASSIS_ID: str = "chassis-id"
LLDP_ATTR_CHASSIS_ID_TYPE: str = "chassis-id-type"
LLDP_ATTR_DESTINATION: str = "destination"
LLDP_ATTR_IEEE_802_1_PPVID: str = "ieee-802-1-ppvid"
LLDP_ATTR_IEEE_802_1_PPVIDS: str = "ieee-802-1-ppvids"
LLDP_ATTR_IEEE_802_1_PPVID_FLAGS: str = "ieee-802-1-ppvid-flags"
LLDP_ATTR_IEEE_802_1_PVID: str = "ieee-802-1-pvid"
LLDP_ATTR_IEEE_802_1_VID: str = "ieee-802-1-vid"
LLDP_ATTR_IEEE_802_1_VLANS: str = "ieee-802-1-vlans"
LLDP_ATTR_IEEE_802_1_VLAN_NAME: str = "ieee-802-1-vlan-name"
LLDP_ATTR_IEEE_802_3_MAC_PHY_CONF: str = "ieee-802-3-mac-phy-conf"
LLDP_ATTR_IEEE_802_3_MAX_FRAME_SIZE: str = "ieee-802-3-max-frame-size"
LLDP_ATTR_IEEE_802_3_POWER_VIA_MDI: str = "ieee-802-3-power-via-mdi"
LLDP_ATTR_MANAGEMENT_ADDRESSES: str = "management-addresses"
LLDP_ATTR_MUD_URL: str = "mud-url"
LLDP_ATTR_PORT_DESCRIPTION: str = "port-description"
LLDP_ATTR_PORT_ID: str = "port-id"
LLDP_ATTR_PORT_ID_TYPE: str = "port-id-type"
LLDP_ATTR_RAW: str = "raw"
LLDP_ATTR_SYSTEM_CAPABILITIES: str = "system-capabilities"
LLDP_ATTR_SYSTEM_DESCRIPTION: str = "system-description"
LLDP_ATTR_SYSTEM_NAME: str = "system-name"
LLDP_DEST_NEAREST_BRIDGE: str = "nearest-bridge"
LLDP_DEST_NEAREST_CUSTOMER_BRIDGE: str = "nearest-customer-bridge"
LLDP_DEST_NEAREST_NON_TPMR_BRIDGE: str = "nearest-non-tpmr-bridge"
MAJOR_VERSION: int = 1
MICRO_VERSION: int = 10
MINOR_VERSION: int = 48
OBJECT_CLIENT: str = "client"
OBJECT_PATH: str = "path"
REMOTE_CONNECTION_DBUS_CONNECTION: str = "dbus-connection"
REMOTE_CONNECTION_FILENAME: str = "filename"
REMOTE_CONNECTION_FLAGS: str = "flags"
REMOTE_CONNECTION_PATH: str = "path"
REMOTE_CONNECTION_UNSAVED: str = "unsaved"
REMOTE_CONNECTION_VERSION_ID: str = "version-id"
REMOTE_CONNECTION_VISIBLE: str = "visible"
SECRET_AGENT_OLD_AUTO_REGISTER: str = "auto-register"
SECRET_AGENT_OLD_CAPABILITIES: str = "capabilities"
SECRET_AGENT_OLD_DBUS_CONNECTION: str = "dbus-connection"
SECRET_AGENT_OLD_IDENTIFIER: str = "identifier"
SECRET_AGENT_OLD_REGISTERED: str = "registered"
SECRET_TAG_DYNAMIC_CHALLENGE: str = "x-dynamic-challenge:"
SECRET_TAG_DYNAMIC_CHALLENGE_ECHO: str = "x-dynamic-challenge-echo:"
SECRET_TAG_VPN_MSG: str = "x-vpn-message:"
SETTING_6LOWPAN_PARENT: str = "parent"
SETTING_6LOWPAN_SETTING_NAME: str = "6lowpan"
SETTING_802_1X_ALTSUBJECT_MATCHES: str = "altsubject-matches"
SETTING_802_1X_ANONYMOUS_IDENTITY: str = "anonymous-identity"
SETTING_802_1X_AUTH_TIMEOUT: str = "auth-timeout"
SETTING_802_1X_CA_CERT: str = "ca-cert"
SETTING_802_1X_CA_CERT_PASSWORD: str = "ca-cert-password"
SETTING_802_1X_CA_CERT_PASSWORD_FLAGS: str = "ca-cert-password-flags"
SETTING_802_1X_CA_PATH: str = "ca-path"
SETTING_802_1X_CERT_SCHEME_PREFIX_PATH: str = "file://"
SETTING_802_1X_CERT_SCHEME_PREFIX_PKCS11: str = "pkcs11:"
SETTING_802_1X_CLIENT_CERT: str = "client-cert"
SETTING_802_1X_CLIENT_CERT_PASSWORD: str = "client-cert-password"
SETTING_802_1X_CLIENT_CERT_PASSWORD_FLAGS: str = "client-cert-password-flags"
SETTING_802_1X_DOMAIN_MATCH: str = "domain-match"
SETTING_802_1X_DOMAIN_SUFFIX_MATCH: str = "domain-suffix-match"
SETTING_802_1X_EAP: str = "eap"
SETTING_802_1X_IDENTITY: str = "identity"
SETTING_802_1X_OPENSSL_CIPHERS: str = "openssl-ciphers"
SETTING_802_1X_OPTIONAL: str = "optional"
SETTING_802_1X_PAC_FILE: str = "pac-file"
SETTING_802_1X_PASSWORD: str = "password"
SETTING_802_1X_PASSWORD_FLAGS: str = "password-flags"
SETTING_802_1X_PASSWORD_RAW: str = "password-raw"
SETTING_802_1X_PASSWORD_RAW_FLAGS: str = "password-raw-flags"
SETTING_802_1X_PHASE1_AUTH_FLAGS: str = "phase1-auth-flags"
SETTING_802_1X_PHASE1_FAST_PROVISIONING: str = "phase1-fast-provisioning"
SETTING_802_1X_PHASE1_PEAPLABEL: str = "phase1-peaplabel"
SETTING_802_1X_PHASE1_PEAPVER: str = "phase1-peapver"
SETTING_802_1X_PHASE2_ALTSUBJECT_MATCHES: str = "phase2-altsubject-matches"
SETTING_802_1X_PHASE2_AUTH: str = "phase2-auth"
SETTING_802_1X_PHASE2_AUTHEAP: str = "phase2-autheap"
SETTING_802_1X_PHASE2_CA_CERT: str = "phase2-ca-cert"
SETTING_802_1X_PHASE2_CA_CERT_PASSWORD: str = "phase2-ca-cert-password"
SETTING_802_1X_PHASE2_CA_CERT_PASSWORD_FLAGS: str = "phase2-ca-cert-password-flags"
SETTING_802_1X_PHASE2_CA_PATH: str = "phase2-ca-path"
SETTING_802_1X_PHASE2_CLIENT_CERT: str = "phase2-client-cert"
SETTING_802_1X_PHASE2_CLIENT_CERT_PASSWORD: str = "phase2-client-cert-password"
SETTING_802_1X_PHASE2_CLIENT_CERT_PASSWORD_FLAGS: str = (
    "phase2-client-cert-password-flags"
)
SETTING_802_1X_PHASE2_DOMAIN_MATCH: str = "phase2-domain-match"
SETTING_802_1X_PHASE2_DOMAIN_SUFFIX_MATCH: str = "phase2-domain-suffix-match"
SETTING_802_1X_PHASE2_PRIVATE_KEY: str = "phase2-private-key"
SETTING_802_1X_PHASE2_PRIVATE_KEY_PASSWORD: str = "phase2-private-key-password"
SETTING_802_1X_PHASE2_PRIVATE_KEY_PASSWORD_FLAGS: str = (
    "phase2-private-key-password-flags"
)
SETTING_802_1X_PHASE2_SUBJECT_MATCH: str = "phase2-subject-match"
SETTING_802_1X_PIN: str = "pin"
SETTING_802_1X_PIN_FLAGS: str = "pin-flags"
SETTING_802_1X_PRIVATE_KEY: str = "private-key"
SETTING_802_1X_PRIVATE_KEY_PASSWORD: str = "private-key-password"
SETTING_802_1X_PRIVATE_KEY_PASSWORD_FLAGS: str = "private-key-password-flags"
SETTING_802_1X_SETTING_NAME: str = "802-1x"
SETTING_802_1X_SUBJECT_MATCH: str = "subject-match"
SETTING_802_1X_SYSTEM_CA_CERTS: str = "system-ca-certs"
SETTING_ADSL_ENCAPSULATION: str = "encapsulation"
SETTING_ADSL_ENCAPSULATION_LLC: str = "llc"
SETTING_ADSL_ENCAPSULATION_VCMUX: str = "vcmux"
SETTING_ADSL_PASSWORD: str = "password"
SETTING_ADSL_PASSWORD_FLAGS: str = "password-flags"
SETTING_ADSL_PROTOCOL: str = "protocol"
SETTING_ADSL_PROTOCOL_IPOATM: str = "ipoatm"
SETTING_ADSL_PROTOCOL_PPPOA: str = "pppoa"
SETTING_ADSL_PROTOCOL_PPPOE: str = "pppoe"
SETTING_ADSL_SETTING_NAME: str = "adsl"
SETTING_ADSL_USERNAME: str = "username"
SETTING_ADSL_VCI: str = "vci"
SETTING_ADSL_VPI: str = "vpi"
SETTING_BLUETOOTH_BDADDR: str = "bdaddr"
SETTING_BLUETOOTH_SETTING_NAME: str = "bluetooth"
SETTING_BLUETOOTH_TYPE: str = "type"
SETTING_BLUETOOTH_TYPE_DUN: str = "dun"
SETTING_BLUETOOTH_TYPE_NAP: str = "nap"
SETTING_BLUETOOTH_TYPE_PANU: str = "panu"
SETTING_BOND_OPTIONS: str = "options"
SETTING_BOND_OPTION_ACTIVE_SLAVE: str = "active_slave"
SETTING_BOND_OPTION_AD_ACTOR_SYSTEM: str = "ad_actor_system"
SETTING_BOND_OPTION_AD_ACTOR_SYS_PRIO: str = "ad_actor_sys_prio"
SETTING_BOND_OPTION_AD_SELECT: str = "ad_select"
SETTING_BOND_OPTION_AD_USER_PORT_KEY: str = "ad_user_port_key"
SETTING_BOND_OPTION_ALL_SLAVES_ACTIVE: str = "all_slaves_active"
SETTING_BOND_OPTION_ARP_ALL_TARGETS: str = "arp_all_targets"
SETTING_BOND_OPTION_ARP_INTERVAL: str = "arp_interval"
SETTING_BOND_OPTION_ARP_IP_TARGET: str = "arp_ip_target"
SETTING_BOND_OPTION_ARP_MISSED_MAX: str = "arp_missed_max"
SETTING_BOND_OPTION_ARP_VALIDATE: str = "arp_validate"
SETTING_BOND_OPTION_BALANCE_SLB: str = "balance-slb"
SETTING_BOND_OPTION_DOWNDELAY: str = "downdelay"
SETTING_BOND_OPTION_FAIL_OVER_MAC: str = "fail_over_mac"
SETTING_BOND_OPTION_LACP_ACTIVE: str = "lacp_active"
SETTING_BOND_OPTION_LACP_RATE: str = "lacp_rate"
SETTING_BOND_OPTION_LP_INTERVAL: str = "lp_interval"
SETTING_BOND_OPTION_MIIMON: str = "miimon"
SETTING_BOND_OPTION_MIN_LINKS: str = "min_links"
SETTING_BOND_OPTION_MODE: str = "mode"
SETTING_BOND_OPTION_NS_IP6_TARGET: str = "ns_ip6_target"
SETTING_BOND_OPTION_NUM_GRAT_ARP: str = "num_grat_arp"
SETTING_BOND_OPTION_NUM_UNSOL_NA: str = "num_unsol_na"
SETTING_BOND_OPTION_PACKETS_PER_SLAVE: str = "packets_per_slave"
SETTING_BOND_OPTION_PEER_NOTIF_DELAY: str = "peer_notif_delay"
SETTING_BOND_OPTION_PRIMARY: str = "primary"
SETTING_BOND_OPTION_PRIMARY_RESELECT: str = "primary_reselect"
SETTING_BOND_OPTION_RESEND_IGMP: str = "resend_igmp"
SETTING_BOND_OPTION_TLB_DYNAMIC_LB: str = "tlb_dynamic_lb"
SETTING_BOND_OPTION_UPDELAY: str = "updelay"
SETTING_BOND_OPTION_USE_CARRIER: str = "use_carrier"
SETTING_BOND_OPTION_XMIT_HASH_POLICY: str = "xmit_hash_policy"
SETTING_BOND_PORT_PRIO: str = "prio"
SETTING_BOND_PORT_QUEUE_ID: str = "queue-id"
SETTING_BOND_PORT_SETTING_NAME: str = "bond-port"
SETTING_BOND_SETTING_NAME: str = "bond"
SETTING_BRIDGE_AGEING_TIME: str = "ageing-time"
SETTING_BRIDGE_FORWARD_DELAY: str = "forward-delay"
SETTING_BRIDGE_GROUP_ADDRESS: str = "group-address"
SETTING_BRIDGE_GROUP_FORWARD_MASK: str = "group-forward-mask"
SETTING_BRIDGE_HELLO_TIME: str = "hello-time"
SETTING_BRIDGE_MAC_ADDRESS: str = "mac-address"
SETTING_BRIDGE_MAX_AGE: str = "max-age"
SETTING_BRIDGE_MULTICAST_HASH_MAX: str = "multicast-hash-max"
SETTING_BRIDGE_MULTICAST_LAST_MEMBER_COUNT: str = "multicast-last-member-count"
SETTING_BRIDGE_MULTICAST_LAST_MEMBER_INTERVAL: str = "multicast-last-member-interval"
SETTING_BRIDGE_MULTICAST_MEMBERSHIP_INTERVAL: str = "multicast-membership-interval"
SETTING_BRIDGE_MULTICAST_QUERIER: str = "multicast-querier"
SETTING_BRIDGE_MULTICAST_QUERIER_INTERVAL: str = "multicast-querier-interval"
SETTING_BRIDGE_MULTICAST_QUERY_INTERVAL: str = "multicast-query-interval"
SETTING_BRIDGE_MULTICAST_QUERY_RESPONSE_INTERVAL: str = (
    "multicast-query-response-interval"
)
SETTING_BRIDGE_MULTICAST_QUERY_USE_IFADDR: str = "multicast-query-use-ifaddr"
SETTING_BRIDGE_MULTICAST_ROUTER: str = "multicast-router"
SETTING_BRIDGE_MULTICAST_SNOOPING: str = "multicast-snooping"
SETTING_BRIDGE_MULTICAST_STARTUP_QUERY_COUNT: str = "multicast-startup-query-count"
SETTING_BRIDGE_MULTICAST_STARTUP_QUERY_INTERVAL: str = (
    "multicast-startup-query-interval"
)
SETTING_BRIDGE_PORT_HAIRPIN_MODE: str = "hairpin-mode"
SETTING_BRIDGE_PORT_PATH_COST: str = "path-cost"
SETTING_BRIDGE_PORT_PRIORITY: str = "priority"
SETTING_BRIDGE_PORT_SETTING_NAME: str = "bridge-port"
SETTING_BRIDGE_PORT_VLANS: str = "vlans"
SETTING_BRIDGE_PRIORITY: str = "priority"
SETTING_BRIDGE_SETTING_NAME: str = "bridge"
SETTING_BRIDGE_STP: str = "stp"
SETTING_BRIDGE_VLANS: str = "vlans"
SETTING_BRIDGE_VLAN_DEFAULT_PVID: str = "vlan-default-pvid"
SETTING_BRIDGE_VLAN_FILTERING: str = "vlan-filtering"
SETTING_BRIDGE_VLAN_PROTOCOL: str = "vlan-protocol"
SETTING_BRIDGE_VLAN_STATS_ENABLED: str = "vlan-stats-enabled"
SETTING_CDMA_MTU: str = "mtu"
SETTING_CDMA_NUMBER: str = "number"
SETTING_CDMA_PASSWORD: str = "password"
SETTING_CDMA_PASSWORD_FLAGS: str = "password-flags"
SETTING_CDMA_SETTING_NAME: str = "cdma"
SETTING_CDMA_USERNAME: str = "username"
SETTING_CONNECTION_AUTH_RETRIES: str = "auth-retries"
SETTING_CONNECTION_AUTOCONNECT: str = "autoconnect"
SETTING_CONNECTION_AUTOCONNECT_PORTS: str = "autoconnect-ports"
SETTING_CONNECTION_AUTOCONNECT_PRIORITY: str = "autoconnect-priority"
SETTING_CONNECTION_AUTOCONNECT_PRIORITY_DEFAULT: int = 0
SETTING_CONNECTION_AUTOCONNECT_PRIORITY_MAX: int = 999
SETTING_CONNECTION_AUTOCONNECT_PRIORITY_MIN: int = -999
SETTING_CONNECTION_AUTOCONNECT_RETRIES: str = "autoconnect-retries"
SETTING_CONNECTION_AUTOCONNECT_SLAVES: str = "autoconnect-slaves"
SETTING_CONNECTION_CONTROLLER: str = "controller"
SETTING_CONNECTION_DNS_OVER_TLS: str = "dns-over-tls"
SETTING_CONNECTION_DOWN_ON_POWEROFF: str = "down-on-poweroff"
SETTING_CONNECTION_GATEWAY_PING_TIMEOUT: str = "gateway-ping-timeout"
SETTING_CONNECTION_ID: str = "id"
SETTING_CONNECTION_INTERFACE_NAME: str = "interface-name"
SETTING_CONNECTION_LLDP: str = "lldp"
SETTING_CONNECTION_LLMNR: str = "llmnr"
SETTING_CONNECTION_MASTER: str = "master"
SETTING_CONNECTION_MDNS: str = "mdns"
SETTING_CONNECTION_METERED: str = "metered"
SETTING_CONNECTION_MPTCP_FLAGS: str = "mptcp-flags"
SETTING_CONNECTION_MUD_URL: str = "mud-url"
SETTING_CONNECTION_MULTI_CONNECT: str = "multi-connect"
SETTING_CONNECTION_PERMISSIONS: str = "permissions"
SETTING_CONNECTION_PORT_TYPE: str = "port-type"
SETTING_CONNECTION_READ_ONLY: str = "read-only"
SETTING_CONNECTION_SECONDARIES: str = "secondaries"
SETTING_CONNECTION_SETTING_NAME: str = "connection"
SETTING_CONNECTION_SLAVE_TYPE: str = "slave-type"
SETTING_CONNECTION_STABLE_ID: str = "stable-id"
SETTING_CONNECTION_TIMESTAMP: str = "timestamp"
SETTING_CONNECTION_TYPE: str = "type"
SETTING_CONNECTION_UUID: str = "uuid"
SETTING_CONNECTION_WAIT_ACTIVATION_DELAY: str = "wait-activation-delay"
SETTING_CONNECTION_WAIT_DEVICE_TIMEOUT: str = "wait-device-timeout"
SETTING_CONNECTION_ZONE: str = "zone"
SETTING_DCB_APP_FCOE_FLAGS: str = "app-fcoe-flags"
SETTING_DCB_APP_FCOE_MODE: str = "app-fcoe-mode"
SETTING_DCB_APP_FCOE_PRIORITY: str = "app-fcoe-priority"
SETTING_DCB_APP_FIP_FLAGS: str = "app-fip-flags"
SETTING_DCB_APP_FIP_PRIORITY: str = "app-fip-priority"
SETTING_DCB_APP_ISCSI_FLAGS: str = "app-iscsi-flags"
SETTING_DCB_APP_ISCSI_PRIORITY: str = "app-iscsi-priority"
SETTING_DCB_FCOE_MODE_FABRIC: str = "fabric"
SETTING_DCB_FCOE_MODE_VN2VN: str = "vn2vn"
SETTING_DCB_PRIORITY_BANDWIDTH: str = "priority-bandwidth"
SETTING_DCB_PRIORITY_FLOW_CONTROL: str = "priority-flow-control"
SETTING_DCB_PRIORITY_FLOW_CONTROL_FLAGS: str = "priority-flow-control-flags"
SETTING_DCB_PRIORITY_GROUP_BANDWIDTH: str = "priority-group-bandwidth"
SETTING_DCB_PRIORITY_GROUP_FLAGS: str = "priority-group-flags"
SETTING_DCB_PRIORITY_GROUP_ID: str = "priority-group-id"
SETTING_DCB_PRIORITY_STRICT_BANDWIDTH: str = "priority-strict-bandwidth"
SETTING_DCB_PRIORITY_TRAFFIC_CLASS: str = "priority-traffic-class"
SETTING_DCB_SETTING_NAME: str = "dcb"
SETTING_DNS_OPTION_ATTEMPTS: str = "attempts"
SETTING_DNS_OPTION_DEBUG: str = "debug"
SETTING_DNS_OPTION_EDNS0: str = "edns0"
SETTING_DNS_OPTION_INET6: str = "inet6"
SETTING_DNS_OPTION_INTERNAL_NO_ADD_EDNS0: str = "_no-add-edns0"
SETTING_DNS_OPTION_INTERNAL_NO_ADD_TRUST_AD: str = "_no-add-trust-ad"
SETTING_DNS_OPTION_IP6_BYTESTRING: str = "ip6-bytestring"
SETTING_DNS_OPTION_IP6_DOTINT: str = "ip6-dotint"
SETTING_DNS_OPTION_NDOTS: str = "ndots"
SETTING_DNS_OPTION_NO_AAAA: str = "no-aaaa"
SETTING_DNS_OPTION_NO_CHECK_NAMES: str = "no-check-names"
SETTING_DNS_OPTION_NO_IP6_DOTINT: str = "no-ip6-dotint"
SETTING_DNS_OPTION_NO_RELOAD: str = "no-reload"
SETTING_DNS_OPTION_NO_TLD_QUERY: str = "no-tld-query"
SETTING_DNS_OPTION_ROTATE: str = "rotate"
SETTING_DNS_OPTION_SINGLE_REQUEST: str = "single-request"
SETTING_DNS_OPTION_SINGLE_REQUEST_REOPEN: str = "single-request-reopen"
SETTING_DNS_OPTION_TIMEOUT: str = "timeout"
SETTING_DNS_OPTION_TRUST_AD: str = "trust-ad"
SETTING_DNS_OPTION_USE_VC: str = "use-vc"
SETTING_DUMMY_SETTING_NAME: str = "dummy"
SETTING_ETHTOOL_SETTING_NAME: str = "ethtool"
SETTING_GENERIC_DEVICE_HANDLER: str = "device-handler"
SETTING_GENERIC_SETTING_NAME: str = "generic"
SETTING_GSM_APN: str = "apn"
SETTING_GSM_AUTO_CONFIG: str = "auto-config"
SETTING_GSM_DEVICE_ID: str = "device-id"
SETTING_GSM_HOME_ONLY: str = "home-only"
SETTING_GSM_INITIAL_EPS_BEARER_APN: str = "initial-eps-bearer-apn"
SETTING_GSM_INITIAL_EPS_BEARER_CONFIGURE: str = "initial-eps-bearer-configure"
SETTING_GSM_MTU: str = "mtu"
SETTING_GSM_NETWORK_ID: str = "network-id"
SETTING_GSM_NUMBER: str = "number"
SETTING_GSM_PASSWORD: str = "password"
SETTING_GSM_PASSWORD_FLAGS: str = "password-flags"
SETTING_GSM_PIN: str = "pin"
SETTING_GSM_PIN_FLAGS: str = "pin-flags"
SETTING_GSM_SETTING_NAME: str = "gsm"
SETTING_GSM_SIM_ID: str = "sim-id"
SETTING_GSM_SIM_OPERATOR_ID: str = "sim-operator-id"
SETTING_GSM_USERNAME: str = "username"
SETTING_HOSTNAME_FROM_DHCP: str = "from-dhcp"
SETTING_HOSTNAME_FROM_DNS_LOOKUP: str = "from-dns-lookup"
SETTING_HOSTNAME_ONLY_FROM_DEFAULT: str = "only-from-default"
SETTING_HOSTNAME_PRIORITY: str = "priority"
SETTING_HOSTNAME_SETTING_NAME: str = "hostname"
SETTING_HSR_MULTICAST_SPEC: str = "multicast-spec"
SETTING_HSR_PORT1: str = "port1"
SETTING_HSR_PORT2: str = "port2"
SETTING_HSR_PRP: str = "prp"
SETTING_HSR_SETTING_NAME: str = "hsr"
SETTING_INFINIBAND_MAC_ADDRESS: str = "mac-address"
SETTING_INFINIBAND_MTU: str = "mtu"
SETTING_INFINIBAND_PARENT: str = "parent"
SETTING_INFINIBAND_P_KEY: str = "p-key"
SETTING_INFINIBAND_SETTING_NAME: str = "infiniband"
SETTING_INFINIBAND_TRANSPORT_MODE: str = "transport-mode"
SETTING_IP4_CONFIG_DHCP_CLIENT_ID: str = "dhcp-client-id"
SETTING_IP4_CONFIG_DHCP_FQDN: str = "dhcp-fqdn"
SETTING_IP4_CONFIG_DHCP_VENDOR_CLASS_IDENTIFIER: str = "dhcp-vendor-class-identifier"
SETTING_IP4_CONFIG_LINK_LOCAL: str = "link-local"
SETTING_IP4_CONFIG_METHOD_AUTO: str = "auto"
SETTING_IP4_CONFIG_METHOD_DISABLED: str = "disabled"
SETTING_IP4_CONFIG_METHOD_LINK_LOCAL: str = "link-local"
SETTING_IP4_CONFIG_METHOD_MANUAL: str = "manual"
SETTING_IP4_CONFIG_METHOD_SHARED: str = "shared"
SETTING_IP4_CONFIG_SETTING_NAME: str = "ipv4"
SETTING_IP6_CONFIG_ADDR_GEN_MODE: str = "addr-gen-mode"
SETTING_IP6_CONFIG_DHCP_DUID: str = "dhcp-duid"
SETTING_IP6_CONFIG_DHCP_PD_HINT: str = "dhcp-pd-hint"
SETTING_IP6_CONFIG_IP6_PRIVACY: str = "ip6-privacy"
SETTING_IP6_CONFIG_METHOD_AUTO: str = "auto"
SETTING_IP6_CONFIG_METHOD_DHCP: str = "dhcp"
SETTING_IP6_CONFIG_METHOD_DISABLED: str = "disabled"
SETTING_IP6_CONFIG_METHOD_IGNORE: str = "ignore"
SETTING_IP6_CONFIG_METHOD_LINK_LOCAL: str = "link-local"
SETTING_IP6_CONFIG_METHOD_MANUAL: str = "manual"
SETTING_IP6_CONFIG_METHOD_SHARED: str = "shared"
SETTING_IP6_CONFIG_MTU: str = "mtu"
SETTING_IP6_CONFIG_RA_TIMEOUT: str = "ra-timeout"
SETTING_IP6_CONFIG_SETTING_NAME: str = "ipv6"
SETTING_IP6_CONFIG_TEMP_PREFERRED_LIFETIME: str = "temp-preferred-lifetime"
SETTING_IP6_CONFIG_TEMP_VALID_LIFETIME: str = "temp-valid-lifetime"
SETTING_IP6_CONFIG_TOKEN: str = "token"
SETTING_IP_CONFIG_ADDRESSES: str = "addresses"
SETTING_IP_CONFIG_AUTO_ROUTE_EXT_GW: str = "auto-route-ext-gw"
SETTING_IP_CONFIG_DAD_TIMEOUT: str = "dad-timeout"
SETTING_IP_CONFIG_DAD_TIMEOUT_MAX: int = 30000
SETTING_IP_CONFIG_DHCP_DSCP: str = "dhcp-dscp"
SETTING_IP_CONFIG_DHCP_HOSTNAME: str = "dhcp-hostname"
SETTING_IP_CONFIG_DHCP_HOSTNAME_FLAGS: str = "dhcp-hostname-flags"
SETTING_IP_CONFIG_DHCP_IAID: str = "dhcp-iaid"
SETTING_IP_CONFIG_DHCP_REJECT_SERVERS: str = "dhcp-reject-servers"
SETTING_IP_CONFIG_DHCP_SEND_HOSTNAME: str = "dhcp-send-hostname"
SETTING_IP_CONFIG_DHCP_SEND_RELEASE: str = "dhcp-send-release"
SETTING_IP_CONFIG_DHCP_TIMEOUT: str = "dhcp-timeout"
SETTING_IP_CONFIG_DNS: str = "dns"
SETTING_IP_CONFIG_DNS_OPTIONS: str = "dns-options"
SETTING_IP_CONFIG_DNS_PRIORITY: str = "dns-priority"
SETTING_IP_CONFIG_DNS_SEARCH: str = "dns-search"
SETTING_IP_CONFIG_GATEWAY: str = "gateway"
SETTING_IP_CONFIG_IGNORE_AUTO_DNS: str = "ignore-auto-dns"
SETTING_IP_CONFIG_IGNORE_AUTO_ROUTES: str = "ignore-auto-routes"
SETTING_IP_CONFIG_MAY_FAIL: str = "may-fail"
SETTING_IP_CONFIG_METHOD: str = "method"
SETTING_IP_CONFIG_NEVER_DEFAULT: str = "never-default"
SETTING_IP_CONFIG_REPLACE_LOCAL_RULE: str = "replace-local-rule"
SETTING_IP_CONFIG_REQUIRED_TIMEOUT: str = "required-timeout"
SETTING_IP_CONFIG_ROUTES: str = "routes"
SETTING_IP_CONFIG_ROUTE_METRIC: str = "route-metric"
SETTING_IP_CONFIG_ROUTE_TABLE: str = "route-table"
SETTING_IP_CONFIG_ROUTING_RULES: str = "routing-rules"
SETTING_IP_TUNNEL_ENCAPSULATION_LIMIT: str = "encapsulation-limit"
SETTING_IP_TUNNEL_FLAGS: str = "flags"
SETTING_IP_TUNNEL_FLOW_LABEL: str = "flow-label"
SETTING_IP_TUNNEL_FWMARK: str = "fwmark"
SETTING_IP_TUNNEL_INPUT_KEY: str = "input-key"
SETTING_IP_TUNNEL_LOCAL: str = "local"
SETTING_IP_TUNNEL_MODE: str = "mode"
SETTING_IP_TUNNEL_MTU: str = "mtu"
SETTING_IP_TUNNEL_OUTPUT_KEY: str = "output-key"
SETTING_IP_TUNNEL_PARENT: str = "parent"
SETTING_IP_TUNNEL_PATH_MTU_DISCOVERY: str = "path-mtu-discovery"
SETTING_IP_TUNNEL_REMOTE: str = "remote"
SETTING_IP_TUNNEL_SETTING_NAME: str = "ip-tunnel"
SETTING_IP_TUNNEL_TOS: str = "tos"
SETTING_IP_TUNNEL_TTL: str = "ttl"
SETTING_LINK_GRO_MAX_SIZE: str = "gro-max-size"
SETTING_LINK_GSO_MAX_SEGMENTS: str = "gso-max-segments"
SETTING_LINK_GSO_MAX_SIZE: str = "gso-max-size"
SETTING_LINK_SETTING_NAME: str = "link"
SETTING_LINK_TX_QUEUE_LENGTH: str = "tx-queue-length"
SETTING_LOOPBACK_MTU: str = "mtu"
SETTING_LOOPBACK_SETTING_NAME: str = "loopback"
SETTING_MACSEC_ENCRYPT: str = "encrypt"
SETTING_MACSEC_MKA_CAK: str = "mka-cak"
SETTING_MACSEC_MKA_CAK_FLAGS: str = "mka-cak-flags"
SETTING_MACSEC_MKA_CAK_LENGTH: int = 32
SETTING_MACSEC_MKA_CKN: str = "mka-ckn"
SETTING_MACSEC_MKA_CKN_LENGTH: int = 64
SETTING_MACSEC_MODE: str = "mode"
SETTING_MACSEC_OFFLOAD: str = "offload"
SETTING_MACSEC_PARENT: str = "parent"
SETTING_MACSEC_PORT: str = "port"
SETTING_MACSEC_SEND_SCI: str = "send-sci"
SETTING_MACSEC_SETTING_NAME: str = "macsec"
SETTING_MACSEC_VALIDATION: str = "validation"
SETTING_MACVLAN_MODE: str = "mode"
SETTING_MACVLAN_PARENT: str = "parent"
SETTING_MACVLAN_PROMISCUOUS: str = "promiscuous"
SETTING_MACVLAN_SETTING_NAME: str = "macvlan"
SETTING_MACVLAN_TAP: str = "tap"
SETTING_MATCH_DRIVER: str = "driver"
SETTING_MATCH_INTERFACE_NAME: str = "interface-name"
SETTING_MATCH_KERNEL_COMMAND_LINE: str = "kernel-command-line"
SETTING_MATCH_PATH: str = "path"
SETTING_MATCH_SETTING_NAME: str = "match"
SETTING_NAME: str = "name"
SETTING_OLPC_MESH_CHANNEL: str = "channel"
SETTING_OLPC_MESH_DHCP_ANYCAST_ADDRESS: str = "dhcp-anycast-address"
SETTING_OLPC_MESH_SETTING_NAME: str = "802-11-olpc-mesh"
SETTING_OLPC_MESH_SSID: str = "ssid"
SETTING_OVS_BRIDGE_DATAPATH_TYPE: str = "datapath-type"
SETTING_OVS_BRIDGE_FAIL_MODE: str = "fail-mode"
SETTING_OVS_BRIDGE_MCAST_SNOOPING_ENABLE: str = "mcast-snooping-enable"
SETTING_OVS_BRIDGE_RSTP_ENABLE: str = "rstp-enable"
SETTING_OVS_BRIDGE_SETTING_NAME: str = "ovs-bridge"
SETTING_OVS_BRIDGE_STP_ENABLE: str = "stp-enable"
SETTING_OVS_DPDK_DEVARGS: str = "devargs"
SETTING_OVS_DPDK_N_RXQ: str = "n-rxq"
SETTING_OVS_DPDK_N_RXQ_DESC: str = "n-rxq-desc"
SETTING_OVS_DPDK_N_TXQ_DESC: str = "n-txq-desc"
SETTING_OVS_DPDK_SETTING_NAME: str = "ovs-dpdk"
SETTING_OVS_EXTERNAL_IDS_DATA: str = "data"
SETTING_OVS_EXTERNAL_IDS_SETTING_NAME: str = "ovs-external-ids"
SETTING_OVS_INTERFACE_OFPORT_REQUEST: str = "ofport-request"
SETTING_OVS_INTERFACE_SETTING_NAME: str = "ovs-interface"
SETTING_OVS_INTERFACE_TYPE: str = "type"
SETTING_OVS_OTHER_CONFIG_DATA: str = "data"
SETTING_OVS_OTHER_CONFIG_SETTING_NAME: str = "ovs-other-config"
SETTING_OVS_PATCH_PEER: str = "peer"
SETTING_OVS_PATCH_SETTING_NAME: str = "ovs-patch"
SETTING_OVS_PORT_BOND_DOWNDELAY: str = "bond-downdelay"
SETTING_OVS_PORT_BOND_MODE: str = "bond-mode"
SETTING_OVS_PORT_BOND_UPDELAY: str = "bond-updelay"
SETTING_OVS_PORT_LACP: str = "lacp"
SETTING_OVS_PORT_SETTING_NAME: str = "ovs-port"
SETTING_OVS_PORT_TAG: str = "tag"
SETTING_OVS_PORT_TRUNKS: str = "trunks"
SETTING_OVS_PORT_VLAN_MODE: str = "vlan-mode"
SETTING_PARAM_FUZZY_IGNORE: int = 2048
SETTING_PARAM_REQUIRED: int = 512
SETTING_PARAM_SECRET: int = 1024
SETTING_PPPOE_PARENT: str = "parent"
SETTING_PPPOE_PASSWORD: str = "password"
SETTING_PPPOE_PASSWORD_FLAGS: str = "password-flags"
SETTING_PPPOE_SERVICE: str = "service"
SETTING_PPPOE_SETTING_NAME: str = "pppoe"
SETTING_PPPOE_USERNAME: str = "username"
SETTING_PPP_BAUD: str = "baud"
SETTING_PPP_CRTSCTS: str = "crtscts"
SETTING_PPP_LCP_ECHO_FAILURE: str = "lcp-echo-failure"
SETTING_PPP_LCP_ECHO_INTERVAL: str = "lcp-echo-interval"
SETTING_PPP_MPPE_STATEFUL: str = "mppe-stateful"
SETTING_PPP_MRU: str = "mru"
SETTING_PPP_MTU: str = "mtu"
SETTING_PPP_NOAUTH: str = "noauth"
SETTING_PPP_NOBSDCOMP: str = "nobsdcomp"
SETTING_PPP_NODEFLATE: str = "nodeflate"
SETTING_PPP_NO_VJ_COMP: str = "no-vj-comp"
SETTING_PPP_REFUSE_CHAP: str = "refuse-chap"
SETTING_PPP_REFUSE_EAP: str = "refuse-eap"
SETTING_PPP_REFUSE_MSCHAP: str = "refuse-mschap"
SETTING_PPP_REFUSE_MSCHAPV2: str = "refuse-mschapv2"
SETTING_PPP_REFUSE_PAP: str = "refuse-pap"
SETTING_PPP_REQUIRE_MPPE: str = "require-mppe"
SETTING_PPP_REQUIRE_MPPE_128: str = "require-mppe-128"
SETTING_PPP_SETTING_NAME: str = "ppp"
SETTING_PROXY_BROWSER_ONLY: str = "browser-only"
SETTING_PROXY_METHOD: str = "method"
SETTING_PROXY_PAC_SCRIPT: str = "pac-script"
SETTING_PROXY_PAC_URL: str = "pac-url"
SETTING_PROXY_SETTING_NAME: str = "proxy"
SETTING_SERIAL_BAUD: str = "baud"
SETTING_SERIAL_BITS: str = "bits"
SETTING_SERIAL_PARITY: str = "parity"
SETTING_SERIAL_SEND_DELAY: str = "send-delay"
SETTING_SERIAL_SETTING_NAME: str = "serial"
SETTING_SERIAL_STOPBITS: str = "stopbits"
SETTING_SRIOV_AUTOPROBE_DRIVERS: str = "autoprobe-drivers"
SETTING_SRIOV_ESWITCH_ENCAP_MODE: str = "eswitch-encap-mode"
SETTING_SRIOV_ESWITCH_INLINE_MODE: str = "eswitch-inline-mode"
SETTING_SRIOV_ESWITCH_MODE: str = "eswitch-mode"
SETTING_SRIOV_SETTING_NAME: str = "sriov"
SETTING_SRIOV_TOTAL_VFS: str = "total-vfs"
SETTING_SRIOV_VFS: str = "vfs"
SETTING_TC_CONFIG_QDISCS: str = "qdiscs"
SETTING_TC_CONFIG_SETTING_NAME: str = "tc"
SETTING_TC_CONFIG_TFILTERS: str = "tfilters"
SETTING_TEAM_CONFIG: str = "config"
SETTING_TEAM_LINK_WATCHERS: str = "link-watchers"
SETTING_TEAM_MCAST_REJOIN_COUNT: str = "mcast-rejoin-count"
SETTING_TEAM_MCAST_REJOIN_INTERVAL: str = "mcast-rejoin-interval"
SETTING_TEAM_NOTIFY_MCAST_COUNT_ACTIVEBACKUP_DEFAULT: int = 1
SETTING_TEAM_NOTIFY_PEERS_COUNT: str = "notify-peers-count"
SETTING_TEAM_NOTIFY_PEERS_COUNT_ACTIVEBACKUP_DEFAULT: int = 1
SETTING_TEAM_NOTIFY_PEERS_INTERVAL: str = "notify-peers-interval"
SETTING_TEAM_PORT_CONFIG: str = "config"
SETTING_TEAM_PORT_LACP_KEY: str = "lacp-key"
SETTING_TEAM_PORT_LACP_PRIO: str = "lacp-prio"
SETTING_TEAM_PORT_LACP_PRIO_DEFAULT: int = 255
SETTING_TEAM_PORT_LINK_WATCHERS: str = "link-watchers"
SETTING_TEAM_PORT_PRIO: str = "prio"
SETTING_TEAM_PORT_QUEUE_ID: str = "queue-id"
SETTING_TEAM_PORT_QUEUE_ID_DEFAULT: int = -1
SETTING_TEAM_PORT_SETTING_NAME: str = "team-port"
SETTING_TEAM_PORT_STICKY: str = "sticky"
SETTING_TEAM_RUNNER: str = "runner"
SETTING_TEAM_RUNNER_ACTIVE: str = "runner-active"
SETTING_TEAM_RUNNER_ACTIVEBACKUP: str = "activebackup"
SETTING_TEAM_RUNNER_AGG_SELECT_POLICY: str = "runner-agg-select-policy"
SETTING_TEAM_RUNNER_AGG_SELECT_POLICY_BANDWIDTH: str = "bandwidth"
SETTING_TEAM_RUNNER_AGG_SELECT_POLICY_COUNT: str = "count"
SETTING_TEAM_RUNNER_AGG_SELECT_POLICY_LACP_PRIO: str = "lacp_prio"
SETTING_TEAM_RUNNER_AGG_SELECT_POLICY_LACP_PRIO_STABLE: str = "lacp_prio_stable"
SETTING_TEAM_RUNNER_AGG_SELECT_POLICY_PORT_CONFIG: str = "port_config"
SETTING_TEAM_RUNNER_BROADCAST: str = "broadcast"
SETTING_TEAM_RUNNER_FAST_RATE: str = "runner-fast-rate"
SETTING_TEAM_RUNNER_HWADDR_POLICY: str = "runner-hwaddr-policy"
SETTING_TEAM_RUNNER_HWADDR_POLICY_BY_ACTIVE: str = "by_active"
SETTING_TEAM_RUNNER_HWADDR_POLICY_ONLY_ACTIVE: str = "only_active"
SETTING_TEAM_RUNNER_HWADDR_POLICY_SAME_ALL: str = "same_all"
SETTING_TEAM_RUNNER_LACP: str = "lacp"
SETTING_TEAM_RUNNER_LOADBALANCE: str = "loadbalance"
SETTING_TEAM_RUNNER_MIN_PORTS: str = "runner-min-ports"
SETTING_TEAM_RUNNER_RANDOM: str = "random"
SETTING_TEAM_RUNNER_ROUNDROBIN: str = "roundrobin"
SETTING_TEAM_RUNNER_SYS_PRIO: str = "runner-sys-prio"
SETTING_TEAM_RUNNER_SYS_PRIO_DEFAULT: int = 65535
SETTING_TEAM_RUNNER_TX_BALANCER: str = "runner-tx-balancer"
SETTING_TEAM_RUNNER_TX_BALANCER_INTERVAL: str = "runner-tx-balancer-interval"
SETTING_TEAM_RUNNER_TX_BALANCER_INTERVAL_DEFAULT: int = 50
SETTING_TEAM_RUNNER_TX_HASH: str = "runner-tx-hash"
SETTING_TEAM_SETTING_NAME: str = "team"
SETTING_TUN_GROUP: str = "group"
SETTING_TUN_MODE: str = "mode"
SETTING_TUN_MULTI_QUEUE: str = "multi-queue"
SETTING_TUN_OWNER: str = "owner"
SETTING_TUN_PI: str = "pi"
SETTING_TUN_SETTING_NAME: str = "tun"
SETTING_TUN_VNET_HDR: str = "vnet-hdr"
SETTING_USER_DATA: str = "data"
SETTING_USER_SETTING_NAME: str = "user"
SETTING_VETH_PEER: str = "peer"
SETTING_VETH_SETTING_NAME: str = "veth"
SETTING_VLAN_EGRESS_PRIORITY_MAP: str = "egress-priority-map"
SETTING_VLAN_FLAGS: str = "flags"
SETTING_VLAN_ID: str = "id"
SETTING_VLAN_INGRESS_PRIORITY_MAP: str = "ingress-priority-map"
SETTING_VLAN_PARENT: str = "parent"
SETTING_VLAN_PROTOCOL: str = "protocol"
SETTING_VLAN_SETTING_NAME: str = "vlan"
SETTING_VPN_DATA: str = "data"
SETTING_VPN_PERSISTENT: str = "persistent"
SETTING_VPN_SECRETS: str = "secrets"
SETTING_VPN_SERVICE_TYPE: str = "service-type"
SETTING_VPN_SETTING_NAME: str = "vpn"
SETTING_VPN_TIMEOUT: str = "timeout"
SETTING_VPN_USER_NAME: str = "user-name"
SETTING_VRF_SETTING_NAME: str = "vrf"
SETTING_VRF_TABLE: str = "table"
SETTING_VXLAN_AGEING: str = "ageing"
SETTING_VXLAN_DESTINATION_PORT: str = "destination-port"
SETTING_VXLAN_ID: str = "id"
SETTING_VXLAN_L2_MISS: str = "l2-miss"
SETTING_VXLAN_L3_MISS: str = "l3-miss"
SETTING_VXLAN_LEARNING: str = "learning"
SETTING_VXLAN_LIMIT: str = "limit"
SETTING_VXLAN_LOCAL: str = "local"
SETTING_VXLAN_PARENT: str = "parent"
SETTING_VXLAN_PROXY: str = "proxy"
SETTING_VXLAN_REMOTE: str = "remote"
SETTING_VXLAN_RSC: str = "rsc"
SETTING_VXLAN_SETTING_NAME: str = "vxlan"
SETTING_VXLAN_SOURCE_PORT_MAX: str = "source-port-max"
SETTING_VXLAN_SOURCE_PORT_MIN: str = "source-port-min"
SETTING_VXLAN_TOS: str = "tos"
SETTING_VXLAN_TTL: str = "ttl"
SETTING_WIFI_P2P_PEER: str = "peer"
SETTING_WIFI_P2P_SETTING_NAME: str = "wifi-p2p"
SETTING_WIFI_P2P_WFD_IES: str = "wfd-ies"
SETTING_WIFI_P2P_WPS_METHOD: str = "wps-method"
SETTING_WIMAX_MAC_ADDRESS: str = "mac-address"
SETTING_WIMAX_NETWORK_NAME: str = "network-name"
SETTING_WIMAX_SETTING_NAME: str = "wimax"
SETTING_WIRED_ACCEPT_ALL_MAC_ADDRESSES: str = "accept-all-mac-addresses"
SETTING_WIRED_AUTO_NEGOTIATE: str = "auto-negotiate"
SETTING_WIRED_CLONED_MAC_ADDRESS: str = "cloned-mac-address"
SETTING_WIRED_DUPLEX: str = "duplex"
SETTING_WIRED_GENERATE_MAC_ADDRESS_MASK: str = "generate-mac-address-mask"
SETTING_WIRED_MAC_ADDRESS: str = "mac-address"
SETTING_WIRED_MAC_ADDRESS_BLACKLIST: str = "mac-address-blacklist"
SETTING_WIRED_MAC_ADDRESS_DENYLIST: str = "mac-address-denylist"
SETTING_WIRED_MTU: str = "mtu"
SETTING_WIRED_PORT: str = "port"
SETTING_WIRED_S390_NETTYPE: str = "s390-nettype"
SETTING_WIRED_S390_OPTIONS: str = "s390-options"
SETTING_WIRED_S390_SUBCHANNELS: str = "s390-subchannels"
SETTING_WIRED_SETTING_NAME: str = "802-3-ethernet"
SETTING_WIRED_SPEED: str = "speed"
SETTING_WIRED_WAKE_ON_LAN: str = "wake-on-lan"
SETTING_WIRED_WAKE_ON_LAN_PASSWORD: str = "wake-on-lan-password"
SETTING_WIREGUARD_FWMARK: str = "fwmark"
SETTING_WIREGUARD_IP4_AUTO_DEFAULT_ROUTE: str = "ip4-auto-default-route"
SETTING_WIREGUARD_IP6_AUTO_DEFAULT_ROUTE: str = "ip6-auto-default-route"
SETTING_WIREGUARD_LISTEN_PORT: str = "listen-port"
SETTING_WIREGUARD_MTU: str = "mtu"
SETTING_WIREGUARD_PEERS: str = "peers"
SETTING_WIREGUARD_PEER_ROUTES: str = "peer-routes"
SETTING_WIREGUARD_PRIVATE_KEY: str = "private-key"
SETTING_WIREGUARD_PRIVATE_KEY_FLAGS: str = "private-key-flags"
SETTING_WIREGUARD_SETTING_NAME: str = "wireguard"
SETTING_WIRELESS_AP_ISOLATION: str = "ap-isolation"
SETTING_WIRELESS_BAND: str = "band"
SETTING_WIRELESS_BSSID: str = "bssid"
SETTING_WIRELESS_CHANNEL: str = "channel"
SETTING_WIRELESS_CLONED_MAC_ADDRESS: str = "cloned-mac-address"
SETTING_WIRELESS_GENERATE_MAC_ADDRESS_MASK: str = "generate-mac-address-mask"
SETTING_WIRELESS_HIDDEN: str = "hidden"
SETTING_WIRELESS_MAC_ADDRESS: str = "mac-address"
SETTING_WIRELESS_MAC_ADDRESS_BLACKLIST: str = "mac-address-blacklist"
SETTING_WIRELESS_MAC_ADDRESS_DENYLIST: str = "mac-address-denylist"
SETTING_WIRELESS_MAC_ADDRESS_RANDOMIZATION: str = "mac-address-randomization"
SETTING_WIRELESS_MODE: str = "mode"
SETTING_WIRELESS_MODE_ADHOC: str = "adhoc"
SETTING_WIRELESS_MODE_AP: str = "ap"
SETTING_WIRELESS_MODE_INFRA: str = "infrastructure"
SETTING_WIRELESS_MODE_MESH: str = "mesh"
SETTING_WIRELESS_MTU: str = "mtu"
SETTING_WIRELESS_POWERSAVE: str = "powersave"
SETTING_WIRELESS_RATE: str = "rate"
SETTING_WIRELESS_SECURITY_AUTH_ALG: str = "auth-alg"
SETTING_WIRELESS_SECURITY_FILS: str = "fils"
SETTING_WIRELESS_SECURITY_GROUP: str = "group"
SETTING_WIRELESS_SECURITY_KEY_MGMT: str = "key-mgmt"
SETTING_WIRELESS_SECURITY_LEAP_PASSWORD: str = "leap-password"
SETTING_WIRELESS_SECURITY_LEAP_PASSWORD_FLAGS: str = "leap-password-flags"
SETTING_WIRELESS_SECURITY_LEAP_USERNAME: str = "leap-username"
SETTING_WIRELESS_SECURITY_PAIRWISE: str = "pairwise"
SETTING_WIRELESS_SECURITY_PMF: str = "pmf"
SETTING_WIRELESS_SECURITY_PROTO: str = "proto"
SETTING_WIRELESS_SECURITY_PSK: str = "psk"
SETTING_WIRELESS_SECURITY_PSK_FLAGS: str = "psk-flags"
SETTING_WIRELESS_SECURITY_SETTING_NAME: str = "802-11-wireless-security"
SETTING_WIRELESS_SECURITY_WEP_KEY0: str = "wep-key0"
SETTING_WIRELESS_SECURITY_WEP_KEY1: str = "wep-key1"
SETTING_WIRELESS_SECURITY_WEP_KEY2: str = "wep-key2"
SETTING_WIRELESS_SECURITY_WEP_KEY3: str = "wep-key3"
SETTING_WIRELESS_SECURITY_WEP_KEY_FLAGS: str = "wep-key-flags"
SETTING_WIRELESS_SECURITY_WEP_KEY_TYPE: str = "wep-key-type"
SETTING_WIRELESS_SECURITY_WEP_TX_KEYIDX: str = "wep-tx-keyidx"
SETTING_WIRELESS_SECURITY_WPS_METHOD: str = "wps-method"
SETTING_WIRELESS_SEEN_BSSIDS: str = "seen-bssids"
SETTING_WIRELESS_SETTING_NAME: str = "802-11-wireless"
SETTING_WIRELESS_SSID: str = "ssid"
SETTING_WIRELESS_TX_POWER: str = "tx-power"
SETTING_WIRELESS_WAKE_ON_WLAN: str = "wake-on-wlan"
SETTING_WPAN_CHANNEL: str = "channel"
SETTING_WPAN_CHANNEL_DEFAULT: int = -1
SETTING_WPAN_MAC_ADDRESS: str = "mac-address"
SETTING_WPAN_PAGE: str = "page"
SETTING_WPAN_PAGE_DEFAULT: int = -1
SETTING_WPAN_PAN_ID: str = "pan-id"
SETTING_WPAN_SETTING_NAME: str = "wpan"
SETTING_WPAN_SHORT_ADDRESS: str = "short-address"
SRIOV_VF_ATTRIBUTE_MAC: str = "mac"
SRIOV_VF_ATTRIBUTE_MAX_TX_RATE: str = "max-tx-rate"
SRIOV_VF_ATTRIBUTE_MIN_TX_RATE: str = "min-tx-rate"
SRIOV_VF_ATTRIBUTE_SPOOF_CHECK: str = "spoof-check"
SRIOV_VF_ATTRIBUTE_TRUST: str = "trust"
TEAM_LINK_WATCHER_ARP_PING: str = "arp_ping"
TEAM_LINK_WATCHER_ETHTOOL: str = "ethtool"
TEAM_LINK_WATCHER_NSNA_PING: str = "nsna_ping"
UTILS_HWADDR_LEN_MAX: int = 20
VLAN_FLAGS_ALL: int = 15
VPN_CONNECTION_BANNER: str = "banner"
VPN_CONNECTION_VPN_STATE: str = "vpn-state"
VPN_DBUS_PLUGIN_INTERFACE: str = "org.freedesktop.NetworkManager.VPN.Plugin"
VPN_DBUS_PLUGIN_PATH: str = "/org/freedesktop/NetworkManager/VPN/Plugin"
VPN_EDITOR_PLUGIN_DESCRIPTION: str = "description"
VPN_EDITOR_PLUGIN_NAME: str = "name"
VPN_EDITOR_PLUGIN_SERVICE: str = "service"
VPN_PLUGIN_CAN_PERSIST: str = "can-persist"
VPN_PLUGIN_CONFIG_BANNER: str = "banner"
VPN_PLUGIN_CONFIG_EXT_GATEWAY: str = "gateway"
VPN_PLUGIN_CONFIG_HAS_IP4: str = "has-ip4"
VPN_PLUGIN_CONFIG_HAS_IP6: str = "has-ip6"
VPN_PLUGIN_CONFIG_MTU: str = "mtu"
VPN_PLUGIN_CONFIG_PROXY_PAC: str = "pac"
VPN_PLUGIN_CONFIG_TUNDEV: str = "tundev"
VPN_PLUGIN_INFO_FILENAME: str = "filename"
VPN_PLUGIN_INFO_KEYFILE: str = "keyfile"
VPN_PLUGIN_INFO_KF_GROUP_CONNECTION: str = "VPN Connection"
VPN_PLUGIN_INFO_KF_GROUP_GNOME: str = "GNOME"
VPN_PLUGIN_INFO_KF_GROUP_LIBNM: str = "libnm"
VPN_PLUGIN_INFO_NAME: str = "name"
VPN_PLUGIN_IP4_CONFIG_ADDRESS: str = "address"
VPN_PLUGIN_IP4_CONFIG_DNS: str = "dns"
VPN_PLUGIN_IP4_CONFIG_DOMAIN: str = "domain"
VPN_PLUGIN_IP4_CONFIG_DOMAINS: str = "domains"
VPN_PLUGIN_IP4_CONFIG_INT_GATEWAY: str = "internal-gateway"
VPN_PLUGIN_IP4_CONFIG_MSS: str = "mss"
VPN_PLUGIN_IP4_CONFIG_NBNS: str = "nbns"
VPN_PLUGIN_IP4_CONFIG_NEVER_DEFAULT: str = "never-default"
VPN_PLUGIN_IP4_CONFIG_PREFIX: str = "prefix"
VPN_PLUGIN_IP4_CONFIG_PRESERVE_ROUTES: str = "preserve-routes"
VPN_PLUGIN_IP4_CONFIG_PTP: str = "ptp"
VPN_PLUGIN_IP4_CONFIG_ROUTES: str = "routes"
VPN_PLUGIN_IP6_CONFIG_ADDRESS: str = "address"
VPN_PLUGIN_IP6_CONFIG_DNS: str = "dns"
VPN_PLUGIN_IP6_CONFIG_DOMAIN: str = "domain"
VPN_PLUGIN_IP6_CONFIG_DOMAINS: str = "domains"
VPN_PLUGIN_IP6_CONFIG_INT_GATEWAY: str = "internal-gateway"
VPN_PLUGIN_IP6_CONFIG_MSS: str = "mss"
VPN_PLUGIN_IP6_CONFIG_NEVER_DEFAULT: str = "never-default"
VPN_PLUGIN_IP6_CONFIG_PREFIX: str = "prefix"
VPN_PLUGIN_IP6_CONFIG_PRESERVE_ROUTES: str = "preserve-routes"
VPN_PLUGIN_IP6_CONFIG_PTP: str = "ptp"
VPN_PLUGIN_IP6_CONFIG_ROUTES: str = "routes"
VPN_PLUGIN_OLD_DBUS_SERVICE_NAME: str = "service-name"
VPN_PLUGIN_OLD_STATE: str = "state"
VPN_SERVICE_PLUGIN_DBUS_SERVICE_NAME: str = "service-name"
VPN_SERVICE_PLUGIN_DBUS_WATCH_PEER: str = "watch-peer"
VPN_SERVICE_PLUGIN_STATE: str = "state"
WIFI_P2P_PEER_FLAGS: str = "flags"
WIFI_P2P_PEER_HW_ADDRESS: str = "hw-address"
WIFI_P2P_PEER_LAST_SEEN: str = "last-seen"
WIFI_P2P_PEER_MANUFACTURER: str = "manufacturer"
WIFI_P2P_PEER_MODEL: str = "model"
WIFI_P2P_PEER_MODEL_NUMBER: str = "model-number"
WIFI_P2P_PEER_NAME: str = "name"
WIFI_P2P_PEER_SERIAL: str = "serial"
WIFI_P2P_PEER_STRENGTH: str = "strength"
WIFI_P2P_PEER_WFD_IES: str = "wfd-ies"
WIMAX_NSP_NAME: str = "name"
WIMAX_NSP_NETWORK_TYPE: str = "network-type"
WIMAX_NSP_SIGNAL_QUALITY: str = "signal-quality"
WIREGUARD_PEER_ATTR_ALLOWED_IPS: str = "allowed-ips"
WIREGUARD_PEER_ATTR_ENDPOINT: str = "endpoint"
WIREGUARD_PEER_ATTR_PERSISTENT_KEEPALIVE: str = "persistent-keepalive"
WIREGUARD_PEER_ATTR_PRESHARED_KEY: str = "preshared-key"
WIREGUARD_PEER_ATTR_PRESHARED_KEY_FLAGS: str = "preshared-key-flags"
WIREGUARD_PEER_ATTR_PUBLIC_KEY: str = "public-key"
WIREGUARD_PUBLIC_KEY_LEN: int = 32
WIREGUARD_SYMMETRIC_KEY_LEN: int = 32
_lock = ...  # FIXME Constant
_namespace: str = "NM"
_version: str = "1.0"

class _80211ApFlags: ...
class _80211ApSecurityFlags: ...
class _80211Mode: ...

def agent_manager_error_quark() -> int: ...
def bridge_vlan_from_str(str: str) -> BridgeVlan: ...
def client_error_quark() -> int: ...
def conn_wireguard_import(filename: str) -> Connection: ...
def connection_error_quark() -> int: ...
def crypto_error_quark() -> int: ...
def device_error_quark() -> int: ...
def ethtool_optname_is_channels(optname: str | None = None) -> bool: ...
def ethtool_optname_is_coalesce(optname: str | None = None) -> bool: ...
def ethtool_optname_is_eee(optname: str | None = None) -> bool: ...
def ethtool_optname_is_feature(optname: str | None = None) -> bool: ...
def ethtool_optname_is_pause(optname: str | None = None) -> bool: ...
def ethtool_optname_is_ring(optname: str | None = None) -> bool: ...
def ip_route_attribute_validate(
    name: str, value: GLib.Variant, family: int
) -> tuple[bool, bool]: ...
def ip_route_get_variant_attribute_spec() -> VariantAttributeSpec: ...
def ip_routing_rule_from_string(
    str: str,
    to_string_flags: IPRoutingRuleAsStringFlags,
    extra_args: dict[None, None] | None = None,
) -> IPRoutingRule: ...
def keyfile_read(
    keyfile: GLib.KeyFile,
    base_dir: str,
    handler_flags: KeyfileHandlerFlags,
    handler: Callable[..., bool] | None = None,
    *user_data: Any,
) -> Connection: ...
def keyfile_write(
    connection: Connection,
    handler_flags: KeyfileHandlerFlags,
    handler: Callable[..., bool] | None = None,
    *user_data: Any,
) -> GLib.KeyFile: ...
def manager_error_quark() -> int: ...
def range_from_str(str: str) -> Range: ...
def secret_agent_error_quark() -> int: ...
def settings_error_quark() -> int: ...
def sriov_vf_attribute_validate(
    name: str, value: GLib.Variant
) -> tuple[bool, bool]: ...
def utils_ap_mode_security_valid(
    type: UtilsSecurityType, wifi_caps: DeviceWifiCapabilities
) -> bool: ...
def utils_base64secret_decode(
    base64_key: str, required_key_len: int
) -> tuple[bool, int]: ...
def utils_bin2hexstr(src: Sequence[int], final_len: int) -> str: ...
def utils_bond_mode_int_to_string(mode: int) -> str: ...
def utils_bond_mode_string_to_int(mode: str) -> int: ...
def utils_check_virtual_device_compatibility(
    virtual_type: type, other_type: type
) -> bool: ...
def utils_ensure_gtypes() -> None: ...
def utils_enum_from_str(type: type, str: str) -> tuple[bool, int, str]: ...
def utils_enum_get_values(type: type, from_: int, to: int) -> list[str]: ...
def utils_enum_to_str(type: type, value: int) -> str: ...
def utils_escape_ssid(ssid: Sequence[int]) -> str: ...
def utils_file_is_certificate(filename: str) -> bool: ...
def utils_file_is_pkcs12(filename: str) -> bool: ...
def utils_file_is_private_key(filename: str) -> tuple[bool, bool]: ...
def utils_file_search_in_paths(
    progname: str,
    try_first: str | None,
    paths: str | None,
    file_test_flags: GLib.FileTest,
    predicate: Callable[..., bool],
    *user_data: Any,
) -> str: ...
def utils_format_variant_attributes(
    attributes: dict[str, GLib.Variant], attr_separator: int, key_value_separator: int
) -> str: ...
def utils_get_timestamp_msec() -> int: ...
def utils_hexstr2bin(hex: str) -> GLib.Bytes: ...
def utils_hwaddr_atoba(asc: str, length: int) -> bytes: ...
def utils_hwaddr_aton(asc: str, buffer: Sequence[int]) -> int: ...
def utils_hwaddr_canonical(asc: str, length: int) -> str: ...
def utils_hwaddr_len(type: int) -> int: ...
def utils_hwaddr_matches(
    hwaddr1: None, hwaddr1_len: int, hwaddr2: None, hwaddr2_len: int
) -> bool: ...
def utils_hwaddr_ntoa(addr: Sequence[int]) -> str: ...
def utils_hwaddr_valid(asc: str, length: int) -> bool: ...
def utils_iface_valid_name(name: str | None = None) -> bool: ...
def utils_ip4_addresses_from_variant(
    value: GLib.Variant,
) -> tuple[list[IPAddress], str]: ...
def utils_ip4_addresses_to_variant(
    addresses: Sequence[IPAddress], gateway: str | None = None
) -> GLib.Variant: ...
def utils_ip4_dns_from_variant(value: GLib.Variant) -> str: ...
def utils_ip4_dns_to_variant(dns: str) -> GLib.Variant: ...
def utils_ip4_get_default_prefix(ip: int) -> int: ...
def utils_ip4_netmask_to_prefix(netmask: int) -> int: ...
def utils_ip4_prefix_to_netmask(prefix: int) -> int: ...
def utils_ip4_routes_from_variant(value: GLib.Variant) -> list[IPRoute]: ...
def utils_ip4_routes_to_variant(routes: Sequence[IPRoute]) -> GLib.Variant: ...
def utils_ip6_addresses_from_variant(
    value: GLib.Variant,
) -> tuple[list[IPAddress], str]: ...
def utils_ip6_addresses_to_variant(
    addresses: Sequence[IPAddress], gateway: str | None = None
) -> GLib.Variant: ...
def utils_ip6_dns_from_variant(value: GLib.Variant) -> str: ...
def utils_ip6_dns_to_variant(dns: str) -> GLib.Variant: ...
def utils_ip6_routes_from_variant(value: GLib.Variant) -> list[IPRoute]: ...
def utils_ip6_routes_to_variant(routes: Sequence[IPRoute]) -> GLib.Variant: ...
def utils_ip_addresses_from_variant(
    value: GLib.Variant, family: int
) -> list[IPAddress]: ...
def utils_ip_addresses_to_variant(addresses: Sequence[IPAddress]) -> GLib.Variant: ...
def utils_ip_routes_from_variant(value: GLib.Variant, family: int) -> list[IPRoute]: ...
def utils_ip_routes_to_variant(routes: Sequence[IPRoute]) -> GLib.Variant: ...
def utils_ipaddr_valid(family: int, ip: str) -> bool: ...
def utils_is_empty_ssid(ssid: Sequence[int]) -> bool: ...
def utils_is_json_object(str: str) -> bool: ...
def utils_is_uuid(str: str | None = None) -> bool: ...
def utils_is_valid_iface_name(name: str | None = None) -> bool: ...
def utils_parse_variant_attributes(
    string: str,
    attr_separator: int,
    key_value_separator: int,
    ignore_unknown: bool,
    spec: VariantAttributeSpec,
) -> dict[str, GLib.Variant]: ...
def utils_print(output_mode: int, msg: str) -> None: ...
def utils_same_ssid(
    ssid1: Sequence[int], ssid2: Sequence[int], ignore_trailing_null: bool
) -> bool: ...
def utils_security_valid(
    type: UtilsSecurityType,
    wifi_caps: DeviceWifiCapabilities,
    have_ap: bool,
    adhoc: bool,
    ap_flags: _80211ApFlags,
    ap_wpa: _80211ApSecurityFlags,
    ap_rsn: _80211ApSecurityFlags,
) -> bool: ...
def utils_sriov_vf_from_str(str: str) -> SriovVF: ...
def utils_sriov_vf_to_str(vf: SriovVF, omit_index: bool) -> str: ...
def utils_ssid_to_utf8(ssid: Sequence[int]) -> str: ...
def utils_tc_action_from_str(str: str) -> TCAction: ...
def utils_tc_action_to_str(action: TCAction) -> str: ...
def utils_tc_qdisc_from_str(str: str) -> TCQdisc: ...
def utils_tc_qdisc_to_str(qdisc: TCQdisc) -> str: ...
def utils_tc_tfilter_from_str(str: str) -> TCTfilter: ...
def utils_tc_tfilter_to_str(tfilter: TCTfilter) -> str: ...
def utils_uuid_generate() -> str: ...
def utils_version() -> int: ...
def utils_wep_key_valid(key: str, wep_type: WepKeyType) -> bool: ...
def utils_wifi_2ghz_freqs() -> int: ...
def utils_wifi_5ghz_freqs() -> int: ...
def utils_wifi_channel_to_freq(channel: int, band: str) -> int: ...
def utils_wifi_find_next_channel(channel: int, direction: int, band: str) -> int: ...
def utils_wifi_freq_to_channel(freq: int) -> int: ...
def utils_wifi_is_channel_valid(channel: int, band: str) -> bool: ...
def utils_wifi_strength_bars(strength: int) -> str: ...
def utils_wpa_psk_valid(psk: str) -> bool: ...
def vpn_editor_plugin_load(plugin_name: str, check_service: str) -> VpnEditorPlugin: ...
def vpn_editor_plugin_load_from_file(
    plugin_name: str,
    check_service: str,
    check_owner: int,
    check_file: Callable[..., bool],
    *user_data: Any,
) -> VpnEditorPlugin: ...
def vpn_plugin_error_quark() -> int: ...

class AccessPoint(Object):
    """
    :Constructors:

    ::

        AccessPoint(**properties)

    Object NMAccessPoint

    Properties from NMAccessPoint:
      flags -> NM80211ApFlags:

      wpa-flags -> NM80211ApSecurityFlags:

      rsn-flags -> NM80211ApSecurityFlags:

      ssid -> GBytes:

      frequency -> guint:

      hw-address -> gchararray:

      mode -> NM80211Mode:

      max-bitrate -> guint:

      bandwidth -> guint:

      strength -> guchar:

      bssid -> gchararray:

      last-seen -> gint:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        bandwidth: int
        bssid: str
        flags: _80211ApFlags
        frequency: int
        hw_address: str
        last_seen: int
        max_bitrate: int
        mode: _80211Mode
        rsn_flags: _80211ApSecurityFlags
        ssid: GLib.Bytes
        strength: int
        wpa_flags: _80211ApSecurityFlags
        client: Client | None
        path: str

    props: Props = ...
    def connection_valid(self, connection: Connection) -> bool: ...
    def filter_connections(
        self, connections: Sequence[Connection]
    ) -> list[Connection]: ...
    def get_bandwidth(self) -> int: ...
    def get_bssid(self) -> str: ...
    def get_flags(self) -> _80211ApFlags: ...
    def get_frequency(self) -> int: ...
    def get_last_seen(self) -> int: ...
    def get_max_bitrate(self) -> int: ...
    def get_mode(self) -> _80211Mode: ...
    def get_rsn_flags(self) -> _80211ApSecurityFlags: ...
    def get_ssid(self) -> GLib.Bytes: ...
    def get_strength(self) -> int: ...
    def get_wpa_flags(self) -> _80211ApSecurityFlags: ...

class AccessPointClass(GObject.GPointer): ...

class ActiveConnection(Object):
    """
    :Constructors:

    ::

        ActiveConnection(**properties)

    Object NMActiveConnection

    Signals from NMActiveConnection:
      state-changed (guint, guint)

    Properties from NMActiveConnection:
      connection -> NMRemoteConnection:

      id -> gchararray:

      uuid -> gchararray:

      type -> gchararray:

      specific-object-path -> gchararray:

      devices -> GPtrArray:

      state -> NMActiveConnectionState:

      state-flags -> guint:

      default -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      default6 -> gboolean:

      ip6-config -> NMIPConfig:

      dhcp6-config -> NMDhcpConfig:

      vpn -> gboolean:

      master -> NMDevice:

      controller -> NMDevice:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        connection: RemoteConnection
        controller: Device | None
        default: bool
        default6: bool
        devices: list[Device]
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        id: str
        ip4_config: IPConfig
        ip6_config: IPConfig
        master: Device | None
        specific_object_path: str
        state: ActiveConnectionState
        state_flags: int
        type: str
        uuid: str
        vpn: bool
        client: Client | None
        path: str

    props: Props = ...
    def get_connection(self) -> RemoteConnection: ...
    def get_connection_type(self) -> str: ...
    def get_controller(self) -> None: ...
    def get_default(self) -> bool: ...
    def get_default6(self) -> bool: ...
    def get_devices(self) -> list[Device]: ...
    def get_dhcp4_config(self) -> DhcpConfig: ...
    def get_dhcp6_config(self) -> DhcpConfig: ...
    def get_id(self) -> str: ...
    def get_ip4_config(self) -> IPConfig: ...
    def get_ip6_config(self) -> IPConfig: ...
    def get_master(self) -> None: ...
    def get_specific_object_path(self) -> str: ...
    def get_state(self) -> ActiveConnectionState: ...
    def get_state_flags(self) -> ActivationStateFlags: ...
    def get_state_reason(self) -> ActiveConnectionStateReason: ...
    def get_uuid(self) -> str: ...
    def get_vpn(self) -> bool: ...

class ActiveConnectionClass(GObject.GPointer): ...

class BridgeVlan(GObject.GBoxed):
    """
    :Constructors:

    ::

        new(vid_start:int, vid_end:int) -> NM.BridgeVlan
    """
    def cmp(self, b: BridgeVlan) -> int: ...
    @staticmethod
    def from_str(str: str) -> BridgeVlan: ...
    def get_vid_range(self) -> tuple[bool, int, int]: ...
    def is_pvid(self) -> bool: ...
    def is_sealed(self) -> bool: ...
    def is_untagged(self) -> bool: ...
    @classmethod
    def new(cls, vid_start: int, vid_end: int) -> BridgeVlan: ...
    def new_clone(self) -> BridgeVlan: ...
    def ref(self) -> BridgeVlan: ...
    def seal(self) -> None: ...
    def set_pvid(self, value: bool) -> None: ...
    def set_untagged(self, value: bool) -> None: ...
    def to_str(self) -> str: ...
    def unref(self) -> None: ...

class Checkpoint(Object):
    """
    :Constructors:

    ::

        Checkpoint(**properties)

    Object NMCheckpoint

    Properties from NMCheckpoint:
      devices -> GPtrArray:

      created -> gint64:

      rollback-timeout -> guint:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        created: int
        devices: list[Device]
        rollback_timeout: int
        client: Client | None
        path: str

    props: Props = ...
    def get_created(self) -> int: ...
    def get_devices(self) -> list[Device]: ...
    def get_rollback_timeout(self) -> int: ...

class CheckpointClass(GObject.GPointer): ...

class Client(GObject.Object, Gio.AsyncInitable, Gio.Initable):  # type: ignore
    """
    :Constructors:

    ::

        Client(**properties)
        new(cancellable:Gio.Cancellable=None) -> NM.Client
        new_finish(result:Gio.AsyncResult) -> NM.Client

    Object NMClient

    Signals from NMClient:
      device-added (GObject)
      device-removed (GObject)
      any-device-added (GObject)
      any-device-removed (GObject)
      permission-changed (guint, guint)
      connection-added (NMRemoteConnection)
      connection-removed (NMRemoteConnection)
      active-connection-added (NMActiveConnection)
      active-connection-removed (NMActiveConnection)

    Properties from NMClient:
      dbus-connection -> GDBusConnection:

      dbus-name-owner -> gchararray:

      version -> gchararray:

      instance-flags -> guint:

      state -> NMState:

      startup -> gboolean:

      nm-running -> gboolean:

      networking-enabled -> gboolean:

      wireless-enabled -> gboolean:

      wireless-hardware-enabled -> gboolean:

      wwan-enabled -> gboolean:

      wwan-hardware-enabled -> gboolean:

      wimax-enabled -> gboolean:

      wimax-hardware-enabled -> gboolean:

      radio-flags -> guint:

      active-connections -> GPtrArray:

      connectivity -> NMConnectivityState:

      connectivity-check-uri -> gchararray:

      connectivity-check-available -> gboolean:

      connectivity-check-enabled -> gboolean:

      primary-connection -> NMActiveConnection:

      activating-connection -> NMActiveConnection:

      devices -> GPtrArray:

      all-devices -> GPtrArray:

      connections -> GPtrArray:

      hostname -> gchararray:

      can-modify -> gboolean:

      metered -> guint:

      dns-mode -> gchararray:

      dns-rc-manager -> gchararray:

      dns-configuration -> GPtrArray:

      checkpoints -> GPtrArray:

      version-info -> GArray:

      capabilities -> GArray:

      permissions-state -> NMTernary:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        activating_connection: ActiveConnection
        active_connections: list[ActiveConnection]
        all_devices: list[Device]
        can_modify: bool
        capabilities: list[int]
        checkpoints: list[Checkpoint]
        connections: list[RemoteConnection]
        connectivity: ConnectivityState
        connectivity_check_available: bool
        connectivity_check_enabled: bool
        connectivity_check_uri: str
        dbus_connection: Gio.DBusConnection
        dbus_name_owner: str
        devices: list[Device]
        dns_configuration: list[DnsEntry]
        dns_mode: str
        dns_rc_manager: str
        hostname: str
        instance_flags: int
        metered: int
        networking_enabled: bool
        nm_running: bool
        permissions_state: Ternary
        primary_connection: ActiveConnection
        radio_flags: int
        startup: bool
        state: State
        version: str
        version_info: list[int]
        wimax_enabled: bool
        wimax_hardware_enabled: bool
        wireless_enabled: bool
        wireless_hardware_enabled: bool
        wwan_enabled: bool
        wwan_hardware_enabled: bool

    props: Props = ...
    def __init__(
        self,
        connectivity_check_enabled: bool = ...,
        dbus_connection: Gio.DBusConnection = ...,
        instance_flags: int = ...,
        networking_enabled: bool = ...,
        wimax_enabled: bool = ...,
        wireless_enabled: bool = ...,
        wwan_enabled: bool = ...,
    ): ...
    def activate_connection_async(
        self,
        connection: Connection | None = None,
        device: Device | None = None,
        specific_object: str | None = None,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def activate_connection_finish(
        self, result: Gio.AsyncResult
    ) -> ActiveConnection: ...
    def add_and_activate_connection2(
        self,
        partial: Connection | None,
        device: Device | None,
        specific_object: str | None,
        options: GLib.Variant,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def add_and_activate_connection2_finish(
        self, result: Gio.AsyncResult
    ) -> tuple[ActiveConnection, GLib.Variant]: ...
    def add_and_activate_connection_async(
        self,
        partial: Connection | None = None,
        device: Device | None = None,
        specific_object: str | None = None,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def add_and_activate_connection_finish(
        self, result: Gio.AsyncResult
    ) -> ActiveConnection: ...
    def add_connection2(
        self,
        settings: GLib.Variant,
        flags: SettingsAddConnection2Flags,
        args: GLib.Variant | None,
        ignore_out_result: bool,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def add_connection2_finish(
        self, result: Gio.AsyncResult
    ) -> tuple[RemoteConnection, GLib.Variant]: ...
    def add_connection_async(
        self,
        connection: Connection,
        save_to_disk: bool,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def add_connection_finish(self, result: Gio.AsyncResult) -> RemoteConnection: ...
    def check_connectivity(
        self, cancellable: Gio.Cancellable | None = None
    ) -> ConnectivityState: ...
    def check_connectivity_async(
        self,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def check_connectivity_finish(
        self, result: Gio.AsyncResult
    ) -> ConnectivityState: ...
    def checkpoint_adjust_rollback_timeout(
        self,
        checkpoint_path: str,
        add_timeout: int,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def checkpoint_adjust_rollback_timeout_finish(
        self, result: Gio.AsyncResult
    ) -> bool: ...
    def checkpoint_create(
        self,
        devices: Sequence[Device],
        rollback_timeout: int,
        flags: CheckpointCreateFlags,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def checkpoint_create_finish(self, result: Gio.AsyncResult) -> Checkpoint: ...
    def checkpoint_destroy(
        self,
        checkpoint_path: str,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def checkpoint_destroy_finish(self, result: Gio.AsyncResult) -> bool: ...
    def checkpoint_rollback(
        self,
        checkpoint_path: str,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def checkpoint_rollback_finish(self, result: Gio.AsyncResult) -> dict[str, int]: ...
    def connectivity_check_get_available(self) -> bool: ...
    def connectivity_check_get_enabled(self) -> bool: ...
    def connectivity_check_get_uri(self) -> str: ...
    def connectivity_check_set_enabled(self, enabled: bool) -> None: ...
    def dbus_call(
        self,
        object_path: str,
        interface_name: str,
        method_name: str,
        parameters: GLib.Variant | None,
        reply_type: GLib.VariantType | None,
        timeout_msec: int,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def dbus_call_finish(self, result: Gio.AsyncResult) -> GLib.Variant: ...
    def dbus_set_property(
        self,
        object_path: str,
        interface_name: str,
        property_name: str,
        value: GLib.Variant,
        timeout_msec: int,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def dbus_set_property_finish(self, result: Gio.AsyncResult) -> bool: ...
    def deactivate_connection(
        self, active: ActiveConnection, cancellable: Gio.Cancellable | None = None
    ) -> bool: ...
    def deactivate_connection_async(
        self,
        active: ActiveConnection,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def deactivate_connection_finish(self, result: Gio.AsyncResult) -> bool: ...
    def get_activating_connection(self) -> ActiveConnection: ...
    def get_active_connections(self) -> list[ActiveConnection]: ...
    def get_all_devices(self) -> list[Device]: ...
    def get_capabilities(self) -> list[int]: ...
    def get_checkpoints(self) -> list[Checkpoint]: ...
    def get_connection_by_id(self, id: str) -> RemoteConnection: ...
    def get_connection_by_path(self, path: str) -> RemoteConnection: ...
    def get_connection_by_uuid(self, uuid: str) -> RemoteConnection: ...
    def get_connections(self) -> list[RemoteConnection]: ...
    def get_connectivity(self) -> ConnectivityState: ...
    def get_context_busy_watcher(self) -> GObject.Object: ...
    def get_dbus_connection(self) -> Gio.DBusConnection: ...
    def get_dbus_name_owner(self) -> str: ...
    def get_device_by_iface(self, iface: str) -> Device: ...
    def get_device_by_path(self, object_path: str) -> Device: ...
    def get_devices(self) -> list[Device]: ...
    def get_dns_configuration(self) -> list[DnsEntry]: ...
    def get_dns_mode(self) -> str: ...
    def get_dns_rc_manager(self) -> str: ...
    def get_instance_flags(self) -> ClientInstanceFlags: ...
    def get_logging(self) -> tuple[bool, str, str]: ...
    def get_main_context(self) -> GLib.MainContext: ...
    def get_metered(self) -> Metered: ...
    def get_nm_running(self) -> bool: ...
    def get_object_by_path(self, dbus_path: str) -> Object: ...
    def get_permission_result(
        self, permission: ClientPermission
    ) -> ClientPermissionResult: ...
    def get_permissions_state(self) -> Ternary: ...
    def get_primary_connection(self) -> ActiveConnection: ...
    def get_radio_flags(self) -> RadioFlags: ...
    def get_startup(self) -> bool: ...
    def get_state(self) -> State: ...
    def get_version(self) -> str: ...
    def get_version_info(self) -> list[int]: ...
    def load_connections(
        self, filenames: Sequence[str], cancellable: Gio.Cancellable | None = None
    ) -> tuple[bool, str]: ...
    def load_connections_async(
        self,
        filenames: Sequence[str],
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def load_connections_finish(
        self, result: Gio.AsyncResult
    ) -> tuple[bool, list[str]]: ...
    def networking_get_enabled(self) -> bool: ...
    def networking_set_enabled(self, enabled: bool) -> bool: ...
    @classmethod
    def new(cls, cancellable: Gio.Cancellable | None = None) -> Client: ...
    @staticmethod
    def new_async(
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    @classmethod
    def new_finish(cls, result: Gio.AsyncResult) -> Client: ...
    def reload(
        self,
        flags: ManagerReloadFlags,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def reload_connections(
        self, cancellable: Gio.Cancellable | None = None
    ) -> bool: ...
    def reload_connections_async(
        self,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def reload_connections_finish(self, result: Gio.AsyncResult) -> bool: ...
    def reload_finish(self, result: Gio.AsyncResult) -> bool: ...
    def save_hostname(
        self, hostname: str | None = None, cancellable: Gio.Cancellable | None = None
    ) -> bool: ...
    def save_hostname_async(
        self,
        hostname: str | None = None,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def save_hostname_finish(self, result: Gio.AsyncResult) -> bool: ...
    def set_logging(
        self, level: str | None = None, domains: str | None = None
    ) -> bool: ...
    def wait_shutdown(
        self,
        integrate_maincontext: bool,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    @staticmethod
    def wait_shutdown_finish(result: Gio.AsyncResult) -> bool: ...
    def wimax_get_enabled(self) -> bool: ...
    def wimax_hardware_get_enabled(self) -> bool: ...
    def wimax_set_enabled(self, enabled: bool) -> None: ...
    def wireless_get_enabled(self) -> bool: ...
    def wireless_hardware_get_enabled(self) -> bool: ...
    def wireless_set_enabled(self, enabled: bool) -> None: ...
    def wwan_get_enabled(self) -> bool: ...
    def wwan_hardware_get_enabled(self) -> bool: ...
    def wwan_set_enabled(self, enabled: bool) -> None: ...

class ClientClass(GObject.GPointer): ...

class Connection(GObject.GInterface):
    """
    Interface NMConnection

    Signals from GObject:
      notify (GParam)
    """
    def add_setting(self, setting: Setting) -> None: ...
    def clear_secrets(self) -> None: ...
    def clear_secrets_with_flags(
        self, func: Callable[..., bool] | None = None, *user_data: Any
    ) -> None: ...
    def clear_settings(self) -> None: ...
    def compare(self, b: Connection, flags: SettingCompareFlags) -> bool: ...
    def dump(self) -> None: ...
    def for_each_setting_value(
        self, func: Callable[..., None], *user_data: Any
    ) -> None: ...
    def get_connection_type(self) -> str: ...
    def get_id(self) -> str: ...
    def get_interface_name(self) -> str: ...
    def get_path(self) -> str: ...
    def get_setting(self, setting_type: type) -> Setting: ...
    def get_setting_802_1x(self) -> Setting8021x: ...
    def get_setting_adsl(self) -> SettingAdsl: ...
    def get_setting_bluetooth(self) -> SettingBluetooth: ...
    def get_setting_bond(self) -> SettingBond: ...
    def get_setting_bridge(self) -> SettingBridge: ...
    def get_setting_bridge_port(self) -> SettingBridgePort: ...
    def get_setting_by_name(self, name: str) -> Setting: ...
    def get_setting_cdma(self) -> SettingCdma: ...
    def get_setting_connection(self) -> SettingConnection: ...
    def get_setting_dcb(self) -> SettingDcb: ...
    def get_setting_dummy(self) -> SettingDummy: ...
    def get_setting_generic(self) -> SettingGeneric: ...
    def get_setting_gsm(self) -> SettingGsm: ...
    def get_setting_infiniband(self) -> SettingInfiniband: ...
    def get_setting_ip4_config(self) -> SettingIP4Config: ...
    def get_setting_ip6_config(self) -> SettingIP6Config: ...
    def get_setting_ip_tunnel(self) -> SettingIPTunnel: ...
    def get_setting_macsec(self) -> SettingMacsec: ...
    def get_setting_macvlan(self) -> SettingMacvlan: ...
    def get_setting_olpc_mesh(self) -> SettingOlpcMesh: ...
    def get_setting_ovs_bridge(self) -> SettingOvsBridge: ...
    def get_setting_ovs_interface(self) -> SettingOvsInterface: ...
    def get_setting_ovs_patch(self) -> SettingOvsPatch: ...
    def get_setting_ovs_port(self) -> SettingOvsPort: ...
    def get_setting_ppp(self) -> SettingPpp: ...
    def get_setting_pppoe(self) -> SettingPppoe: ...
    def get_setting_proxy(self) -> SettingProxy: ...
    def get_setting_serial(self) -> SettingSerial: ...
    def get_setting_tc_config(self) -> SettingTCConfig: ...
    def get_setting_team(self) -> SettingTeam: ...
    def get_setting_team_port(self) -> SettingTeamPort: ...
    def get_setting_tun(self) -> SettingTun: ...
    def get_setting_vlan(self) -> SettingVlan: ...
    def get_setting_vpn(self) -> SettingVpn: ...
    def get_setting_vxlan(self) -> SettingVxlan: ...
    def get_setting_wimax(self) -> SettingWimax: ...
    def get_setting_wired(self) -> SettingWired: ...
    def get_setting_wireless(self) -> SettingWireless: ...
    def get_setting_wireless_security(self) -> SettingWirelessSecurity: ...
    def get_settings(self) -> list[Setting] | None: ...
    def get_uuid(self) -> str: ...
    def get_virtual_device_description(self) -> str: ...
    def is_type(self, type: str) -> bool: ...
    def is_virtual(self) -> bool: ...
    def need_secrets(self) -> tuple[str | None, list[str]]: ...
    def normalize(
        self, parameters: dict[str, None] | None = None
    ) -> tuple[bool, bool]: ...
    def remove_setting(self, setting_type: type) -> None: ...
    def replace_settings(self, new_settings: GLib.Variant) -> bool: ...
    def replace_settings_from_connection(self, new_connection: Connection) -> None: ...
    def set_path(self, path: str) -> None: ...
    def to_dbus(self, flags: ConnectionSerializationFlags) -> GLib.Variant: ...
    def update_secrets(self, setting_name: str, secrets: GLib.Variant) -> bool: ...
    def verify(self) -> bool: ...
    def verify_secrets(self) -> bool: ...

class ConnectionInterface(GObject.GPointer):
    """
    :Constructors:

    ::

        ConnectionInterface()
    """

    parent: GObject.TypeInterface = ...
    secrets_updated: Callable[[Connection, str], None] = ...
    secrets_cleared: Callable[[Connection], None] = ...
    changed: Callable[[Connection], None] = ...

class Device(Object):
    """
    :Constructors:

    ::

        Device(**properties)

    Object NMDevice

    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def connection_compatible(self, connection: Connection) -> bool: ...
    def connection_valid(self, connection: Connection) -> bool: ...
    def delete(self, cancellable: Gio.Cancellable | None = None) -> bool: ...
    def delete_async(
        self,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def delete_finish(self, result: Gio.AsyncResult) -> bool: ...
    @staticmethod
    def disambiguate_names(devices: Sequence[Device]) -> list[str]: ...
    def disconnect(self, cancellable: Gio.Cancellable | None = None) -> bool: ...  # type: ignore
    def disconnect_async(
        self,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def disconnect_finish(self, result: Gio.AsyncResult) -> bool: ...
    def filter_connections(
        self, connections: Sequence[Connection]
    ) -> list[Connection]: ...
    def get_active_connection(self) -> ActiveConnection: ...
    def get_applied_connection(
        self, flags: int, cancellable: Gio.Cancellable | None = None
    ) -> tuple[Connection, int]: ...
    def get_applied_connection_async(
        self,
        flags: int,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def get_applied_connection_finish(
        self, result: Gio.AsyncResult
    ) -> tuple[Connection, int]: ...
    def get_autoconnect(self) -> bool: ...
    def get_available_connections(self) -> list[RemoteConnection]: ...
    def get_capabilities(self) -> DeviceCapabilities: ...
    def get_connectivity(self, addr_family: int) -> ConnectivityState: ...
    def get_description(self) -> str: ...
    def get_device_type(self) -> DeviceType: ...
    def get_dhcp4_config(self) -> DhcpConfig: ...
    def get_dhcp6_config(self) -> DhcpConfig: ...
    def get_driver(self) -> str: ...
    def get_driver_version(self) -> str: ...
    def get_firmware_missing(self) -> bool: ...
    def get_firmware_version(self) -> str: ...
    def get_hw_address(self) -> str: ...
    def get_iface(self) -> str: ...
    def get_interface_flags(self) -> DeviceInterfaceFlags: ...
    def get_ip4_config(self) -> IPConfig: ...
    def get_ip6_config(self) -> IPConfig: ...
    def get_ip_iface(self) -> str: ...
    def get_lldp_neighbors(self) -> list[LldpNeighbor]: ...
    def get_managed(self) -> bool: ...
    def get_metered(self) -> Metered: ...
    def get_mtu(self) -> int: ...
    def get_nm_plugin_missing(self) -> bool: ...
    def get_path(self) -> str: ...
    def get_physical_port_id(self) -> str: ...
    def get_ports(self) -> list[Device]: ...
    def get_product(self) -> str: ...
    def get_setting_type(self) -> type: ...
    def get_state(self) -> DeviceState: ...
    def get_state_reason(self) -> DeviceStateReason: ...
    def get_type_description(self) -> str: ...
    def get_udi(self) -> str: ...
    def get_vendor(self) -> str: ...
    def is_real(self) -> bool: ...
    def is_software(self) -> bool: ...
    def reapply(
        self,
        connection: Connection | None,
        version_id: int,
        flags: int,
        cancellable: Gio.Cancellable | None = None,
    ) -> bool: ...
    def reapply_async(
        self,
        connection: Connection | None,
        version_id: int,
        flags: int,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def reapply_finish(self, result: Gio.AsyncResult) -> bool: ...
    def set_autoconnect(self, autoconnect: bool) -> None: ...
    def set_managed(self, managed: bool) -> None: ...

class Device6Lowpan(Device):
    """
    :Constructors:

    ::

        Device6Lowpan(**properties)

    Object NMDevice6Lowpan

    Properties from NMDevice6Lowpan:
      parent -> NMDevice:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        parent: Device
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_parent(self) -> Device: ...

class Device6LowpanClass(GObject.GPointer): ...

class DeviceAdsl(Device):
    """
    :Constructors:

    ::

        DeviceAdsl(**properties)

    Object NMDeviceAdsl

    Properties from NMDeviceAdsl:
      carrier -> gboolean:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        carrier: bool
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_carrier(self) -> bool: ...

class DeviceAdslClass(GObject.GPointer): ...

class DeviceBond(Device):
    """
    :Constructors:

    ::

        DeviceBond(**properties)

    Object NMDeviceBond

    Properties from NMDeviceBond:
      carrier -> gboolean:

      slaves -> GPtrArray:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        carrier: bool
        slaves: list[Device]
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_carrier(self) -> bool: ...
    def get_slaves(self) -> list[Device]: ...

class DeviceBondClass(GObject.GPointer): ...

class DeviceBridge(Device):
    """
    :Constructors:

    ::

        DeviceBridge(**properties)

    Object NMDeviceBridge

    Properties from NMDeviceBridge:
      carrier -> gboolean:

      slaves -> GPtrArray:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        carrier: bool
        slaves: list[Device]
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_carrier(self) -> bool: ...
    def get_slaves(self) -> list[Device]: ...

class DeviceBridgeClass(GObject.GPointer): ...

class DeviceBt(Device):
    """
    :Constructors:

    ::

        DeviceBt(**properties)

    Object NMDeviceBt

    Properties from NMDeviceBt:
      name -> gchararray:

      bt-capabilities -> NMBluetoothCapabilities:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        bt_capabilities: BluetoothCapabilities
        name: str
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_capabilities(self) -> BluetoothCapabilities: ...  # type: ignore
    def get_name(self) -> str: ...

class DeviceBtClass(GObject.GPointer): ...
class DeviceClass(GObject.GPointer): ...

class DeviceDummy(Device):
    """
    :Constructors:

    ::

        DeviceDummy(**properties)

    Object NMDeviceDummy

    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...

class DeviceDummyClass(GObject.GPointer): ...

class DeviceEthernet(Device):
    """
    :Constructors:

    ::

        DeviceEthernet(**properties)

    Object NMDeviceEthernet

    Properties from NMDeviceEthernet:
      perm-hw-address -> gchararray:

      speed -> guint:

      carrier -> gboolean:

      s390-subchannels -> GStrv:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        carrier: bool
        perm_hw_address: str
        s390_subchannels: list[str]
        speed: int
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_carrier(self) -> bool: ...
    def get_permanent_hw_address(self) -> str: ...
    def get_s390_subchannels(self) -> list[str]: ...
    def get_speed(self) -> int: ...

class DeviceEthernetClass(GObject.GPointer): ...

class DeviceGeneric(Device):
    """
    :Constructors:

    ::

        DeviceGeneric(**properties)

    Object NMDeviceGeneric

    Properties from NMDeviceGeneric:
      type-description -> gchararray:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        type_description: str
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...

class DeviceGenericClass(GObject.GPointer): ...

class DeviceHsr(Device):
    """
    :Constructors:

    ::

        DeviceHsr(**properties)

    Object NMDeviceHsr

    Properties from NMDeviceHsr:
      port1 -> NMDevice:

      port2 -> NMDevice:

      supervision-address -> gchararray:

      multicast-spec -> guchar:

      prp -> gboolean:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        multicast_spec: int
        port1: Device
        port2: Device
        prp: bool
        supervision_address: str
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_multicast_spec(self) -> int: ...
    def get_port1(self) -> Device: ...
    def get_port2(self) -> Device: ...
    def get_prp(self) -> bool: ...
    def get_supervision_address(self) -> str: ...

class DeviceHsrClass(GObject.GPointer): ...

class DeviceIPTunnel(Device):
    """
    :Constructors:

    ::

        DeviceIPTunnel(**properties)

    Object NMDeviceIPTunnel

    Properties from NMDeviceIPTunnel:
      mode -> guint:

      parent -> NMDevice:

      local -> gchararray:

      remote -> gchararray:

      ttl -> guchar:

      tos -> guchar:

      path-mtu-discovery -> gboolean:

      input-key -> gchararray:

      output-key -> gchararray:

      encapsulation-limit -> guchar:

      flow-label -> guint:

      fwmark -> guint:

      flags -> guint:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        encapsulation_limit: int
        flags: int
        flow_label: int
        fwmark: int
        input_key: str
        local: str
        mode: int
        output_key: str
        parent: Device
        path_mtu_discovery: bool
        remote: str
        tos: int
        ttl: int
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_encapsulation_limit(self) -> int: ...
    def get_flags(self) -> IPTunnelFlags: ...
    def get_flow_label(self) -> int: ...
    def get_fwmark(self) -> int: ...
    def get_input_key(self) -> str: ...
    def get_local(self) -> str: ...
    def get_mode(self) -> IPTunnelMode: ...
    def get_output_key(self) -> str: ...
    def get_parent(self) -> Device: ...
    def get_path_mtu_discovery(self) -> bool: ...
    def get_remote(self) -> str: ...
    def get_tos(self) -> int: ...
    def get_ttl(self) -> int: ...

class DeviceIPTunnelClass(GObject.GPointer): ...

class DeviceInfiniband(Device):
    """
    :Constructors:

    ::

        DeviceInfiniband(**properties)

    Object NMDeviceInfiniband

    Properties from NMDeviceInfiniband:
      carrier -> gboolean:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        carrier: bool
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_carrier(self) -> bool: ...

class DeviceInfinibandClass(GObject.GPointer): ...

class DeviceLoopback(Device):
    """
    :Constructors:

    ::

        DeviceLoopback(**properties)

    Object NMDeviceLoopback

    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...

class DeviceLoopbackClass(GObject.GPointer): ...

class DeviceMacsec(Device):
    """
    :Constructors:

    ::

        DeviceMacsec(**properties)

    Object NMDeviceMacsec

    Properties from NMDeviceMacsec:
      parent -> NMDevice:

      sci -> guint64:

      cipher-suite -> guint64:

      icv-length -> guchar:

      window -> guint:

      encoding-sa -> guchar:

      encrypt -> gboolean:

      protect -> gboolean:

      include-sci -> gboolean:

      es -> gboolean:

      scb -> gboolean:

      replay-protect -> gboolean:

      validation -> gchararray:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        cipher_suite: int
        encoding_sa: int
        encrypt: bool
        es: bool
        icv_length: int
        include_sci: bool
        parent: Device
        protect: bool
        replay_protect: bool
        scb: bool
        sci: int
        validation: str
        window: int
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_cipher_suite(self) -> int: ...
    def get_encoding_sa(self) -> int: ...
    def get_encrypt(self) -> bool: ...
    def get_es(self) -> bool: ...
    def get_icv_length(self) -> int: ...
    def get_include_sci(self) -> bool: ...
    def get_parent(self) -> Device: ...
    def get_protect(self) -> bool: ...
    def get_replay_protect(self) -> bool: ...
    def get_scb(self) -> bool: ...
    def get_sci(self) -> int: ...
    def get_validation(self) -> str: ...
    def get_window(self) -> int: ...

class DeviceMacsecClass(GObject.GPointer): ...

class DeviceMacvlan(Device):
    """
    :Constructors:

    ::

        DeviceMacvlan(**properties)

    Object NMDeviceMacvlan

    Properties from NMDeviceMacvlan:
      parent -> NMDevice:

      mode -> gchararray:

      no-promisc -> gboolean:

      tap -> gboolean:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        mode: str
        no_promisc: bool
        parent: Device
        tap: bool
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_mode(self) -> str: ...
    def get_no_promisc(self) -> bool: ...
    def get_parent(self) -> Device: ...
    def get_tap(self) -> bool: ...

class DeviceMacvlanClass(GObject.GPointer): ...

class DeviceModem(Device):
    """
    :Constructors:

    ::

        DeviceModem(**properties)

    Object NMDeviceModem

    Properties from NMDeviceModem:
      modem-capabilities -> NMDeviceModemCapabilities:

      current-capabilities -> NMDeviceModemCapabilities:

      device-id -> gchararray:

      operator-code -> gchararray:

      apn -> gchararray:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        apn: str
        current_capabilities: DeviceModemCapabilities
        device_id: str
        modem_capabilities: DeviceModemCapabilities
        operator_code: str
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_apn(self) -> str: ...
    def get_current_capabilities(self) -> DeviceModemCapabilities: ...
    def get_device_id(self) -> str: ...
    def get_modem_capabilities(self) -> DeviceModemCapabilities: ...
    def get_operator_code(self) -> str: ...

class DeviceModemClass(GObject.GPointer): ...

class DeviceOlpcMesh(Device):
    """
    :Constructors:

    ::

        DeviceOlpcMesh(**properties)

    Object NMDeviceOlpcMesh

    Properties from NMDeviceOlpcMesh:
      companion -> NMDeviceWifi:

      active-channel -> guint:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        active_channel: int
        companion: DeviceWifi
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_active_channel(self) -> int: ...
    def get_companion(self) -> DeviceWifi: ...

class DeviceOlpcMeshClass(GObject.GPointer): ...

class DeviceOvsBridge(Device):
    """
    :Constructors:

    ::

        DeviceOvsBridge(**properties)

    Object NMDeviceOvsBridge

    Properties from NMDeviceOvsBridge:
      slaves -> GPtrArray:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        slaves: list[Device]
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_slaves(self) -> list[Device]: ...

class DeviceOvsBridgeClass(GObject.GPointer): ...

class DeviceOvsInterface(Device):
    """
    :Constructors:

    ::

        DeviceOvsInterface(**properties)

    Object NMDeviceOvsInterface

    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...

class DeviceOvsInterfaceClass(GObject.GPointer): ...

class DeviceOvsPort(Device):
    """
    :Constructors:

    ::

        DeviceOvsPort(**properties)

    Object NMDeviceOvsPort

    Properties from NMDeviceOvsPort:
      slaves -> GPtrArray:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        slaves: list[Device]
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_slaves(self) -> list[Device]: ...

class DeviceOvsPortClass(GObject.GPointer): ...

class DevicePpp(Device):
    """
    :Constructors:

    ::

        DevicePpp(**properties)

    Object NMDevicePpp

    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...

class DevicePppClass(GObject.GPointer): ...

class DeviceTeam(Device):
    """
    :Constructors:

    ::

        DeviceTeam(**properties)

    Object NMDeviceTeam

    Properties from NMDeviceTeam:
      carrier -> gboolean:

      slaves -> GPtrArray:

      config -> gchararray:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        carrier: bool
        config: str
        slaves: list[Device]
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_carrier(self) -> bool: ...
    def get_config(self) -> str: ...
    def get_slaves(self) -> list[Device]: ...

class DeviceTeamClass(GObject.GPointer): ...

class DeviceTun(Device):
    """
    :Constructors:

    ::

        DeviceTun(**properties)

    Object NMDeviceTun

    Properties from NMDeviceTun:
      mode -> gchararray:

      owner -> gint64:

      group -> gint64:

      no-pi -> gboolean:

      vnet-hdr -> gboolean:

      multi-queue -> gboolean:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        group: int
        mode: str
        multi_queue: bool
        no_pi: bool
        owner: int
        vnet_hdr: bool
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_group(self) -> int: ...
    def get_mode(self) -> str: ...
    def get_multi_queue(self) -> bool: ...
    def get_no_pi(self) -> bool: ...
    def get_owner(self) -> int: ...
    def get_vnet_hdr(self) -> bool: ...

class DeviceTunClass(GObject.GPointer): ...

class DeviceVeth(DeviceEthernet):
    """
    :Constructors:

    ::

        DeviceVeth(**properties)

    Object NMDeviceVeth

    Properties from NMDeviceVeth:
      peer -> NMDevice:


    Properties from NMDeviceEthernet:
      perm-hw-address -> gchararray:

      speed -> guint:

      carrier -> gboolean:

      s390-subchannels -> GStrv:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        peer: Device
        carrier: bool
        perm_hw_address: str
        s390_subchannels: list[str]
        speed: int
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_peer(self) -> Device: ...

class DeviceVethClass(GObject.GPointer): ...

class DeviceVlan(Device):
    """
    :Constructors:

    ::

        DeviceVlan(**properties)

    Object NMDeviceVlan

    Properties from NMDeviceVlan:
      carrier -> gboolean:

      parent -> NMDevice:

      vlan-id -> guint:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        carrier: bool
        parent: Device
        vlan_id: int
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_carrier(self) -> bool: ...
    def get_parent(self) -> Device: ...
    def get_vlan_id(self) -> int: ...

class DeviceVlanClass(GObject.GPointer): ...

class DeviceVrf(Device):
    """
    :Constructors:

    ::

        DeviceVrf(**properties)

    Object NMDeviceVrf

    Properties from NMDeviceVrf:
      table -> guint:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        table: int
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_table(self) -> int: ...

class DeviceVrfClass(GObject.GPointer): ...

class DeviceVxlan(Device):
    """
    :Constructors:

    ::

        DeviceVxlan(**properties)

    Object NMDeviceVxlan

    Properties from NMDeviceVxlan:
      carrier -> gboolean:

      parent -> NMDevice:

      id -> guint:

      group -> gchararray:

      local -> gchararray:

      tos -> guchar:

      ttl -> guchar:

      limit -> guint:

      learning -> gboolean:

      ageing -> guint:

      dst-port -> guint:

      src-port-min -> guint:

      src-port-max -> guint:

      proxy -> gboolean:

      rsc -> gboolean:

      l2miss -> gboolean:

      l3miss -> gboolean:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        ageing: int
        carrier: bool
        dst_port: int
        group: str
        id: int
        l2miss: bool
        l3miss: bool
        learning: bool
        limit: int
        local: str
        parent: Device
        proxy: bool
        rsc: bool
        src_port_max: int
        src_port_min: int
        tos: int
        ttl: int
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_ageing(self) -> int: ...
    def get_carrier(self) -> bool: ...
    def get_dst_port(self) -> int: ...
    def get_group(self) -> str: ...
    def get_id(self) -> int: ...
    def get_l2miss(self) -> bool: ...
    def get_l3miss(self) -> bool: ...
    def get_learning(self) -> bool: ...
    def get_limit(self) -> int: ...
    def get_local(self) -> str: ...
    def get_parent(self) -> Device: ...
    def get_proxy(self) -> bool: ...
    def get_rsc(self) -> bool: ...
    def get_src_port_max(self) -> int: ...
    def get_src_port_min(self) -> int: ...
    def get_tos(self) -> int: ...
    def get_ttl(self) -> int: ...

class DeviceVxlanClass(GObject.GPointer): ...

class DeviceWifi(Device):
    """
    :Constructors:

    ::

        DeviceWifi(**properties)

    Object NMDeviceWifi

    Signals from NMDeviceWifi:
      access-point-added (GObject)
      access-point-removed (GObject)

    Properties from NMDeviceWifi:
      perm-hw-address -> gchararray:

      mode -> NM80211Mode:

      bitrate -> guint:

      access-points -> GPtrArray:

      active-access-point -> NMAccessPoint:

      wireless-capabilities -> NMDeviceWifiCapabilities:

      last-scan -> gint64:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        access_points: list[AccessPoint]
        active_access_point: AccessPoint
        bitrate: int
        last_scan: int
        mode: _80211Mode
        perm_hw_address: str
        wireless_capabilities: DeviceWifiCapabilities
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_access_point_by_path(self, path: str) -> AccessPoint: ...
    def get_access_points(self) -> list[AccessPoint]: ...
    def get_active_access_point(self) -> AccessPoint: ...
    def get_bitrate(self) -> int: ...
    def get_capabilities(self) -> DeviceWifiCapabilities: ...  # type: ignore
    def get_last_scan(self) -> int: ...
    def get_mode(self) -> _80211Mode: ...
    def get_permanent_hw_address(self) -> str: ...
    def request_scan(self, cancellable: Gio.Cancellable | None = None) -> bool: ...
    def request_scan_async(
        self,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def request_scan_finish(self, result: Gio.AsyncResult) -> bool: ...
    def request_scan_options(
        self, options: GLib.Variant, cancellable: Gio.Cancellable | None = None
    ) -> bool: ...
    def request_scan_options_async(
        self,
        options: GLib.Variant,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...

class DeviceWifiClass(GObject.GPointer): ...

class DeviceWifiP2P(Device):
    """
    :Constructors:

    ::

        DeviceWifiP2P(**properties)

    Object NMDeviceWifiP2P

    Signals from NMDeviceWifiP2P:
      peer-added (GObject)
      peer-removed (GObject)

    Properties from NMDeviceWifiP2P:
      peers -> GPtrArray:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        peers: list[WifiP2PPeer]
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_peer_by_path(self, path: str) -> WifiP2PPeer: ...
    def get_peers(self) -> list[WifiP2PPeer]: ...
    def start_find(
        self,
        options: GLib.Variant | None = None,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def start_find_finish(self, result: Gio.AsyncResult) -> bool: ...
    def stop_find(
        self,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def stop_find_finish(self, result: Gio.AsyncResult) -> bool: ...

class DeviceWifiP2PClass(GObject.GPointer): ...

class DeviceWimax(Device):
    """
    :Constructors:

    ::

        DeviceWimax(**properties)

    Object NMDeviceWimax

    Signals from NMDeviceWimax:
      nsp-added (GObject)
      nsp-removed (GObject)

    Properties from NMDeviceWimax:
      hw-address -> gchararray:

      active-nsp -> NMWimaxNsp:

      center-frequency -> guint:

      rssi -> gint:

      cinr -> gint:

      tx-power -> gint:

      bsid -> gchararray:

      nsps -> GPtrArray:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        active_nsp: WimaxNsp
        bsid: str
        center_frequency: int
        cinr: int
        hw_address: str
        nsps: list[WimaxNsp]
        rssi: int
        tx_power: int
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_active_nsp(self) -> WimaxNsp: ...
    def get_bsid(self) -> str: ...
    def get_center_frequency(self) -> int: ...
    def get_cinr(self) -> int: ...
    def get_hw_address(self) -> str: ...
    def get_nsp_by_path(self, path: str) -> WimaxNsp: ...
    def get_nsps(self) -> list[WimaxNsp]: ...
    def get_rssi(self) -> int: ...
    def get_tx_power(self) -> int: ...

class DeviceWimaxClass(GObject.GPointer): ...

class DeviceWireGuard(Device):
    """
    :Constructors:

    ::

        DeviceWireGuard(**properties)

    Object NMDeviceWireGuard

    Properties from NMDeviceWireGuard:
      public-key -> GBytes:

      listen-port -> guint:

      fwmark -> guint:


    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        fwmark: int
        listen_port: int
        public_key: GLib.Bytes
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...
    def get_fwmark(self) -> int: ...
    def get_listen_port(self) -> int: ...
    def get_public_key(self) -> GLib.Bytes: ...

class DeviceWireGuardClass(GObject.GPointer): ...

class DeviceWpan(Device):
    """
    :Constructors:

    ::

        DeviceWpan(**properties)

    Object NMDeviceWpan

    Signals from NMDevice:
      state-changed (guint, guint, guint)

    Properties from NMDevice:
      interface -> gchararray:

      udi -> gchararray:

      path -> gchararray:

      driver -> gchararray:

      driver-version -> gchararray:

      firmware-version -> gchararray:

      capabilities -> NMDeviceCapabilities:

      real -> gboolean:

      managed -> gboolean:

      autoconnect -> gboolean:

      firmware-missing -> gboolean:

      nm-plugin-missing -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      ip6-config -> NMIPConfig:

      state -> NMDeviceState:

      state-reason -> guint:

      product -> gchararray:

      vendor -> gchararray:

      dhcp6-config -> NMDhcpConfig:

      ip-interface -> gchararray:

      device-type -> NMDeviceType:

      active-connection -> NMActiveConnection:

      available-connections -> GPtrArray:

      physical-port-id -> gchararray:

      mtu -> guint:

      metered -> guint:

      lldp-neighbors -> GPtrArray:

      ip4-connectivity -> NMConnectivityState:

      ip6-connectivity -> NMConnectivityState:

      interface-flags -> guint:

      hw-address -> gchararray:

      ports -> GPtrArray:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        active_connection: ActiveConnection
        autoconnect: bool
        available_connections: list[RemoteConnection]
        capabilities: DeviceCapabilities
        device_type: DeviceType
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        driver: str
        driver_version: str
        firmware_missing: bool
        firmware_version: str
        hw_address: str
        interface: str
        interface_flags: int
        ip_interface: str
        ip4_config: IPConfig
        ip4_connectivity: ConnectivityState
        ip6_config: IPConfig
        ip6_connectivity: ConnectivityState
        lldp_neighbors: list[None]
        managed: bool
        metered: int
        mtu: int
        nm_plugin_missing: bool
        path: str
        physical_port_id: str
        ports: list[None]
        product: str
        real: bool
        state: DeviceState
        state_reason: int
        udi: str
        vendor: str
        client: Client | None

    props: Props = ...
    def __init__(self, autoconnect: bool = ...): ...

class DeviceWpanClass(GObject.GPointer): ...

class DhcpConfig(Object):
    """
    :Constructors:

    ::

        DhcpConfig(**properties)

    Object NMDhcpConfig

    Properties from NMDhcpConfig:
      family -> gint:

      options -> GHashTable:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        family: int
        options: dict[str, str]
        client: Client | None
        path: str

    props: Props = ...
    def get_family(self) -> int: ...
    def get_one_option(self, option: str) -> str: ...
    def get_options(self) -> dict[str, str]: ...

class DhcpConfigClass(GObject.GPointer): ...

class DnsEntry(GObject.GBoxed):
    def get_domains(self) -> list[str]: ...
    def get_interface(self) -> str: ...
    def get_nameservers(self) -> list[str]: ...
    def get_priority(self) -> int: ...
    def get_vpn(self) -> bool: ...
    def unref(self) -> None: ...

class IPAddress(GObject.GBoxed):
    """
    :Constructors:

    ::

        new(family:int, addr:str, prefix:int) -> NM.IPAddress
        new_binary(family:int, addr=None, prefix:int) -> NM.IPAddress
    """
    def cmp_full(self, b: IPAddress, cmp_flags: IPAddressCmpFlags) -> int: ...
    def dup(self) -> IPAddress: ...
    def equal(self, other: IPAddress) -> bool: ...
    def get_address(self) -> str: ...
    def get_attribute(self, name: str) -> GLib.Variant: ...
    def get_attribute_names(self) -> list[str]: ...
    def get_family(self) -> int: ...
    def get_prefix(self) -> int: ...
    @classmethod
    def new(cls, family: int, addr: str, prefix: int) -> IPAddress: ...
    @classmethod
    def new_binary(cls, family: int, addr: None, prefix: int) -> IPAddress: ...
    def ref(self) -> None: ...
    def set_address(self, addr: str) -> None: ...
    def set_attribute(self, name: str, value: GLib.Variant | None = None) -> None: ...
    def set_prefix(self, prefix: int) -> None: ...
    def unref(self) -> None: ...

class IPConfig(Object):
    """
    :Constructors:

    ::

        IPConfig(**properties)

    Object NMIPConfig

    Properties from NMIPConfig:
      family -> gint:

      gateway -> gchararray:

      addresses -> GPtrArray:

      routes -> GPtrArray:

      nameservers -> GStrv:

      domains -> GStrv:

      searches -> GStrv:

      wins-servers -> GStrv:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        addresses: list[None]
        domains: list[str]
        family: int
        gateway: str
        nameservers: list[str]
        routes: list[IPRoute]
        searches: list[str]
        wins_servers: list[str]
        client: Client | None
        path: str

    props: Props = ...
    def get_addresses(self) -> list[IPAddress]: ...
    def get_domains(self) -> list[str]: ...
    def get_family(self) -> int: ...
    def get_gateway(self) -> str: ...
    def get_nameservers(self) -> list[str]: ...
    def get_routes(self) -> list[IPRoute]: ...
    def get_searches(self) -> list[str]: ...
    def get_wins_servers(self) -> list[str]: ...

class IPConfigClass(GObject.GPointer): ...

class IPRoute(GObject.GBoxed):
    """
    :Constructors:

    ::

        new(family:int, dest:str, prefix:int, next_hop:str=None, metric:int) -> NM.IPRoute
        new_binary(family:int, dest=None, prefix:int, next_hop=None, metric:int) -> NM.IPRoute
    """
    @staticmethod
    def attribute_validate(
        name: str, value: GLib.Variant, family: int
    ) -> tuple[bool, bool]: ...
    def dup(self) -> IPRoute: ...
    def equal(self, other: IPRoute) -> bool: ...
    def equal_full(self, other: IPRoute, cmp_flags: int) -> bool: ...
    def get_attribute(self, name: str) -> GLib.Variant: ...
    def get_attribute_names(self) -> list[str]: ...
    def get_dest(self) -> str: ...
    def get_family(self) -> int: ...
    def get_metric(self) -> int: ...
    def get_next_hop(self) -> str: ...
    def get_prefix(self) -> int: ...
    @staticmethod
    def get_variant_attribute_spec() -> VariantAttributeSpec: ...
    @classmethod
    def new(
        cls, family: int, dest: str, prefix: int, next_hop: str | None, metric: int
    ) -> IPRoute: ...
    @classmethod
    def new_binary(
        cls, family: int, dest: None, prefix: int, next_hop: None, metric: int
    ) -> IPRoute: ...
    def ref(self) -> None: ...
    def set_attribute(self, name: str, value: GLib.Variant | None = None) -> None: ...
    def set_dest(self, dest: str) -> None: ...
    def set_metric(self, metric: int) -> None: ...
    def set_next_hop(self, next_hop: str | None = None) -> None: ...
    def set_prefix(self, prefix: int) -> None: ...
    def unref(self) -> None: ...

class IPRoutingRule(GObject.GBoxed):
    """
    :Constructors:

    ::

        new(addr_family:int) -> NM.IPRoutingRule
    """
    def cmp(self, other: IPRoutingRule | None = None) -> int: ...
    @staticmethod
    def from_string(
        str: str,
        to_string_flags: IPRoutingRuleAsStringFlags,
        extra_args: dict[None, None] | None = None,
    ) -> IPRoutingRule: ...
    def get_action(self) -> int: ...
    def get_addr_family(self) -> int: ...
    def get_destination_port_end(self) -> int: ...
    def get_destination_port_start(self) -> int: ...
    def get_from(self) -> str: ...
    def get_from_len(self) -> int: ...
    def get_fwmark(self) -> int: ...
    def get_fwmask(self) -> int: ...
    def get_iifname(self) -> str: ...
    def get_invert(self) -> bool: ...
    def get_ipproto(self) -> int: ...
    def get_oifname(self) -> str: ...
    def get_priority(self) -> int: ...
    def get_source_port_end(self) -> int: ...
    def get_source_port_start(self) -> int: ...
    def get_suppress_prefixlength(self) -> int: ...
    def get_table(self) -> int: ...
    def get_to(self) -> str: ...
    def get_to_len(self) -> int: ...
    def get_tos(self) -> int: ...
    def get_uid_range(self) -> tuple[bool, int, int]: ...
    def is_sealed(self) -> bool: ...
    @classmethod
    def new(cls, addr_family: int) -> IPRoutingRule: ...
    def new_clone(self) -> IPRoutingRule: ...
    def ref(self) -> IPRoutingRule: ...
    def seal(self) -> None: ...
    def set_action(self, action: int) -> None: ...
    def set_destination_port(self, start: int, end: int) -> None: ...
    def set_from(self, from_: str | None, len: int) -> None: ...
    def set_fwmark(self, fwmark: int, fwmask: int) -> None: ...
    def set_iifname(self, iifname: str | None = None) -> None: ...
    def set_invert(self, invert: bool) -> None: ...
    def set_ipproto(self, ipproto: int) -> None: ...
    def set_oifname(self, oifname: str | None = None) -> None: ...
    def set_priority(self, priority: int) -> None: ...
    def set_source_port(self, start: int, end: int) -> None: ...
    def set_suppress_prefixlength(self, suppress_prefixlength: int) -> None: ...
    def set_table(self, table: int) -> None: ...
    def set_to(self, to: str | None, len: int) -> None: ...
    def set_tos(self, tos: int) -> None: ...
    def set_uid_range(self, uid_range_start: int, uid_range_end: int) -> None: ...
    def to_string(
        self,
        to_string_flags: IPRoutingRuleAsStringFlags,
        extra_args: dict[None, None] | None = None,
    ) -> str: ...
    def unref(self) -> None: ...
    def validate(self) -> bool: ...

class KeyfileHandlerData(GObject.GPointer):
    def fail_with_error(self, src: GLib.Error) -> None: ...
    def get_context(self) -> tuple[str, str, Setting, str]: ...
    def warn_get(self) -> tuple[str, KeyfileWarnSeverity]: ...

class LldpNeighbor(GObject.GBoxed):
    """
    :Constructors:

    ::

        new() -> NM.LldpNeighbor
    """
    def get_attr_names(self) -> list[str]: ...
    def get_attr_string_value(self, name: str) -> tuple[bool, str]: ...
    def get_attr_type(self, name: str) -> GLib.VariantType: ...
    def get_attr_uint_value(self, name: str) -> tuple[bool, int]: ...
    def get_attr_value(self, name: str) -> GLib.Variant: ...
    @classmethod
    def new(cls) -> LldpNeighbor: ...
    def ref(self) -> None: ...
    def unref(self) -> None: ...

class Object(GObject.Object):
    """
    :Constructors:

    ::

        Object(**properties)

    Object NMObject

    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        client: Client | None
        path: str

    props: Props = ...
    def get_client(self) -> None: ...
    def get_path(self) -> str: ...

class ObjectClass(GObject.GPointer): ...

class Range(GObject.GBoxed):
    """
    :Constructors:

    ::

        new(start:int, end:int) -> NM.Range
    """
    def cmp(self, b: Range) -> int: ...
    @staticmethod
    def from_str(str: str) -> Range: ...
    def get_range(self) -> tuple[bool, int, int]: ...
    @classmethod
    def new(cls, start: int, end: int) -> Range: ...
    def ref(self) -> Range: ...
    def to_str(self) -> str: ...
    def unref(self) -> None: ...

class RemoteConnection(Object, Connection):
    """
    :Constructors:

    ::

        RemoteConnection(**properties)

    Object NMRemoteConnection

    Properties from NMRemoteConnection:
      unsaved -> gboolean:

      flags -> guint:

      filename -> gchararray:

      version-id -> guint64:

      visible -> gboolean:


    Signals from NMConnection:
      secrets-updated (gchararray)
      secrets-cleared ()
      changed ()

    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        filename: str
        flags: int
        unsaved: bool
        version_id: int
        visible: bool
        client: Client | None
        path: str

    props: Props = ...
    def commit_changes(
        self, save_to_disk: bool, cancellable: Gio.Cancellable | None = None
    ) -> bool: ...
    def commit_changes_async(
        self,
        save_to_disk: bool,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def commit_changes_finish(self, result: Gio.AsyncResult) -> bool: ...
    def delete(self, cancellable: Gio.Cancellable | None = None) -> bool: ...
    def delete_async(
        self,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def delete_finish(self, result: Gio.AsyncResult) -> bool: ...
    def get_filename(self) -> str: ...
    def get_flags(self) -> SettingsConnectionFlags: ...
    def get_secrets(
        self, setting_name: str, cancellable: Gio.Cancellable | None = None
    ) -> GLib.Variant: ...
    def get_secrets_async(
        self,
        setting_name: str,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def get_secrets_finish(self, result: Gio.AsyncResult) -> GLib.Variant: ...
    def get_unsaved(self) -> bool: ...
    def get_version_id(self) -> int: ...
    def get_visible(self) -> bool: ...
    def save(self, cancellable: Gio.Cancellable | None = None) -> bool: ...
    def save_async(
        self,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def save_finish(self, result: Gio.AsyncResult) -> bool: ...
    def update2(
        self,
        settings: GLib.Variant | None,
        flags: SettingsUpdate2Flags,
        args: GLib.Variant | None = None,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def update2_finish(self, result: Gio.AsyncResult) -> GLib.Variant: ...

class RemoteConnectionClass(GObject.GPointer): ...

class SecretAgentOld(GObject.Object, Gio.AsyncInitable, Gio.Initable):  # type: ignore
    """
    :Constructors:

    ::

        SecretAgentOld(**properties)

    Object NMSecretAgentOld

    Properties from NMSecretAgentOld:
      identifier -> gchararray:

      auto-register -> gboolean:

      registered -> gboolean:

      capabilities -> NMSecretAgentCapabilities:

      dbus-connection -> GDBusConnection:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        auto_register: bool
        capabilities: SecretAgentCapabilities
        dbus_connection: Gio.DBusConnection
        identifier: str
        registered: bool

    props: Props = ...
    parent: GObject.Object = ...
    def __init__(
        self,
        auto_register: bool = ...,
        capabilities: SecretAgentCapabilities = ...,
        dbus_connection: Gio.DBusConnection = ...,
        identifier: str = ...,
    ): ...
    def delete_secrets(
        self, connection: Connection, callback: Callable[..., None], *user_data: Any
    ) -> None: ...
    def destroy(self) -> None: ...
    def do_cancel_get_secrets(
        self, connection_path: str, setting_name: str
    ) -> None: ...
    def do_delete_secrets(
        self,
        connection: Connection,
        connection_path: str,
        callback: Callable[..., None],
        *user_data: Any,
    ) -> None: ...
    def do_get_secrets(
        self,
        connection: Connection,
        connection_path: str,
        setting_name: str,
        hints: Sequence[str],
        flags: SecretAgentGetSecretsFlags,
        callback: Callable[..., None],
        *user_data: Any,
    ) -> None: ...
    def do_save_secrets(
        self,
        connection: Connection,
        connection_path: str,
        callback: Callable[..., None],
        *user_data: Any,
    ) -> None: ...
    def enable(self, enable: bool) -> None: ...
    def get_context_busy_watcher(self) -> GObject.Object: ...
    def get_dbus_connection(self) -> Gio.DBusConnection: ...
    def get_dbus_name_owner(self) -> str: ...
    def get_main_context(self) -> GLib.MainContext: ...
    def get_registered(self) -> bool: ...
    def get_secrets(
        self,
        connection: Connection,
        setting_name: str,
        hints: Sequence[str],
        flags: SecretAgentGetSecretsFlags,
        callback: Callable[..., None],
        *user_data: Any,
    ) -> None: ...
    def register(self, cancellable: Gio.Cancellable | None = None) -> bool: ...
    def register_async(
        self,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def register_finish(self, result: Gio.AsyncResult) -> bool: ...
    def save_secrets(
        self, connection: Connection, callback: Callable[..., None], *user_data: Any
    ) -> None: ...
    def unregister(self, cancellable: Gio.Cancellable | None = None) -> bool: ...
    def unregister_async(
        self,
        cancellable: Gio.Cancellable | None = None,
        callback: Callable[..., None] | None = None,
        *user_data: Any,
    ) -> None: ...
    def unregister_finish(self, result: Gio.AsyncResult) -> bool: ...

class SecretAgentOldClass(GObject.GPointer):
    """
    :Constructors:

    ::

        SecretAgentOldClass()
    """

    parent: GObject.ObjectClass = ...
    get_secrets: Callable[..., None] = ...
    cancel_get_secrets: Callable[[SecretAgentOld, str, str], None] = ...
    save_secrets: Callable[..., None] = ...
    delete_secrets: Callable[..., None] = ...
    padding: list[None] = ...

class Setting(GObject.Object):
    """
    :Constructors:

    ::

        Setting(**properties)

    Object NMSetting

    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        name: str

    props: Props = ...
    def compare(self, b: Setting, flags: SettingCompareFlags) -> bool: ...
    def diff(
        self, b: Setting, flags: SettingCompareFlags, invert_results: bool
    ) -> tuple[bool, dict[str, int]]: ...
    def duplicate(self) -> Setting: ...
    def enumerate_values(self, func: Callable[..., None], *user_data: Any) -> None: ...
    def get_dbus_property_type(self, property_name: str) -> GLib.VariantType: ...
    @staticmethod
    def get_enum_property_type(setting_type: type, property_name: str) -> type: ...
    def get_name(self) -> str: ...
    def get_secret_flags(
        self, secret_name: str, out_flags: SettingSecretFlags
    ) -> bool: ...
    @staticmethod
    def lookup_type(name: str) -> type: ...
    def option_clear_by_name(
        self, predicate: Callable[[str], bool] | None = None
    ) -> None: ...
    def option_get(self, opt_name: str) -> GLib.Variant: ...
    def option_get_all_names(self) -> list[str] | None: ...
    def option_get_boolean(self, opt_name: str) -> tuple[bool, bool]: ...
    def option_get_uint32(self, opt_name: str) -> tuple[bool, int]: ...
    def option_set(
        self, opt_name: str, variant: GLib.Variant | None = None
    ) -> None: ...
    def option_set_boolean(self, opt_name: str, value: bool) -> None: ...
    def option_set_uint32(self, opt_name: str, value: int) -> None: ...
    def set_secret_flags(self, secret_name: str, flags: SettingSecretFlags) -> bool: ...
    def to_string(self) -> str: ...
    def verify(self, connection: Connection | None = None) -> bool: ...
    def verify_secrets(self, connection: Connection | None = None) -> bool: ...

class Setting6Lowpan(Setting):
    """
    :Constructors:

    ::

        Setting6Lowpan(**properties)
        new() -> NM.Setting

    Object NMSetting6Lowpan

    Properties from NMSetting6Lowpan:
      parent -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        parent: str
        name: str

    props: Props = ...
    def __init__(self, parent: str = ...): ...
    def get_parent(self) -> str: ...
    @classmethod
    def new(cls) -> Setting6Lowpan: ...

class Setting6LowpanClass(GObject.GPointer): ...

class Setting8021x(Setting):
    """
    :Constructors:

    ::

        Setting8021x(**properties)
        new() -> NM.Setting

    Object NMSetting8021x

    Properties from NMSetting8021x:
      eap -> GStrv:

      identity -> gchararray:

      anonymous-identity -> gchararray:

      pac-file -> gchararray:

      ca-cert -> GBytes:

      ca-cert-password -> gchararray:

      ca-cert-password-flags -> NMSettingSecretFlags:

      ca-path -> gchararray:

      subject-match -> gchararray:

      altsubject-matches -> GStrv:

      domain-suffix-match -> gchararray:

      domain-match -> gchararray:

      client-cert -> GBytes:

      client-cert-password -> gchararray:

      client-cert-password-flags -> NMSettingSecretFlags:

      phase1-peapver -> gchararray:

      phase1-peaplabel -> gchararray:

      phase1-fast-provisioning -> gchararray:

      phase1-auth-flags -> guint:

      phase2-auth -> gchararray:

      phase2-autheap -> gchararray:

      phase2-ca-cert -> GBytes:

      phase2-ca-cert-password -> gchararray:

      phase2-ca-cert-password-flags -> NMSettingSecretFlags:

      phase2-ca-path -> gchararray:

      phase2-subject-match -> gchararray:

      phase2-altsubject-matches -> GStrv:

      phase2-domain-suffix-match -> gchararray:

      phase2-domain-match -> gchararray:

      phase2-client-cert -> GBytes:

      phase2-client-cert-password -> gchararray:

      phase2-client-cert-password-flags -> NMSettingSecretFlags:

      password -> gchararray:

      password-flags -> NMSettingSecretFlags:

      password-raw -> GBytes:

      password-raw-flags -> NMSettingSecretFlags:

      private-key -> GBytes:

      private-key-password -> gchararray:

      private-key-password-flags -> NMSettingSecretFlags:

      phase2-private-key -> GBytes:

      phase2-private-key-password -> gchararray:

      phase2-private-key-password-flags -> NMSettingSecretFlags:

      pin -> gchararray:

      pin-flags -> NMSettingSecretFlags:

      system-ca-certs -> gboolean:

      optional -> gboolean:

      auth-timeout -> gint:

      openssl-ciphers -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        altsubject_matches: list[str]
        anonymous_identity: str
        auth_timeout: int
        ca_cert: GLib.Bytes
        ca_cert_password: str
        ca_cert_password_flags: SettingSecretFlags
        ca_path: str
        client_cert: GLib.Bytes
        client_cert_password: str
        client_cert_password_flags: SettingSecretFlags
        domain_match: str
        domain_suffix_match: str
        eap: list[str]
        identity: str
        openssl_ciphers: str
        optional: bool
        pac_file: str
        password: str
        password_flags: SettingSecretFlags
        password_raw: GLib.Bytes
        password_raw_flags: SettingSecretFlags
        phase1_auth_flags: int
        phase1_fast_provisioning: str
        phase1_peaplabel: str
        phase1_peapver: str
        phase2_altsubject_matches: list[str]
        phase2_auth: str
        phase2_autheap: str
        phase2_ca_cert: GLib.Bytes
        phase2_ca_cert_password: str
        phase2_ca_cert_password_flags: SettingSecretFlags
        phase2_ca_path: str
        phase2_client_cert: GLib.Bytes
        phase2_client_cert_password: str
        phase2_client_cert_password_flags: SettingSecretFlags
        phase2_domain_match: str
        phase2_domain_suffix_match: str
        phase2_private_key: GLib.Bytes
        phase2_private_key_password: str
        phase2_private_key_password_flags: SettingSecretFlags
        phase2_subject_match: str
        pin: str
        pin_flags: SettingSecretFlags
        private_key: GLib.Bytes
        private_key_password: str
        private_key_password_flags: SettingSecretFlags
        subject_match: str
        system_ca_certs: bool
        name: str

    props: Props = ...
    def __init__(
        self,
        altsubject_matches: Sequence[str] = ...,
        anonymous_identity: str = ...,
        auth_timeout: int = ...,
        ca_cert: GLib.Bytes = ...,
        ca_cert_password: str = ...,
        ca_cert_password_flags: SettingSecretFlags = ...,
        ca_path: str = ...,
        client_cert: GLib.Bytes = ...,
        client_cert_password: str = ...,
        client_cert_password_flags: SettingSecretFlags = ...,
        domain_match: str = ...,
        domain_suffix_match: str = ...,
        eap: Sequence[str] = ...,
        identity: str = ...,
        openssl_ciphers: str = ...,
        optional: bool = ...,
        pac_file: str = ...,
        password: str = ...,
        password_flags: SettingSecretFlags = ...,
        password_raw: GLib.Bytes = ...,
        password_raw_flags: SettingSecretFlags = ...,
        phase1_auth_flags: int = ...,
        phase1_fast_provisioning: str = ...,
        phase1_peaplabel: str = ...,
        phase1_peapver: str = ...,
        phase2_altsubject_matches: Sequence[str] = ...,
        phase2_auth: str = ...,
        phase2_autheap: str = ...,
        phase2_ca_cert: GLib.Bytes = ...,
        phase2_ca_cert_password: str = ...,
        phase2_ca_cert_password_flags: SettingSecretFlags = ...,
        phase2_ca_path: str = ...,
        phase2_client_cert: GLib.Bytes = ...,
        phase2_client_cert_password: str = ...,
        phase2_client_cert_password_flags: SettingSecretFlags = ...,
        phase2_domain_match: str = ...,
        phase2_domain_suffix_match: str = ...,
        phase2_private_key: GLib.Bytes = ...,
        phase2_private_key_password: str = ...,
        phase2_private_key_password_flags: SettingSecretFlags = ...,
        phase2_subject_match: str = ...,
        pin: str = ...,
        pin_flags: SettingSecretFlags = ...,
        private_key: GLib.Bytes = ...,
        private_key_password: str = ...,
        private_key_password_flags: SettingSecretFlags = ...,
        subject_match: str = ...,
        system_ca_certs: bool = ...,
    ): ...
    def add_altsubject_match(self, altsubject_match: str) -> bool: ...
    def add_eap_method(self, eap: str) -> bool: ...
    def add_phase2_altsubject_match(self, phase2_altsubject_match: str) -> bool: ...
    @staticmethod
    def check_cert_scheme(pdata: None, length: int) -> Setting8021xCKScheme: ...
    def clear_altsubject_matches(self) -> None: ...
    def clear_eap_methods(self) -> None: ...
    def clear_phase2_altsubject_matches(self) -> None: ...
    def get_altsubject_match(self, i: int) -> str: ...
    def get_anonymous_identity(self) -> str: ...
    def get_auth_timeout(self) -> int: ...
    def get_ca_cert_blob(self) -> GLib.Bytes: ...
    def get_ca_cert_password(self) -> str: ...
    def get_ca_cert_password_flags(self) -> SettingSecretFlags: ...
    def get_ca_cert_path(self) -> str: ...
    def get_ca_cert_scheme(self) -> Setting8021xCKScheme: ...
    def get_ca_cert_uri(self) -> str: ...
    def get_ca_path(self) -> str: ...
    def get_client_cert_blob(self) -> GLib.Bytes: ...
    def get_client_cert_password(self) -> str: ...
    def get_client_cert_password_flags(self) -> SettingSecretFlags: ...
    def get_client_cert_path(self) -> str: ...
    def get_client_cert_scheme(self) -> Setting8021xCKScheme: ...
    def get_client_cert_uri(self) -> str: ...
    def get_domain_match(self) -> str: ...
    def get_domain_suffix_match(self) -> str: ...
    def get_eap_method(self, i: int) -> str: ...
    def get_identity(self) -> str: ...
    def get_num_altsubject_matches(self) -> int: ...
    def get_num_eap_methods(self) -> int: ...
    def get_num_phase2_altsubject_matches(self) -> int: ...
    def get_openssl_ciphers(self) -> str: ...
    def get_optional(self) -> bool: ...
    def get_pac_file(self) -> str: ...
    def get_password(self) -> str: ...
    def get_password_flags(self) -> SettingSecretFlags: ...
    def get_password_raw(self) -> GLib.Bytes: ...
    def get_password_raw_flags(self) -> SettingSecretFlags: ...
    def get_phase1_auth_flags(self) -> Setting8021xAuthFlags: ...
    def get_phase1_fast_provisioning(self) -> str: ...
    def get_phase1_peaplabel(self) -> str: ...
    def get_phase1_peapver(self) -> str: ...
    def get_phase2_altsubject_match(self, i: int) -> str: ...
    def get_phase2_auth(self) -> str: ...
    def get_phase2_autheap(self) -> str: ...
    def get_phase2_ca_cert_blob(self) -> GLib.Bytes: ...
    def get_phase2_ca_cert_password(self) -> str: ...
    def get_phase2_ca_cert_password_flags(self) -> SettingSecretFlags: ...
    def get_phase2_ca_cert_path(self) -> str: ...
    def get_phase2_ca_cert_scheme(self) -> Setting8021xCKScheme: ...
    def get_phase2_ca_cert_uri(self) -> str: ...
    def get_phase2_ca_path(self) -> str: ...
    def get_phase2_client_cert_blob(self) -> GLib.Bytes: ...
    def get_phase2_client_cert_password(self) -> str: ...
    def get_phase2_client_cert_password_flags(self) -> SettingSecretFlags: ...
    def get_phase2_client_cert_path(self) -> str: ...
    def get_phase2_client_cert_scheme(self) -> Setting8021xCKScheme: ...
    def get_phase2_client_cert_uri(self) -> str: ...
    def get_phase2_domain_match(self) -> str: ...
    def get_phase2_domain_suffix_match(self) -> str: ...
    def get_phase2_private_key_blob(self) -> GLib.Bytes: ...
    def get_phase2_private_key_format(self) -> Setting8021xCKFormat: ...
    def get_phase2_private_key_password(self) -> str: ...
    def get_phase2_private_key_password_flags(self) -> SettingSecretFlags: ...
    def get_phase2_private_key_path(self) -> str: ...
    def get_phase2_private_key_scheme(self) -> Setting8021xCKScheme: ...
    def get_phase2_private_key_uri(self) -> str: ...
    def get_phase2_subject_match(self) -> str: ...
    def get_pin(self) -> str: ...
    def get_pin_flags(self) -> SettingSecretFlags: ...
    def get_private_key_blob(self) -> GLib.Bytes: ...
    def get_private_key_format(self) -> Setting8021xCKFormat: ...
    def get_private_key_password(self) -> str: ...
    def get_private_key_password_flags(self) -> SettingSecretFlags: ...
    def get_private_key_path(self) -> str: ...
    def get_private_key_scheme(self) -> Setting8021xCKScheme: ...
    def get_private_key_uri(self) -> str: ...
    def get_subject_match(self) -> str: ...
    def get_system_ca_certs(self) -> bool: ...
    @classmethod
    def new(cls) -> Setting8021x: ...
    def remove_altsubject_match(self, i: int) -> None: ...
    def remove_altsubject_match_by_value(self, altsubject_match: str) -> bool: ...
    def remove_eap_method(self, i: int) -> None: ...
    def remove_eap_method_by_value(self, eap: str) -> bool: ...
    def remove_phase2_altsubject_match(self, i: int) -> None: ...
    def remove_phase2_altsubject_match_by_value(
        self, phase2_altsubject_match: str
    ) -> bool: ...
    def set_ca_cert(
        self, value: str, scheme: Setting8021xCKScheme, out_format: Setting8021xCKFormat
    ) -> bool: ...
    def set_client_cert(
        self, value: str, scheme: Setting8021xCKScheme, out_format: Setting8021xCKFormat
    ) -> bool: ...
    def set_phase2_ca_cert(
        self, value: str, scheme: Setting8021xCKScheme, out_format: Setting8021xCKFormat
    ) -> bool: ...
    def set_phase2_client_cert(
        self, value: str, scheme: Setting8021xCKScheme, out_format: Setting8021xCKFormat
    ) -> bool: ...
    def set_phase2_private_key(
        self,
        value: str,
        password: str,
        scheme: Setting8021xCKScheme,
        out_format: Setting8021xCKFormat,
    ) -> bool: ...
    def set_private_key(
        self,
        value: str,
        password: str,
        scheme: Setting8021xCKScheme,
        out_format: Setting8021xCKFormat,
    ) -> bool: ...

class Setting8021xClass(GObject.GPointer): ...

class SettingAdsl(Setting):
    """
    :Constructors:

    ::

        SettingAdsl(**properties)
        new() -> NM.Setting

    Object NMSettingAdsl

    Properties from NMSettingAdsl:
      username -> gchararray:

      password -> gchararray:

      password-flags -> NMSettingSecretFlags:

      protocol -> gchararray:

      encapsulation -> gchararray:

      vpi -> guint:

      vci -> guint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        encapsulation: str
        password: str
        password_flags: SettingSecretFlags
        protocol: str
        username: str
        vci: int
        vpi: int
        name: str

    props: Props = ...
    def __init__(
        self,
        encapsulation: str = ...,
        password: str = ...,
        password_flags: SettingSecretFlags = ...,
        protocol: str = ...,
        username: str = ...,
        vci: int = ...,
        vpi: int = ...,
    ): ...
    def get_encapsulation(self) -> str: ...
    def get_password(self) -> str: ...
    def get_password_flags(self) -> SettingSecretFlags: ...
    def get_protocol(self) -> str: ...
    def get_username(self) -> str: ...
    def get_vci(self) -> int: ...
    def get_vpi(self) -> int: ...
    @classmethod
    def new(cls) -> SettingAdsl: ...

class SettingAdslClass(GObject.GPointer): ...

class SettingBluetooth(Setting):
    """
    :Constructors:

    ::

        SettingBluetooth(**properties)
        new() -> NM.Setting

    Object NMSettingBluetooth

    Properties from NMSettingBluetooth:
      bdaddr -> gchararray:

      type -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        bdaddr: str
        type: str
        name: str

    props: Props = ...
    def __init__(self, bdaddr: str = ..., type: str = ...): ...
    def get_bdaddr(self) -> str: ...
    def get_connection_type(self) -> str: ...
    @classmethod
    def new(cls) -> SettingBluetooth: ...

class SettingBluetoothClass(GObject.GPointer): ...

class SettingBond(Setting):
    """
    :Constructors:

    ::

        SettingBond(**properties)
        new() -> NM.Setting

    Object NMSettingBond

    Properties from NMSettingBond:
      options -> GHashTable:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        options: dict[str, str]
        name: str

    props: Props = ...
    def __init__(self, options: dict[str, str] = ...): ...
    def add_option(self, name: str, value: str) -> bool: ...
    def get_num_options(self) -> int: ...
    def get_option(self, idx: int) -> tuple[bool, str, str]: ...
    def get_option_by_name(self, name: str) -> str: ...
    def get_option_default(self, name: str) -> str: ...
    def get_option_normalized(self, name: str) -> str: ...
    def get_valid_options(self) -> list[str] | None: ...
    @classmethod
    def new(cls) -> SettingBond: ...
    def remove_option(self, name: str) -> bool: ...
    @staticmethod
    def validate_option(name: str, value: str | None = None) -> bool: ...

class SettingBondClass(GObject.GPointer): ...

class SettingBondPort(Setting):
    """
    :Constructors:

    ::

        SettingBondPort(**properties)
        new() -> NM.Setting

    Object NMSettingBondPort

    Properties from NMSettingBondPort:
      queue-id -> guint:

      prio -> gint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        prio: int
        queue_id: int
        name: str

    props: Props = ...
    def __init__(self, prio: int = ..., queue_id: int = ...): ...
    def get_prio(self) -> int: ...
    def get_queue_id(self) -> int: ...
    @classmethod
    def new(cls) -> SettingBondPort: ...

class SettingBondPortClass(GObject.GPointer): ...

class SettingBridge(Setting):
    """
    :Constructors:

    ::

        SettingBridge(**properties)
        new() -> NM.Setting

    Object NMSettingBridge

    Properties from NMSettingBridge:
      mac-address -> gchararray:

      stp -> gboolean:

      priority -> guint:

      forward-delay -> guint:

      hello-time -> guint:

      max-age -> guint:

      ageing-time -> guint:

      group-address -> gchararray:

      group-forward-mask -> guint:

      multicast-hash-max -> guint:

      multicast-last-member-count -> guint:

      multicast-last-member-interval -> guint64:

      multicast-membership-interval -> guint64:

      multicast-router -> gchararray:

      multicast-querier -> gboolean:

      multicast-querier-interval -> guint64:

      multicast-query-interval -> guint64:

      multicast-query-response-interval -> guint64:

      multicast-query-use-ifaddr -> gboolean:

      multicast-snooping -> gboolean:

      multicast-startup-query-count -> guint:

      multicast-startup-query-interval -> guint64:

      vlan-filtering -> gboolean:

      vlan-default-pvid -> guint:

      vlan-protocol -> gchararray:

      vlan-stats-enabled -> gboolean:

      vlans -> GPtrArray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        ageing_time: int
        forward_delay: int
        group_address: str
        group_forward_mask: int
        hello_time: int
        mac_address: str
        max_age: int
        multicast_hash_max: int
        multicast_last_member_count: int
        multicast_last_member_interval: int
        multicast_membership_interval: int
        multicast_querier: bool
        multicast_querier_interval: int
        multicast_query_interval: int
        multicast_query_response_interval: int
        multicast_query_use_ifaddr: bool
        multicast_router: str
        multicast_snooping: bool
        multicast_startup_query_count: int
        multicast_startup_query_interval: int
        priority: int
        stp: bool
        vlan_default_pvid: int
        vlan_filtering: bool
        vlan_protocol: str
        vlan_stats_enabled: bool
        vlans: list[BridgeVlan]
        name: str

    props: Props = ...
    def __init__(
        self,
        ageing_time: int = ...,
        forward_delay: int = ...,
        group_address: str = ...,
        group_forward_mask: int = ...,
        hello_time: int = ...,
        mac_address: str = ...,
        max_age: int = ...,
        multicast_hash_max: int = ...,
        multicast_last_member_count: int = ...,
        multicast_last_member_interval: int = ...,
        multicast_membership_interval: int = ...,
        multicast_querier: bool = ...,
        multicast_querier_interval: int = ...,
        multicast_query_interval: int = ...,
        multicast_query_response_interval: int = ...,
        multicast_query_use_ifaddr: bool = ...,
        multicast_router: str = ...,
        multicast_snooping: bool = ...,
        multicast_startup_query_count: int = ...,
        multicast_startup_query_interval: int = ...,
        priority: int = ...,
        stp: bool = ...,
        vlan_default_pvid: int = ...,
        vlan_filtering: bool = ...,
        vlan_protocol: str = ...,
        vlan_stats_enabled: bool = ...,
        vlans: Sequence[BridgeVlan] = ...,
    ): ...
    def add_vlan(self, vlan: BridgeVlan) -> None: ...
    def clear_vlans(self) -> None: ...
    def get_ageing_time(self) -> int: ...
    def get_forward_delay(self) -> int: ...
    def get_group_address(self) -> str: ...
    def get_group_forward_mask(self) -> int: ...
    def get_hello_time(self) -> int: ...
    def get_mac_address(self) -> str: ...
    def get_max_age(self) -> int: ...
    def get_multicast_hash_max(self) -> int: ...
    def get_multicast_last_member_count(self) -> int: ...
    def get_multicast_last_member_interval(self) -> int: ...
    def get_multicast_membership_interval(self) -> int: ...
    def get_multicast_querier(self) -> bool: ...
    def get_multicast_querier_interval(self) -> int: ...
    def get_multicast_query_interval(self) -> int: ...
    def get_multicast_query_response_interval(self) -> int: ...
    def get_multicast_query_use_ifaddr(self) -> bool: ...
    def get_multicast_router(self) -> str: ...
    def get_multicast_snooping(self) -> bool: ...
    def get_multicast_startup_query_count(self) -> int: ...
    def get_multicast_startup_query_interval(self) -> int: ...
    def get_num_vlans(self) -> int: ...
    def get_priority(self) -> int: ...
    def get_stp(self) -> bool: ...
    def get_vlan(self, idx: int) -> BridgeVlan: ...
    def get_vlan_default_pvid(self) -> int: ...
    def get_vlan_filtering(self) -> bool: ...
    def get_vlan_protocol(self) -> str: ...
    def get_vlan_stats_enabled(self) -> bool: ...
    @classmethod
    def new(cls) -> SettingBridge: ...
    def remove_vlan(self, idx: int) -> None: ...
    def remove_vlan_by_vid(self, vid_start: int, vid_end: int) -> bool: ...

class SettingBridgeClass(GObject.GPointer): ...

class SettingBridgePort(Setting):
    """
    :Constructors:

    ::

        SettingBridgePort(**properties)
        new() -> NM.Setting

    Object NMSettingBridgePort

    Properties from NMSettingBridgePort:
      priority -> guint:

      path-cost -> guint:

      hairpin-mode -> gboolean:

      vlans -> GPtrArray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        hairpin_mode: bool
        path_cost: int
        priority: int
        vlans: list[BridgeVlan]
        name: str

    props: Props = ...
    def __init__(
        self,
        hairpin_mode: bool = ...,
        path_cost: int = ...,
        priority: int = ...,
        vlans: Sequence[BridgeVlan] = ...,
    ): ...
    def add_vlan(self, vlan: BridgeVlan) -> None: ...
    def clear_vlans(self) -> None: ...
    def get_hairpin_mode(self) -> bool: ...
    def get_num_vlans(self) -> int: ...
    def get_path_cost(self) -> int: ...
    def get_priority(self) -> int: ...
    def get_vlan(self, idx: int) -> BridgeVlan: ...
    @classmethod
    def new(cls) -> SettingBridgePort: ...
    def remove_vlan(self, idx: int) -> None: ...
    def remove_vlan_by_vid(self, vid_start: int, vid_end: int) -> bool: ...

class SettingBridgePortClass(GObject.GPointer): ...

class SettingCdma(Setting):
    """
    :Constructors:

    ::

        SettingCdma(**properties)
        new() -> NM.Setting

    Object NMSettingCdma

    Properties from NMSettingCdma:
      number -> gchararray:

      username -> gchararray:

      password -> gchararray:

      password-flags -> NMSettingSecretFlags:

      mtu -> guint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        mtu: int
        number: str
        password: str
        password_flags: SettingSecretFlags
        username: str
        name: str

    props: Props = ...
    def __init__(
        self,
        mtu: int = ...,
        number: str = ...,
        password: str = ...,
        password_flags: SettingSecretFlags = ...,
        username: str = ...,
    ): ...
    def get_mtu(self) -> int: ...
    def get_number(self) -> str: ...
    def get_password(self) -> str: ...
    def get_password_flags(self) -> SettingSecretFlags: ...
    def get_username(self) -> str: ...
    @classmethod
    def new(cls) -> SettingCdma: ...

class SettingCdmaClass(GObject.GPointer): ...
class SettingClass(GObject.GPointer): ...

class SettingConnection(Setting):
    """
    :Constructors:

    ::

        SettingConnection(**properties)
        new() -> NM.Setting

    Object NMSettingConnection

    Properties from NMSettingConnection:
      id -> gchararray:

      uuid -> gchararray:

      interface-name -> gchararray:

      type -> gchararray:

      permissions -> GStrv:

      autoconnect -> gboolean:

      autoconnect-priority -> gint:

      autoconnect-retries -> gint:

      multi-connect -> gint:

      timestamp -> guint64:

      read-only -> gboolean:

      zone -> gchararray:

      master -> gchararray:

      controller -> gchararray:

      slave-type -> gchararray:

      port-type -> gchararray:

      autoconnect-slaves -> NMSettingConnectionAutoconnectSlaves:

      autoconnect-ports -> gint:

      secondaries -> GStrv:

      gateway-ping-timeout -> guint:

      metered -> NMMetered:

      lldp -> gint:

      mdns -> gint:

      llmnr -> gint:

      dns-over-tls -> gint:

      mptcp-flags -> guint:

      stable-id -> gchararray:

      auth-retries -> gint:

      wait-device-timeout -> gint:

      mud-url -> gchararray:

      wait-activation-delay -> gint:

      down-on-poweroff -> gint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        auth_retries: int
        autoconnect: bool
        autoconnect_ports: int
        autoconnect_priority: int
        autoconnect_retries: int
        autoconnect_slaves: SettingConnectionAutoconnectSlaves
        controller: str
        dns_over_tls: int
        down_on_poweroff: int
        gateway_ping_timeout: int
        id: str
        interface_name: str
        lldp: int
        llmnr: int
        master: str
        mdns: int
        metered: Metered
        mptcp_flags: int
        mud_url: str
        multi_connect: int
        permissions: list[str]
        port_type: str
        read_only: bool
        secondaries: list[str]
        slave_type: str
        stable_id: str
        timestamp: int
        type: str
        uuid: str
        wait_activation_delay: int
        wait_device_timeout: int
        zone: str
        name: str

    props: Props = ...
    def __init__(
        self,
        auth_retries: int = ...,
        autoconnect: bool = ...,
        autoconnect_ports: int = ...,
        autoconnect_priority: int = ...,
        autoconnect_retries: int = ...,
        autoconnect_slaves: SettingConnectionAutoconnectSlaves = ...,
        controller: str = ...,
        dns_over_tls: int = ...,
        down_on_poweroff: int = ...,
        gateway_ping_timeout: int = ...,
        id: str = ...,
        interface_name: str = ...,
        lldp: int = ...,
        llmnr: int = ...,
        master: str = ...,
        mdns: int = ...,
        metered: Metered = ...,
        mptcp_flags: int = ...,
        mud_url: str = ...,
        multi_connect: int = ...,
        permissions: Sequence[str] = ...,
        port_type: str = ...,
        read_only: bool = ...,
        secondaries: Sequence[str] = ...,
        slave_type: str = ...,
        stable_id: str = ...,
        timestamp: int = ...,
        type: str = ...,
        uuid: str = ...,
        wait_activation_delay: int = ...,
        wait_device_timeout: int = ...,
        zone: str = ...,
    ): ...
    def add_permission(
        self, ptype: str, pitem: str, detail: str | None = None
    ) -> bool: ...
    def add_secondary(self, sec_uuid: str) -> bool: ...
    def get_auth_retries(self) -> int: ...
    def get_autoconnect(self) -> bool: ...
    def get_autoconnect_ports(self) -> Ternary: ...
    def get_autoconnect_priority(self) -> int: ...
    def get_autoconnect_retries(self) -> int: ...
    def get_autoconnect_slaves(self) -> SettingConnectionAutoconnectSlaves: ...
    def get_connection_type(self) -> str: ...
    def get_controller(self) -> str: ...
    def get_dns_over_tls(self) -> SettingConnectionDnsOverTls: ...
    def get_down_on_poweroff(self) -> SettingConnectionDownOnPoweroff: ...
    def get_gateway_ping_timeout(self) -> int: ...
    def get_id(self) -> str: ...
    def get_interface_name(self) -> str: ...
    def get_lldp(self) -> SettingConnectionLldp: ...
    def get_llmnr(self) -> SettingConnectionLlmnr: ...
    def get_master(self) -> str: ...
    def get_mdns(self) -> SettingConnectionMdns: ...
    def get_metered(self) -> Metered: ...
    def get_mptcp_flags(self) -> MptcpFlags: ...
    def get_mud_url(self) -> str: ...
    def get_multi_connect(self) -> ConnectionMultiConnect: ...
    def get_num_permissions(self) -> int: ...
    def get_num_secondaries(self) -> int: ...
    def get_permission(
        self, idx: int, out_ptype: str, out_pitem: str, out_detail: str
    ) -> bool: ...
    def get_port_type(self) -> str: ...
    def get_read_only(self) -> bool: ...
    def get_secondary(self, idx: int) -> str: ...
    def get_slave_type(self) -> str: ...
    def get_stable_id(self) -> str: ...
    def get_timestamp(self) -> int: ...
    def get_uuid(self) -> str: ...
    def get_wait_activation_delay(self) -> int: ...
    def get_wait_device_timeout(self) -> int: ...
    def get_zone(self) -> str: ...
    def is_slave_type(self, type: str) -> bool: ...
    @classmethod
    def new(cls) -> SettingConnection: ...
    def permissions_user_allowed(self, uname: str) -> bool: ...
    def remove_permission(self, idx: int) -> None: ...
    def remove_permission_by_value(
        self, ptype: str, pitem: str, detail: str | None = None
    ) -> bool: ...
    def remove_secondary(self, idx: int) -> None: ...
    def remove_secondary_by_value(self, sec_uuid: str) -> bool: ...

class SettingConnectionClass(GObject.GPointer): ...

class SettingDcb(Setting):
    """
    :Constructors:

    ::

        SettingDcb(**properties)
        new() -> NM.Setting

    Object NMSettingDcb

    Properties from NMSettingDcb:
      app-fcoe-flags -> NMSettingDcbFlags:

      app-fcoe-priority -> gint:

      app-fcoe-mode -> gchararray:

      app-iscsi-flags -> NMSettingDcbFlags:

      app-iscsi-priority -> gint:

      app-fip-flags -> NMSettingDcbFlags:

      app-fip-priority -> gint:

      priority-flow-control-flags -> NMSettingDcbFlags:

      priority-flow-control -> GArray:

      priority-group-flags -> NMSettingDcbFlags:

      priority-group-id -> GArray:

      priority-group-bandwidth -> GArray:

      priority-bandwidth -> GArray:

      priority-strict-bandwidth -> GArray:

      priority-traffic-class -> GArray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        app_fcoe_flags: SettingDcbFlags
        app_fcoe_mode: str
        app_fcoe_priority: int
        app_fip_flags: SettingDcbFlags
        app_fip_priority: int
        app_iscsi_flags: SettingDcbFlags
        app_iscsi_priority: int
        priority_bandwidth: list[int]
        priority_flow_control: list[bool]
        priority_flow_control_flags: SettingDcbFlags
        priority_group_bandwidth: list[int]
        priority_group_flags: SettingDcbFlags
        priority_group_id: list[int]
        priority_strict_bandwidth: list[bool]
        priority_traffic_class: list[int]
        name: str

    props: Props = ...
    def __init__(
        self,
        app_fcoe_flags: SettingDcbFlags = ...,
        app_fcoe_mode: str = ...,
        app_fcoe_priority: int = ...,
        app_fip_flags: SettingDcbFlags = ...,
        app_fip_priority: int = ...,
        app_iscsi_flags: SettingDcbFlags = ...,
        app_iscsi_priority: int = ...,
        priority_bandwidth: Sequence[int] = ...,
        priority_flow_control: Sequence[bool] = ...,
        priority_flow_control_flags: SettingDcbFlags = ...,
        priority_group_bandwidth: Sequence[int] = ...,
        priority_group_flags: SettingDcbFlags = ...,
        priority_group_id: Sequence[int] = ...,
        priority_strict_bandwidth: Sequence[bool] = ...,
        priority_traffic_class: Sequence[int] = ...,
    ): ...
    def get_app_fcoe_flags(self) -> SettingDcbFlags: ...
    def get_app_fcoe_mode(self) -> str: ...
    def get_app_fcoe_priority(self) -> int: ...
    def get_app_fip_flags(self) -> SettingDcbFlags: ...
    def get_app_fip_priority(self) -> int: ...
    def get_app_iscsi_flags(self) -> SettingDcbFlags: ...
    def get_app_iscsi_priority(self) -> int: ...
    def get_priority_bandwidth(self, user_priority: int) -> int: ...
    def get_priority_flow_control(self, user_priority: int) -> bool: ...
    def get_priority_flow_control_flags(self) -> SettingDcbFlags: ...
    def get_priority_group_bandwidth(self, group_id: int) -> int: ...
    def get_priority_group_flags(self) -> SettingDcbFlags: ...
    def get_priority_group_id(self, user_priority: int) -> int: ...
    def get_priority_strict_bandwidth(self, user_priority: int) -> bool: ...
    def get_priority_traffic_class(self, user_priority: int) -> int: ...
    @classmethod
    def new(cls) -> SettingDcb: ...
    def set_priority_bandwidth(
        self, user_priority: int, bandwidth_percent: int
    ) -> None: ...
    def set_priority_flow_control(self, user_priority: int, enabled: bool) -> None: ...
    def set_priority_group_bandwidth(
        self, group_id: int, bandwidth_percent: int
    ) -> None: ...
    def set_priority_group_id(self, user_priority: int, group_id: int) -> None: ...
    def set_priority_strict_bandwidth(
        self, user_priority: int, strict: bool
    ) -> None: ...
    def set_priority_traffic_class(
        self, user_priority: int, traffic_class: int
    ) -> None: ...

class SettingDcbClass(GObject.GPointer): ...

class SettingDummy(Setting):
    """
    :Constructors:

    ::

        SettingDummy(**properties)
        new() -> NM.Setting

    Object NMSettingDummy

    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        name: str

    props: Props = ...
    @classmethod
    def new(cls) -> SettingDummy: ...

class SettingDummyClass(GObject.GPointer): ...

class SettingEthtool(Setting):
    """
    :Constructors:

    ::

        SettingEthtool(**properties)
        new() -> NM.Setting

    Object NMSettingEthtool

    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        name: str

    props: Props = ...
    def clear_features(self) -> None: ...
    def get_feature(self, optname: str) -> Ternary: ...
    def get_optnames(self) -> tuple[list[str], int]: ...
    @classmethod
    def new(cls) -> SettingEthtool: ...
    def set_feature(self, optname: str, value: Ternary) -> None: ...

class SettingEthtoolClass(GObject.GPointer): ...

class SettingGeneric(Setting):
    """
    :Constructors:

    ::

        SettingGeneric(**properties)
        new() -> NM.Setting

    Object NMSettingGeneric

    Properties from NMSettingGeneric:
      device-handler -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        device_handler: str
        name: str

    props: Props = ...
    def __init__(self, device_handler: str = ...): ...
    def get_device_handler(self) -> str: ...
    @classmethod
    def new(cls) -> SettingGeneric: ...

class SettingGenericClass(GObject.GPointer): ...

class SettingGsm(Setting):
    """
    :Constructors:

    ::

        SettingGsm(**properties)
        new() -> NM.Setting

    Object NMSettingGsm

    Properties from NMSettingGsm:
      auto-config -> gboolean:

      number -> gchararray:

      username -> gchararray:

      password -> gchararray:

      password-flags -> NMSettingSecretFlags:

      apn -> gchararray:

      network-id -> gchararray:

      pin -> gchararray:

      pin-flags -> NMSettingSecretFlags:

      home-only -> gboolean:

      device-id -> gchararray:

      sim-id -> gchararray:

      sim-operator-id -> gchararray:

      mtu -> guint:

      initial-eps-bearer-configure -> gboolean:

      initial-eps-bearer-apn -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        apn: str
        auto_config: bool
        device_id: str
        home_only: bool
        initial_eps_bearer_apn: str
        initial_eps_bearer_configure: bool
        mtu: int
        network_id: str
        number: str
        password: str
        password_flags: SettingSecretFlags
        pin: str
        pin_flags: SettingSecretFlags
        sim_id: str
        sim_operator_id: str
        username: str
        name: str

    props: Props = ...
    def __init__(
        self,
        apn: str = ...,
        auto_config: bool = ...,
        device_id: str = ...,
        home_only: bool = ...,
        initial_eps_bearer_apn: str = ...,
        initial_eps_bearer_configure: bool = ...,
        mtu: int = ...,
        network_id: str = ...,
        number: str = ...,
        password: str = ...,
        password_flags: SettingSecretFlags = ...,
        pin: str = ...,
        pin_flags: SettingSecretFlags = ...,
        sim_id: str = ...,
        sim_operator_id: str = ...,
        username: str = ...,
    ): ...
    def get_apn(self) -> str: ...
    def get_auto_config(self) -> bool: ...
    def get_device_id(self) -> str: ...
    def get_home_only(self) -> bool: ...
    def get_initial_eps_apn(self) -> str: ...
    def get_initial_eps_config(self) -> bool: ...
    def get_mtu(self) -> int: ...
    def get_network_id(self) -> str: ...
    def get_number(self) -> str: ...
    def get_password(self) -> str: ...
    def get_password_flags(self) -> SettingSecretFlags: ...
    def get_pin(self) -> str: ...
    def get_pin_flags(self) -> SettingSecretFlags: ...
    def get_sim_id(self) -> str: ...
    def get_sim_operator_id(self) -> str: ...
    def get_username(self) -> str: ...
    @classmethod
    def new(cls) -> SettingGsm: ...

class SettingGsmClass(GObject.GPointer): ...

class SettingHostname(Setting):
    """
    :Constructors:

    ::

        SettingHostname(**properties)
        new() -> NM.Setting

    Object NMSettingHostname

    Properties from NMSettingHostname:
      priority -> gint:

      from-dhcp -> NMTernary:

      from-dns-lookup -> NMTernary:

      only-from-default -> NMTernary:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        from_dhcp: Ternary
        from_dns_lookup: Ternary
        only_from_default: Ternary
        priority: int
        name: str

    props: Props = ...
    def __init__(
        self,
        from_dhcp: Ternary = ...,
        from_dns_lookup: Ternary = ...,
        only_from_default: Ternary = ...,
        priority: int = ...,
    ): ...
    def get_from_dhcp(self) -> Ternary: ...
    def get_from_dns_lookup(self) -> Ternary: ...
    def get_only_from_default(self) -> Ternary: ...
    def get_priority(self) -> int: ...
    @classmethod
    def new(cls) -> SettingHostname: ...

class SettingHostnameClass(GObject.GPointer): ...

class SettingHsr(Setting):
    """
    :Constructors:

    ::

        SettingHsr(**properties)
        new() -> NM.Setting

    Object NMSettingHsr

    Properties from NMSettingHsr:
      port1 -> gchararray:

      port2 -> gchararray:

      multicast-spec -> guint:

      prp -> gboolean:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        multicast_spec: int
        port1: str
        port2: str
        prp: bool
        name: str

    props: Props = ...
    def __init__(
        self,
        multicast_spec: int = ...,
        port1: str = ...,
        port2: str = ...,
        prp: bool = ...,
    ): ...
    def get_multicast_spec(self) -> int: ...
    def get_port1(self) -> str: ...
    def get_port2(self) -> str: ...
    def get_prp(self) -> bool: ...
    @classmethod
    def new(cls) -> SettingHsr: ...

class SettingHsrClass(GObject.GPointer): ...

class SettingIP4Config(SettingIPConfig):
    """
    :Constructors:

    ::

        SettingIP4Config(**properties)
        new() -> NM.Setting

    Object NMSettingIP4Config

    Properties from NMSettingIP4Config:
      dhcp-client-id -> gchararray:

      dhcp-fqdn -> gchararray:

      dhcp-vendor-class-identifier -> gchararray:

      link-local -> gint:


    Properties from NMSettingIPConfig:
      method -> gchararray:

      dns -> GStrv:

      dns-search -> GStrv:

      dns-options -> GStrv:

      dns-priority -> gint:

      addresses -> GPtrArray:

      gateway -> gchararray:

      routes -> GPtrArray:

      route-metric -> gint64:

      route-table -> guint:

      ignore-auto-routes -> gboolean:

      ignore-auto-dns -> gboolean:

      dhcp-hostname -> gchararray:

      dhcp-dscp -> gchararray:

      dhcp-hostname-flags -> guint:

      dhcp-send-hostname -> gboolean:

      never-default -> gboolean:

      may-fail -> gboolean:

      dad-timeout -> gint:

      dhcp-timeout -> gint:

      required-timeout -> gint:

      dhcp-iaid -> gchararray:

      dhcp-reject-servers -> GStrv:

      auto-route-ext-gw -> NMTernary:

      replace-local-rule -> NMTernary:

      dhcp-send-release -> NMTernary:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        dhcp_client_id: str
        dhcp_fqdn: str
        dhcp_vendor_class_identifier: str
        link_local: int
        addresses: list[IPAddress]
        auto_route_ext_gw: Ternary
        dad_timeout: int
        dhcp_dscp: str
        dhcp_hostname: str
        dhcp_hostname_flags: int
        dhcp_iaid: str
        dhcp_reject_servers: list[str]
        dhcp_send_hostname: bool
        dhcp_send_release: Ternary
        dhcp_timeout: int
        dns: list[str]
        dns_options: list[str]
        dns_priority: int
        dns_search: list[str]
        gateway: str
        ignore_auto_dns: bool
        ignore_auto_routes: bool
        may_fail: bool
        method: str
        never_default: bool
        replace_local_rule: Ternary
        required_timeout: int
        route_metric: int
        route_table: int
        routes: list[IPRoute]
        name: str

    props: Props = ...
    def __init__(
        self,
        dhcp_client_id: str = ...,
        dhcp_fqdn: str = ...,
        dhcp_vendor_class_identifier: str = ...,
        link_local: int = ...,
        addresses: Sequence[IPAddress] = ...,
        auto_route_ext_gw: Ternary = ...,
        dad_timeout: int = ...,
        dhcp_dscp: str = ...,
        dhcp_hostname: str = ...,
        dhcp_hostname_flags: int = ...,
        dhcp_iaid: str = ...,
        dhcp_reject_servers: Sequence[str] = ...,
        dhcp_send_hostname: bool = ...,
        dhcp_send_release: Ternary = ...,
        dhcp_timeout: int = ...,
        dns: Sequence[str] = ...,
        dns_options: Sequence[str] = ...,
        dns_priority: int = ...,
        dns_search: Sequence[str] = ...,
        gateway: str = ...,
        ignore_auto_dns: bool = ...,
        ignore_auto_routes: bool = ...,
        may_fail: bool = ...,
        method: str = ...,
        never_default: bool = ...,
        replace_local_rule: Ternary = ...,
        required_timeout: int = ...,
        route_metric: int = ...,
        route_table: int = ...,
        routes: Sequence[IPRoute] = ...,
    ): ...
    def get_dhcp_client_id(self) -> str: ...
    def get_dhcp_fqdn(self) -> str: ...
    def get_dhcp_vendor_class_identifier(self) -> str: ...
    def get_link_local(self) -> SettingIP4LinkLocal: ...
    @classmethod
    def new(cls) -> SettingIP4Config: ...

class SettingIP4ConfigClass(GObject.GPointer): ...

class SettingIP6Config(SettingIPConfig):
    """
    :Constructors:

    ::

        SettingIP6Config(**properties)
        new() -> NM.Setting

    Object NMSettingIP6Config

    Properties from NMSettingIP6Config:
      ip6-privacy -> NMSettingIP6ConfigPrivacy:

      temp-valid-lifetime -> gint:

      temp-preferred-lifetime -> gint:

      addr-gen-mode -> gint:

      token -> gchararray:

      dhcp-duid -> gchararray:

      ra-timeout -> gint:

      mtu -> guint:

      dhcp-pd-hint -> gchararray:


    Properties from NMSettingIPConfig:
      method -> gchararray:

      dns -> GStrv:

      dns-search -> GStrv:

      dns-options -> GStrv:

      dns-priority -> gint:

      addresses -> GPtrArray:

      gateway -> gchararray:

      routes -> GPtrArray:

      route-metric -> gint64:

      route-table -> guint:

      ignore-auto-routes -> gboolean:

      ignore-auto-dns -> gboolean:

      dhcp-hostname -> gchararray:

      dhcp-dscp -> gchararray:

      dhcp-hostname-flags -> guint:

      dhcp-send-hostname -> gboolean:

      never-default -> gboolean:

      may-fail -> gboolean:

      dad-timeout -> gint:

      dhcp-timeout -> gint:

      required-timeout -> gint:

      dhcp-iaid -> gchararray:

      dhcp-reject-servers -> GStrv:

      auto-route-ext-gw -> NMTernary:

      replace-local-rule -> NMTernary:

      dhcp-send-release -> NMTernary:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        addr_gen_mode: int
        dhcp_duid: str
        dhcp_pd_hint: str
        ip6_privacy: SettingIP6ConfigPrivacy
        mtu: int
        ra_timeout: int
        temp_preferred_lifetime: int
        temp_valid_lifetime: int
        token: str
        addresses: list[IPAddress]
        auto_route_ext_gw: Ternary
        dad_timeout: int
        dhcp_dscp: str
        dhcp_hostname: str
        dhcp_hostname_flags: int
        dhcp_iaid: str
        dhcp_reject_servers: list[str]
        dhcp_send_hostname: bool
        dhcp_send_release: Ternary
        dhcp_timeout: int
        dns: list[str]
        dns_options: list[str]
        dns_priority: int
        dns_search: list[str]
        gateway: str
        ignore_auto_dns: bool
        ignore_auto_routes: bool
        may_fail: bool
        method: str
        never_default: bool
        replace_local_rule: Ternary
        required_timeout: int
        route_metric: int
        route_table: int
        routes: list[IPRoute]
        name: str

    props: Props = ...
    def __init__(
        self,
        addr_gen_mode: int = ...,
        dhcp_duid: str = ...,
        dhcp_pd_hint: str = ...,
        ip6_privacy: SettingIP6ConfigPrivacy = ...,
        mtu: int = ...,
        ra_timeout: int = ...,
        temp_preferred_lifetime: int = ...,
        temp_valid_lifetime: int = ...,
        token: str = ...,
        addresses: Sequence[IPAddress] = ...,
        auto_route_ext_gw: Ternary = ...,
        dad_timeout: int = ...,
        dhcp_dscp: str = ...,
        dhcp_hostname: str = ...,
        dhcp_hostname_flags: int = ...,
        dhcp_iaid: str = ...,
        dhcp_reject_servers: Sequence[str] = ...,
        dhcp_send_hostname: bool = ...,
        dhcp_send_release: Ternary = ...,
        dhcp_timeout: int = ...,
        dns: Sequence[str] = ...,
        dns_options: Sequence[str] = ...,
        dns_priority: int = ...,
        dns_search: Sequence[str] = ...,
        gateway: str = ...,
        ignore_auto_dns: bool = ...,
        ignore_auto_routes: bool = ...,
        may_fail: bool = ...,
        method: str = ...,
        never_default: bool = ...,
        replace_local_rule: Ternary = ...,
        required_timeout: int = ...,
        route_metric: int = ...,
        route_table: int = ...,
        routes: Sequence[IPRoute] = ...,
    ): ...
    def get_addr_gen_mode(self) -> SettingIP6ConfigAddrGenMode: ...
    def get_dhcp_duid(self) -> str: ...
    def get_dhcp_pd_hint(self) -> str: ...
    def get_ip6_privacy(self) -> SettingIP6ConfigPrivacy: ...
    def get_mtu(self) -> int: ...
    def get_ra_timeout(self) -> int: ...
    def get_temp_preferred_lifetime(self) -> int: ...
    def get_temp_valid_lifetime(self) -> int: ...
    def get_token(self) -> str: ...
    @classmethod
    def new(cls) -> SettingIP6Config: ...

class SettingIP6ConfigClass(GObject.GPointer): ...

class SettingIPConfig(Setting):
    """
    :Constructors:

    ::

        SettingIPConfig(**properties)

    Object NMSettingIPConfig

    Properties from NMSettingIPConfig:
      method -> gchararray:

      dns -> GStrv:

      dns-search -> GStrv:

      dns-options -> GStrv:

      dns-priority -> gint:

      addresses -> GPtrArray:

      gateway -> gchararray:

      routes -> GPtrArray:

      route-metric -> gint64:

      route-table -> guint:

      ignore-auto-routes -> gboolean:

      ignore-auto-dns -> gboolean:

      dhcp-hostname -> gchararray:

      dhcp-dscp -> gchararray:

      dhcp-hostname-flags -> guint:

      dhcp-send-hostname -> gboolean:

      never-default -> gboolean:

      may-fail -> gboolean:

      dad-timeout -> gint:

      dhcp-timeout -> gint:

      required-timeout -> gint:

      dhcp-iaid -> gchararray:

      dhcp-reject-servers -> GStrv:

      auto-route-ext-gw -> NMTernary:

      replace-local-rule -> NMTernary:

      dhcp-send-release -> NMTernary:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        addresses: list[IPAddress]
        auto_route_ext_gw: Ternary
        dad_timeout: int
        dhcp_dscp: str
        dhcp_hostname: str
        dhcp_hostname_flags: int
        dhcp_iaid: str
        dhcp_reject_servers: list[str]
        dhcp_send_hostname: bool
        dhcp_send_release: Ternary
        dhcp_timeout: int
        dns: list[str]
        dns_options: list[str]
        dns_priority: int
        dns_search: list[str]
        gateway: str
        ignore_auto_dns: bool
        ignore_auto_routes: bool
        may_fail: bool
        method: str
        never_default: bool
        replace_local_rule: Ternary
        required_timeout: int
        route_metric: int
        route_table: int
        routes: list[IPRoute]
        name: str

    props: Props = ...
    def __init__(
        self,
        addresses: Sequence[IPAddress] = ...,
        auto_route_ext_gw: Ternary = ...,
        dad_timeout: int = ...,
        dhcp_dscp: str = ...,
        dhcp_hostname: str = ...,
        dhcp_hostname_flags: int = ...,
        dhcp_iaid: str = ...,
        dhcp_reject_servers: Sequence[str] = ...,
        dhcp_send_hostname: bool = ...,
        dhcp_send_release: Ternary = ...,
        dhcp_timeout: int = ...,
        dns: Sequence[str] = ...,
        dns_options: Sequence[str] = ...,
        dns_priority: int = ...,
        dns_search: Sequence[str] = ...,
        gateway: str = ...,
        ignore_auto_dns: bool = ...,
        ignore_auto_routes: bool = ...,
        may_fail: bool = ...,
        method: str = ...,
        never_default: bool = ...,
        replace_local_rule: Ternary = ...,
        required_timeout: int = ...,
        route_metric: int = ...,
        route_table: int = ...,
        routes: Sequence[IPRoute] = ...,
    ): ...
    def add_address(self, address: IPAddress) -> bool: ...
    def add_dhcp_reject_server(self, server: str) -> None: ...
    def add_dns(self, dns: str) -> bool: ...
    def add_dns_option(self, dns_option: str) -> bool: ...
    def add_dns_search(self, dns_search: str) -> bool: ...
    def add_route(self, route: IPRoute) -> bool: ...
    def add_routing_rule(self, routing_rule: IPRoutingRule) -> None: ...
    def clear_addresses(self) -> None: ...
    def clear_dhcp_reject_servers(self) -> None: ...
    def clear_dns(self) -> None: ...
    def clear_dns_options(self, is_set: bool) -> None: ...
    def clear_dns_searches(self) -> None: ...
    def clear_routes(self) -> None: ...
    def clear_routing_rules(self) -> None: ...
    def get_address(self, idx: int) -> IPAddress: ...
    def get_auto_route_ext_gw(self) -> Ternary: ...
    def get_dad_timeout(self) -> int: ...
    def get_dhcp_dscp(self) -> str: ...
    def get_dhcp_hostname(self) -> str: ...
    def get_dhcp_hostname_flags(self) -> DhcpHostnameFlags: ...
    def get_dhcp_iaid(self) -> str: ...
    def get_dhcp_reject_servers(self) -> list[str]: ...
    def get_dhcp_send_hostname(self) -> bool: ...
    def get_dhcp_send_release(self) -> Ternary: ...
    def get_dhcp_timeout(self) -> int: ...
    def get_dns(self, idx: int) -> str: ...
    def get_dns_option(self, idx: int) -> str: ...
    def get_dns_priority(self) -> int: ...
    def get_dns_search(self, idx: int) -> str: ...
    def get_gateway(self) -> str: ...
    def get_ignore_auto_dns(self) -> bool: ...
    def get_ignore_auto_routes(self) -> bool: ...
    def get_may_fail(self) -> bool: ...
    def get_method(self) -> str: ...
    def get_never_default(self) -> bool: ...
    def get_num_addresses(self) -> int: ...
    def get_num_dns(self) -> int: ...
    def get_num_dns_options(self) -> int: ...
    def get_num_dns_searches(self) -> int: ...
    def get_num_routes(self) -> int: ...
    def get_num_routing_rules(self) -> int: ...
    def get_replace_local_rule(self) -> Ternary: ...
    def get_required_timeout(self) -> int: ...
    def get_route(self, idx: int) -> IPRoute: ...
    def get_route_metric(self) -> int: ...
    def get_route_table(self) -> int: ...
    def get_routing_rule(self, idx: int) -> IPRoutingRule: ...
    def has_dns_options(self) -> bool: ...
    def remove_address(self, idx: int) -> None: ...
    def remove_address_by_value(self, address: IPAddress) -> bool: ...
    def remove_dhcp_reject_server(self, idx: int) -> None: ...
    def remove_dns(self, idx: int) -> None: ...
    def remove_dns_by_value(self, dns: str) -> bool: ...
    def remove_dns_option(self, idx: int) -> None: ...
    def remove_dns_option_by_value(self, dns_option: str) -> bool: ...
    def remove_dns_search(self, idx: int) -> None: ...
    def remove_dns_search_by_value(self, dns_search: str) -> bool: ...
    def remove_route(self, idx: int) -> None: ...
    def remove_route_by_value(self, route: IPRoute) -> bool: ...
    def remove_routing_rule(self, idx: int) -> None: ...

class SettingIPConfigClass(GObject.GPointer): ...

class SettingIPTunnel(Setting):
    """
    :Constructors:

    ::

        SettingIPTunnel(**properties)
        new() -> NM.Setting

    Object NMSettingIPTunnel

    Properties from NMSettingIPTunnel:
      parent -> gchararray:

      mode -> guint:

      local -> gchararray:

      remote -> gchararray:

      ttl -> guint:

      tos -> guint:

      path-mtu-discovery -> gboolean:

      input-key -> gchararray:

      output-key -> gchararray:

      encapsulation-limit -> guint:

      flow-label -> guint:

      fwmark -> guint:

      mtu -> guint:

      flags -> guint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        encapsulation_limit: int
        flags: int
        flow_label: int
        fwmark: int
        input_key: str
        local: str
        mode: int
        mtu: int
        output_key: str
        parent: str
        path_mtu_discovery: bool
        remote: str
        tos: int
        ttl: int
        name: str

    props: Props = ...
    def __init__(
        self,
        encapsulation_limit: int = ...,
        flags: int = ...,
        flow_label: int = ...,
        fwmark: int = ...,
        input_key: str = ...,
        local: str = ...,
        mode: int = ...,
        mtu: int = ...,
        output_key: str = ...,
        parent: str = ...,
        path_mtu_discovery: bool = ...,
        remote: str = ...,
        tos: int = ...,
        ttl: int = ...,
    ): ...
    def get_encapsulation_limit(self) -> int: ...
    def get_flags(self) -> IPTunnelFlags: ...
    def get_flow_label(self) -> int: ...
    def get_fwmark(self) -> int: ...
    def get_input_key(self) -> str: ...
    def get_local(self) -> str: ...
    def get_mode(self) -> IPTunnelMode: ...
    def get_mtu(self) -> int: ...
    def get_output_key(self) -> str: ...
    def get_parent(self) -> str: ...
    def get_path_mtu_discovery(self) -> bool: ...
    def get_remote(self) -> str: ...
    def get_tos(self) -> int: ...
    def get_ttl(self) -> int: ...
    @classmethod
    def new(cls) -> SettingIPTunnel: ...

class SettingIPTunnelClass(GObject.GPointer): ...

class SettingInfiniband(Setting):
    """
    :Constructors:

    ::

        SettingInfiniband(**properties)
        new() -> NM.Setting

    Object NMSettingInfiniband

    Properties from NMSettingInfiniband:
      mac-address -> gchararray:

      mtu -> guint:

      transport-mode -> gchararray:

      p-key -> gint:

      parent -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        mac_address: str
        mtu: int
        p_key: int
        parent: str
        transport_mode: str
        name: str

    props: Props = ...
    def __init__(
        self,
        mac_address: str = ...,
        mtu: int = ...,
        p_key: int = ...,
        parent: str = ...,
        transport_mode: str = ...,
    ): ...
    def get_mac_address(self) -> str: ...
    def get_mtu(self) -> int: ...
    def get_p_key(self) -> int: ...
    def get_parent(self) -> str: ...
    def get_transport_mode(self) -> str: ...
    def get_virtual_interface_name(self) -> str: ...
    @classmethod
    def new(cls) -> SettingInfiniband: ...

class SettingInfinibandClass(GObject.GPointer): ...

class SettingLink(Setting):
    """
    :Constructors:

    ::

        SettingLink(**properties)
        new() -> NM.Setting

    Object NMSettingLink

    Properties from NMSettingLink:
      tx-queue-length -> gint64:

      gso-max-size -> gint64:

      gso-max-segments -> gint64:

      gro-max-size -> gint64:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        gro_max_size: int
        gso_max_segments: int
        gso_max_size: int
        tx_queue_length: int
        name: str

    props: Props = ...
    def __init__(
        self,
        gro_max_size: int = ...,
        gso_max_segments: int = ...,
        gso_max_size: int = ...,
        tx_queue_length: int = ...,
    ): ...
    def get_gro_max_size(self) -> int: ...
    def get_gso_max_segments(self) -> int: ...
    def get_gso_max_size(self) -> int: ...
    def get_tx_queue_length(self) -> int: ...
    @classmethod
    def new(cls) -> SettingLink: ...

class SettingLinkClass(GObject.GPointer): ...

class SettingLoopback(Setting):
    """
    :Constructors:

    ::

        SettingLoopback(**properties)
        new() -> NM.Setting

    Object NMSettingLoopback

    Properties from NMSettingLoopback:
      mtu -> guint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        mtu: int
        name: str

    props: Props = ...
    def __init__(self, mtu: int = ...): ...
    def get_mtu(self) -> int: ...
    @classmethod
    def new(cls) -> SettingLoopback: ...

class SettingLoopbackClass(GObject.GPointer): ...

class SettingMacsec(Setting):
    """
    :Constructors:

    ::

        SettingMacsec(**properties)
        new() -> NM.Setting

    Object NMSettingMacsec

    Properties from NMSettingMacsec:
      parent -> gchararray:

      mode -> gint:

      encrypt -> gboolean:

      mka-cak -> gchararray:

      mka-cak-flags -> NMSettingSecretFlags:

      mka-ckn -> gchararray:

      port -> gint:

      validation -> gint:

      send-sci -> gboolean:

      offload -> gint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        encrypt: bool
        mka_cak: str
        mka_cak_flags: SettingSecretFlags
        mka_ckn: str
        mode: int
        offload: int
        parent: str
        port: int
        send_sci: bool
        validation: int
        name: str

    props: Props = ...
    def __init__(
        self,
        encrypt: bool = ...,
        mka_cak: str = ...,
        mka_cak_flags: SettingSecretFlags = ...,
        mka_ckn: str = ...,
        mode: int = ...,
        offload: int = ...,
        parent: str = ...,
        port: int = ...,
        send_sci: bool = ...,
        validation: int = ...,
    ): ...
    def get_encrypt(self) -> bool: ...
    def get_mka_cak(self) -> str: ...
    def get_mka_cak_flags(self) -> SettingSecretFlags: ...
    def get_mka_ckn(self) -> str: ...
    def get_mode(self) -> SettingMacsecMode: ...
    def get_offload(self) -> SettingMacsecOffload: ...
    def get_parent(self) -> str: ...
    def get_port(self) -> int: ...
    def get_send_sci(self) -> bool: ...
    def get_validation(self) -> SettingMacsecValidation: ...
    @classmethod
    def new(cls) -> SettingMacsec: ...

class SettingMacsecClass(GObject.GPointer): ...

class SettingMacvlan(Setting):
    """
    :Constructors:

    ::

        SettingMacvlan(**properties)
        new() -> NM.Setting

    Object NMSettingMacvlan

    Properties from NMSettingMacvlan:
      parent -> gchararray:

      mode -> guint:

      promiscuous -> gboolean:

      tap -> gboolean:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        mode: int
        parent: str
        promiscuous: bool
        tap: bool
        name: str

    props: Props = ...
    def __init__(
        self,
        mode: int = ...,
        parent: str = ...,
        promiscuous: bool = ...,
        tap: bool = ...,
    ): ...
    def get_mode(self) -> SettingMacvlanMode: ...
    def get_parent(self) -> str: ...
    def get_promiscuous(self) -> bool: ...
    def get_tap(self) -> bool: ...
    @classmethod
    def new(cls) -> SettingMacvlan: ...

class SettingMacvlanClass(GObject.GPointer): ...

class SettingMatch(Setting):
    """
    :Constructors:

    ::

        SettingMatch(**properties)
        new() -> NM.Setting

    Object NMSettingMatch

    Properties from NMSettingMatch:
      interface-name -> GStrv:

      kernel-command-line -> GStrv:

      driver -> GStrv:

      path -> GStrv:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        driver: list[str]
        interface_name: list[str]
        kernel_command_line: list[str]
        path: list[str]
        name: str

    props: Props = ...
    def __init__(
        self,
        driver: Sequence[str] = ...,
        interface_name: Sequence[str] = ...,
        kernel_command_line: Sequence[str] = ...,
        path: Sequence[str] = ...,
    ): ...
    def add_driver(self, driver: str) -> None: ...
    def add_interface_name(self, interface_name: str) -> None: ...
    def add_kernel_command_line(self, kernel_command_line: str) -> None: ...
    def add_path(self, path: str) -> None: ...
    def clear_drivers(self) -> None: ...
    def clear_interface_names(self) -> None: ...
    def clear_kernel_command_lines(self) -> None: ...
    def clear_paths(self) -> None: ...
    def get_driver(self, idx: int) -> str: ...
    def get_drivers(self) -> list[str]: ...
    def get_interface_name(self, idx: int) -> str: ...
    def get_interface_names(self) -> list[str]: ...
    def get_kernel_command_line(self, idx: int) -> str: ...
    def get_kernel_command_lines(self) -> list[str]: ...
    def get_num_drivers(self) -> int: ...
    def get_num_interface_names(self) -> int: ...
    def get_num_kernel_command_lines(self) -> int: ...
    def get_num_paths(self) -> int: ...
    def get_path(self, idx: int) -> str: ...
    def get_paths(self) -> list[str]: ...
    @classmethod
    def new(cls) -> SettingMatch: ...
    def remove_driver(self, idx: int) -> None: ...
    def remove_driver_by_value(self, driver: str) -> bool: ...
    def remove_interface_name(self, idx: int) -> None: ...
    def remove_interface_name_by_value(self, interface_name: str) -> bool: ...
    def remove_kernel_command_line(self, idx: int) -> None: ...
    def remove_kernel_command_line_by_value(self, kernel_command_line: str) -> bool: ...
    def remove_path(self, idx: int) -> None: ...
    def remove_path_by_value(self, path: str) -> bool: ...

class SettingMatchClass(GObject.GPointer): ...

class SettingOlpcMesh(Setting):
    """
    :Constructors:

    ::

        SettingOlpcMesh(**properties)
        new() -> NM.Setting

    Object NMSettingOlpcMesh

    Properties from NMSettingOlpcMesh:
      ssid -> GBytes:

      channel -> guint:

      dhcp-anycast-address -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        channel: int
        dhcp_anycast_address: str
        ssid: GLib.Bytes
        name: str

    props: Props = ...
    def __init__(
        self,
        channel: int = ...,
        dhcp_anycast_address: str = ...,
        ssid: GLib.Bytes = ...,
    ): ...
    def get_channel(self) -> int: ...
    def get_dhcp_anycast_address(self) -> str: ...
    def get_ssid(self) -> GLib.Bytes: ...
    @classmethod
    def new(cls) -> SettingOlpcMesh: ...

class SettingOlpcMeshClass(GObject.GPointer): ...

class SettingOvsBridge(Setting):
    """
    :Constructors:

    ::

        SettingOvsBridge(**properties)
        new() -> NM.Setting

    Object NMSettingOvsBridge

    Properties from NMSettingOvsBridge:
      fail-mode -> gchararray:

      mcast-snooping-enable -> gboolean:

      rstp-enable -> gboolean:

      stp-enable -> gboolean:

      datapath-type -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        datapath_type: str
        fail_mode: str
        mcast_snooping_enable: bool
        rstp_enable: bool
        stp_enable: bool
        name: str

    props: Props = ...
    def __init__(
        self,
        datapath_type: str = ...,
        fail_mode: str = ...,
        mcast_snooping_enable: bool = ...,
        rstp_enable: bool = ...,
        stp_enable: bool = ...,
    ): ...
    def get_datapath_type(self) -> str: ...
    def get_fail_mode(self) -> str: ...
    def get_mcast_snooping_enable(self) -> bool: ...
    def get_rstp_enable(self) -> bool: ...
    def get_stp_enable(self) -> bool: ...
    @classmethod
    def new(cls) -> SettingOvsBridge: ...

class SettingOvsBridgeClass(GObject.GPointer): ...

class SettingOvsDpdk(Setting):
    """
    :Constructors:

    ::

        SettingOvsDpdk(**properties)
        new() -> NM.Setting

    Object NMSettingOvsDpdk

    Properties from NMSettingOvsDpdk:
      devargs -> gchararray:

      n-rxq -> guint:

      n-rxq-desc -> guint:

      n-txq-desc -> guint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        devargs: str
        n_rxq: int
        n_rxq_desc: int
        n_txq_desc: int
        name: str

    props: Props = ...
    def __init__(
        self,
        devargs: str = ...,
        n_rxq: int = ...,
        n_rxq_desc: int = ...,
        n_txq_desc: int = ...,
    ): ...
    def get_devargs(self) -> str: ...
    def get_n_rxq(self) -> int: ...
    def get_n_rxq_desc(self) -> int: ...
    def get_n_txq_desc(self) -> int: ...
    @classmethod
    def new(cls) -> SettingOvsDpdk: ...

class SettingOvsDpdkClass(GObject.GPointer): ...

class SettingOvsExternalIDs(Setting):
    """
    :Constructors:

    ::

        SettingOvsExternalIDs(**properties)
        new() -> NM.SettingOvsExternalIDs

    Object NMSettingOvsExternalIDs

    Properties from NMSettingOvsExternalIDs:
      data -> GHashTable:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        data: dict[str, str]
        name: str

    props: Props = ...
    def __init__(self, data: dict[str, str] = ...): ...
    @staticmethod
    def check_key(key: str | None = None) -> bool: ...
    @staticmethod
    def check_val(val: str | None = None) -> bool: ...
    def get_data(self, key: str) -> str: ...
    def get_data_keys(self) -> list[str]: ...
    @classmethod
    def new(cls) -> SettingOvsExternalIDs: ...
    def set_data(self, key: str, val: str | None = None) -> None: ...

class SettingOvsExternalIDsClass(GObject.GPointer): ...

class SettingOvsInterface(Setting):
    """
    :Constructors:

    ::

        SettingOvsInterface(**properties)
        new() -> NM.Setting

    Object NMSettingOvsInterface

    Properties from NMSettingOvsInterface:
      type -> gchararray:

      ofport-request -> guint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        ofport_request: int
        type: str
        name: str

    props: Props = ...
    def __init__(self, ofport_request: int = ..., type: str = ...): ...
    def get_interface_type(self) -> str: ...
    def get_ofport_request(self) -> int: ...
    @classmethod
    def new(cls) -> SettingOvsInterface: ...

class SettingOvsInterfaceClass(GObject.GPointer): ...

class SettingOvsOtherConfig(Setting):
    """
    :Constructors:

    ::

        SettingOvsOtherConfig(**properties)
        new() -> NM.SettingOvsOtherConfig

    Object NMSettingOvsOtherConfig

    Properties from NMSettingOvsOtherConfig:
      data -> GHashTable:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        data: dict[str, str]
        name: str

    props: Props = ...
    def __init__(self, data: dict[str, str] = ...): ...
    def get_data(self, key: str) -> str: ...
    def get_data_keys(self) -> list[str]: ...
    @classmethod
    def new(cls) -> SettingOvsOtherConfig: ...
    def set_data(self, key: str, val: str | None = None) -> None: ...

class SettingOvsOtherConfigClass(GObject.GPointer): ...

class SettingOvsPatch(Setting):
    """
    :Constructors:

    ::

        SettingOvsPatch(**properties)
        new() -> NM.Setting

    Object NMSettingOvsPatch

    Properties from NMSettingOvsPatch:
      peer -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        peer: str
        name: str

    props: Props = ...
    def __init__(self, peer: str = ...): ...
    def get_peer(self) -> str: ...
    @classmethod
    def new(cls) -> SettingOvsPatch: ...

class SettingOvsPatchClass(GObject.GPointer): ...

class SettingOvsPort(Setting):
    """
    :Constructors:

    ::

        SettingOvsPort(**properties)
        new() -> NM.Setting

    Object NMSettingOvsPort

    Properties from NMSettingOvsPort:
      vlan-mode -> gchararray:

      tag -> guint:

      trunks -> GPtrArray:

      lacp -> gchararray:

      bond-mode -> gchararray:

      bond-updelay -> guint:

      bond-downdelay -> guint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        bond_downdelay: int
        bond_mode: str
        bond_updelay: int
        lacp: str
        tag: int
        trunks: list[Range]
        vlan_mode: str
        name: str

    props: Props = ...
    def __init__(
        self,
        bond_downdelay: int = ...,
        bond_mode: str = ...,
        bond_updelay: int = ...,
        lacp: str = ...,
        tag: int = ...,
        trunks: Sequence[Range] = ...,
        vlan_mode: str = ...,
    ): ...
    def add_trunk(self, trunk: Range) -> None: ...
    def clear_trunks(self) -> None: ...
    def get_bond_downdelay(self) -> int: ...
    def get_bond_mode(self) -> str: ...
    def get_bond_updelay(self) -> int: ...
    def get_lacp(self) -> str: ...
    def get_num_trunks(self) -> int: ...
    def get_tag(self) -> int: ...
    def get_trunk(self, idx: int) -> Range: ...
    def get_vlan_mode(self) -> str: ...
    @classmethod
    def new(cls) -> SettingOvsPort: ...
    def remove_trunk(self, idx: int) -> None: ...
    def remove_trunk_by_value(self, start: int, end: int) -> bool: ...

class SettingOvsPortClass(GObject.GPointer): ...

class SettingPpp(Setting):
    """
    :Constructors:

    ::

        SettingPpp(**properties)
        new() -> NM.Setting

    Object NMSettingPpp

    Properties from NMSettingPpp:
      noauth -> gboolean:

      refuse-eap -> gboolean:

      refuse-pap -> gboolean:

      refuse-chap -> gboolean:

      refuse-mschap -> gboolean:

      refuse-mschapv2 -> gboolean:

      nobsdcomp -> gboolean:

      nodeflate -> gboolean:

      no-vj-comp -> gboolean:

      require-mppe -> gboolean:

      require-mppe-128 -> gboolean:

      mppe-stateful -> gboolean:

      crtscts -> gboolean:

      baud -> guint:

      mru -> guint:

      mtu -> guint:

      lcp-echo-failure -> guint:

      lcp-echo-interval -> guint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        baud: int
        crtscts: bool
        lcp_echo_failure: int
        lcp_echo_interval: int
        mppe_stateful: bool
        mru: int
        mtu: int
        no_vj_comp: bool
        noauth: bool
        nobsdcomp: bool
        nodeflate: bool
        refuse_chap: bool
        refuse_eap: bool
        refuse_mschap: bool
        refuse_mschapv2: bool
        refuse_pap: bool
        require_mppe: bool
        require_mppe_128: bool
        name: str

    props: Props = ...
    def __init__(
        self,
        baud: int = ...,
        crtscts: bool = ...,
        lcp_echo_failure: int = ...,
        lcp_echo_interval: int = ...,
        mppe_stateful: bool = ...,
        mru: int = ...,
        mtu: int = ...,
        no_vj_comp: bool = ...,
        noauth: bool = ...,
        nobsdcomp: bool = ...,
        nodeflate: bool = ...,
        refuse_chap: bool = ...,
        refuse_eap: bool = ...,
        refuse_mschap: bool = ...,
        refuse_mschapv2: bool = ...,
        refuse_pap: bool = ...,
        require_mppe: bool = ...,
        require_mppe_128: bool = ...,
    ): ...
    def get_baud(self) -> int: ...
    def get_crtscts(self) -> bool: ...
    def get_lcp_echo_failure(self) -> int: ...
    def get_lcp_echo_interval(self) -> int: ...
    def get_mppe_stateful(self) -> bool: ...
    def get_mru(self) -> int: ...
    def get_mtu(self) -> int: ...
    def get_no_vj_comp(self) -> bool: ...
    def get_noauth(self) -> bool: ...
    def get_nobsdcomp(self) -> bool: ...
    def get_nodeflate(self) -> bool: ...
    def get_refuse_chap(self) -> bool: ...
    def get_refuse_eap(self) -> bool: ...
    def get_refuse_mschap(self) -> bool: ...
    def get_refuse_mschapv2(self) -> bool: ...
    def get_refuse_pap(self) -> bool: ...
    def get_require_mppe(self) -> bool: ...
    def get_require_mppe_128(self) -> bool: ...
    @classmethod
    def new(cls) -> SettingPpp: ...

class SettingPppClass(GObject.GPointer): ...

class SettingPppoe(Setting):
    """
    :Constructors:

    ::

        SettingPppoe(**properties)
        new() -> NM.Setting

    Object NMSettingPppoe

    Properties from NMSettingPppoe:
      parent -> gchararray:

      service -> gchararray:

      username -> gchararray:

      password -> gchararray:

      password-flags -> NMSettingSecretFlags:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        parent: str
        password: str
        password_flags: SettingSecretFlags
        service: str
        username: str
        name: str

    props: Props = ...
    def __init__(
        self,
        parent: str = ...,
        password: str = ...,
        password_flags: SettingSecretFlags = ...,
        service: str = ...,
        username: str = ...,
    ): ...
    def get_parent(self) -> str: ...
    def get_password(self) -> str: ...
    def get_password_flags(self) -> SettingSecretFlags: ...
    def get_service(self) -> str: ...
    def get_username(self) -> str: ...
    @classmethod
    def new(cls) -> SettingPppoe: ...

class SettingPppoeClass(GObject.GPointer): ...

class SettingProxy(Setting):
    """
    :Constructors:

    ::

        SettingProxy(**properties)
        new() -> NM.Setting

    Object NMSettingProxy

    Properties from NMSettingProxy:
      method -> gint:

      browser-only -> gboolean:

      pac-url -> gchararray:

      pac-script -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        browser_only: bool
        method: int
        pac_script: str
        pac_url: str
        name: str

    props: Props = ...
    def __init__(
        self,
        browser_only: bool = ...,
        method: int = ...,
        pac_script: str = ...,
        pac_url: str = ...,
    ): ...
    def get_browser_only(self) -> bool: ...
    def get_method(self) -> SettingProxyMethod: ...
    def get_pac_script(self) -> str: ...
    def get_pac_url(self) -> str: ...
    @classmethod
    def new(cls) -> SettingProxy: ...

class SettingProxyClass(GObject.GPointer): ...

class SettingSerial(Setting):
    """
    :Constructors:

    ::

        SettingSerial(**properties)
        new() -> NM.Setting

    Object NMSettingSerial

    Properties from NMSettingSerial:
      baud -> guint:

      bits -> guint:

      parity -> NMSettingSerialParity:

      stopbits -> guint:

      send-delay -> guint64:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        baud: int
        bits: int
        parity: SettingSerialParity
        send_delay: int
        stopbits: int
        name: str

    props: Props = ...
    def __init__(
        self,
        baud: int = ...,
        bits: int = ...,
        parity: SettingSerialParity = ...,
        send_delay: int = ...,
        stopbits: int = ...,
    ): ...
    def get_baud(self) -> int: ...
    def get_bits(self) -> int: ...
    def get_parity(self) -> SettingSerialParity: ...
    def get_send_delay(self) -> int: ...
    def get_stopbits(self) -> int: ...
    @classmethod
    def new(cls) -> SettingSerial: ...

class SettingSerialClass(GObject.GPointer): ...

class SettingSriov(Setting):
    """
    :Constructors:

    ::

        SettingSriov(**properties)
        new() -> NM.Setting

    Object NMSettingSriov

    Properties from NMSettingSriov:
      total-vfs -> guint:

      vfs -> GPtrArray:

      autoprobe-drivers -> NMTernary:

      eswitch-mode -> gint:

      eswitch-inline-mode -> gint:

      eswitch-encap-mode -> gint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        autoprobe_drivers: Ternary
        eswitch_encap_mode: int
        eswitch_inline_mode: int
        eswitch_mode: int
        total_vfs: int
        vfs: list[SriovVF]
        name: str

    props: Props = ...
    def __init__(
        self,
        autoprobe_drivers: Ternary = ...,
        eswitch_encap_mode: int = ...,
        eswitch_inline_mode: int = ...,
        eswitch_mode: int = ...,
        total_vfs: int = ...,
        vfs: Sequence[SriovVF] = ...,
    ): ...
    def add_vf(self, vf: SriovVF) -> None: ...
    def clear_vfs(self) -> None: ...
    def get_autoprobe_drivers(self) -> Ternary: ...
    def get_eswitch_encap_mode(self) -> SriovEswitchEncapMode: ...
    def get_eswitch_inline_mode(self) -> SriovEswitchInlineMode: ...
    def get_eswitch_mode(self) -> SriovEswitchMode: ...
    def get_num_vfs(self) -> int: ...
    def get_total_vfs(self) -> int: ...
    def get_vf(self, idx: int) -> SriovVF: ...
    @classmethod
    def new(cls) -> SettingSriov: ...
    def remove_vf(self, idx: int) -> None: ...
    def remove_vf_by_index(self, index: int) -> bool: ...

class SettingSriovClass(GObject.GPointer): ...

class SettingTCConfig(Setting):
    """
    :Constructors:

    ::

        SettingTCConfig(**properties)
        new() -> NM.Setting

    Object NMSettingTCConfig

    Properties from NMSettingTCConfig:
      qdiscs -> GPtrArray:

      tfilters -> GPtrArray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        qdiscs: list[TCQdisc]
        tfilters: list[TCTfilter]
        name: str

    props: Props = ...
    def __init__(
        self, qdiscs: Sequence[TCQdisc] = ..., tfilters: Sequence[TCTfilter] = ...
    ): ...
    def add_qdisc(self, qdisc: TCQdisc) -> bool: ...
    def add_tfilter(self, tfilter: TCTfilter) -> bool: ...
    def clear_qdiscs(self) -> None: ...
    def clear_tfilters(self) -> None: ...
    def get_num_qdiscs(self) -> int: ...
    def get_num_tfilters(self) -> int: ...
    def get_qdisc(self, idx: int) -> TCQdisc: ...
    def get_tfilter(self, idx: int) -> TCTfilter: ...
    @classmethod
    def new(cls) -> SettingTCConfig: ...
    def remove_qdisc(self, idx: int) -> None: ...
    def remove_qdisc_by_value(self, qdisc: TCQdisc) -> bool: ...
    def remove_tfilter(self, idx: int) -> None: ...
    def remove_tfilter_by_value(self, tfilter: TCTfilter) -> bool: ...

class SettingTCConfigClass(GObject.GPointer): ...

class SettingTeam(Setting):
    """
    :Constructors:

    ::

        SettingTeam(**properties)
        new() -> NM.Setting

    Object NMSettingTeam

    Properties from NMSettingTeam:
      config -> gchararray:

      link-watchers -> GPtrArray:

      notify-peers-count -> gint:

      notify-peers-interval -> gint:

      mcast-rejoin-count -> gint:

      mcast-rejoin-interval -> gint:

      runner -> gchararray:

      runner-hwaddr-policy -> gchararray:

      runner-tx-hash -> GStrv:

      runner-tx-balancer -> gchararray:

      runner-tx-balancer-interval -> gint:

      runner-active -> gboolean:

      runner-fast-rate -> gboolean:

      runner-sys-prio -> gint:

      runner-min-ports -> gint:

      runner-agg-select-policy -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        config: str
        link_watchers: list[TeamLinkWatcher]
        mcast_rejoin_count: int
        mcast_rejoin_interval: int
        notify_peers_count: int
        notify_peers_interval: int
        runner: str
        runner_active: bool
        runner_agg_select_policy: str
        runner_fast_rate: bool
        runner_hwaddr_policy: str
        runner_min_ports: int
        runner_sys_prio: int
        runner_tx_balancer: str
        runner_tx_balancer_interval: int
        runner_tx_hash: list[str]
        name: str

    props: Props = ...
    def __init__(
        self,
        config: str = ...,
        link_watchers: Sequence[TeamLinkWatcher] = ...,
        mcast_rejoin_count: int = ...,
        mcast_rejoin_interval: int = ...,
        notify_peers_count: int = ...,
        notify_peers_interval: int = ...,
        runner: str = ...,
        runner_active: bool = ...,
        runner_agg_select_policy: str = ...,
        runner_fast_rate: bool = ...,
        runner_hwaddr_policy: str = ...,
        runner_min_ports: int = ...,
        runner_sys_prio: int = ...,
        runner_tx_balancer: str = ...,
        runner_tx_balancer_interval: int = ...,
        runner_tx_hash: Sequence[str] = ...,
    ): ...
    def add_link_watcher(self, link_watcher: TeamLinkWatcher) -> bool: ...
    def add_runner_tx_hash(self, txhash: str) -> bool: ...
    def clear_link_watchers(self) -> None: ...
    def get_config(self) -> str: ...
    def get_link_watcher(self, idx: int) -> TeamLinkWatcher: ...
    def get_mcast_rejoin_count(self) -> int: ...
    def get_mcast_rejoin_interval(self) -> int: ...
    def get_notify_peers_count(self) -> int: ...
    def get_notify_peers_interval(self) -> int: ...
    def get_num_link_watchers(self) -> int: ...
    def get_num_runner_tx_hash(self) -> int: ...
    def get_runner(self) -> str: ...
    def get_runner_active(self) -> bool: ...
    def get_runner_agg_select_policy(self) -> str: ...
    def get_runner_fast_rate(self) -> bool: ...
    def get_runner_hwaddr_policy(self) -> str: ...
    def get_runner_min_ports(self) -> int: ...
    def get_runner_sys_prio(self) -> int: ...
    def get_runner_tx_balancer(self) -> str: ...
    def get_runner_tx_balancer_interval(self) -> int: ...
    def get_runner_tx_hash(self, idx: int) -> str: ...
    @classmethod
    def new(cls) -> SettingTeam: ...
    def remove_link_watcher(self, idx: int) -> None: ...
    def remove_link_watcher_by_value(self, link_watcher: TeamLinkWatcher) -> bool: ...
    def remove_runner_tx_hash(self, idx: int) -> None: ...
    def remove_runner_tx_hash_by_value(self, txhash: str) -> bool: ...

class SettingTeamClass(GObject.GPointer): ...

class SettingTeamPort(Setting):
    """
    :Constructors:

    ::

        SettingTeamPort(**properties)
        new() -> NM.Setting

    Object NMSettingTeamPort

    Properties from NMSettingTeamPort:
      config -> gchararray:

      link-watchers -> GPtrArray:

      queue-id -> gint:

      prio -> gint:

      sticky -> gboolean:

      lacp-prio -> gint:

      lacp-key -> gint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        config: str
        lacp_key: int
        lacp_prio: int
        link_watchers: list[TeamLinkWatcher]
        prio: int
        queue_id: int
        sticky: bool
        name: str

    props: Props = ...
    def __init__(
        self,
        config: str = ...,
        lacp_key: int = ...,
        lacp_prio: int = ...,
        link_watchers: Sequence[TeamLinkWatcher] = ...,
        prio: int = ...,
        queue_id: int = ...,
        sticky: bool = ...,
    ): ...
    def add_link_watcher(self, link_watcher: TeamLinkWatcher) -> bool: ...
    def clear_link_watchers(self) -> None: ...
    def get_config(self) -> str: ...
    def get_lacp_key(self) -> int: ...
    def get_lacp_prio(self) -> int: ...
    def get_link_watcher(self, idx: int) -> TeamLinkWatcher: ...
    def get_num_link_watchers(self) -> int: ...
    def get_prio(self) -> int: ...
    def get_queue_id(self) -> int: ...
    def get_sticky(self) -> bool: ...
    @classmethod
    def new(cls) -> SettingTeamPort: ...
    def remove_link_watcher(self, idx: int) -> None: ...
    def remove_link_watcher_by_value(self, link_watcher: TeamLinkWatcher) -> bool: ...

class SettingTeamPortClass(GObject.GPointer): ...

class SettingTun(Setting):
    """
    :Constructors:

    ::

        SettingTun(**properties)
        new() -> NM.Setting

    Object NMSettingTun

    Properties from NMSettingTun:
      mode -> guint:

      owner -> gchararray:

      group -> gchararray:

      pi -> gboolean:

      vnet-hdr -> gboolean:

      multi-queue -> gboolean:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        group: str
        mode: int
        multi_queue: bool
        owner: str
        pi: bool
        vnet_hdr: bool
        name: str

    props: Props = ...
    def __init__(
        self,
        group: str = ...,
        mode: int = ...,
        multi_queue: bool = ...,
        owner: str = ...,
        pi: bool = ...,
        vnet_hdr: bool = ...,
    ): ...
    def get_group(self) -> str: ...
    def get_mode(self) -> SettingTunMode: ...
    def get_multi_queue(self) -> bool: ...
    def get_owner(self) -> str: ...
    def get_pi(self) -> bool: ...
    def get_vnet_hdr(self) -> bool: ...
    @classmethod
    def new(cls) -> SettingTun: ...

class SettingTunClass(GObject.GPointer): ...

class SettingUser(Setting):
    """
    :Constructors:

    ::

        SettingUser(**properties)
        new() -> NM.Setting

    Object NMSettingUser

    Properties from NMSettingUser:
      data -> GHashTable:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        data: dict[str, str]
        name: str

    props: Props = ...
    def __init__(self, data: dict[str, str] = ...): ...
    @staticmethod
    def check_key(key: str) -> bool: ...
    @staticmethod
    def check_val(val: str) -> bool: ...
    def get_data(self, key: str) -> str: ...
    def get_keys(self) -> list[str]: ...
    @classmethod
    def new(cls) -> SettingUser: ...
    def set_data(self, key: str, val: str | None = None) -> bool: ...

class SettingUserClass(GObject.GPointer): ...

class SettingVeth(Setting):
    """
    :Constructors:

    ::

        SettingVeth(**properties)
        new() -> NM.Setting

    Object NMSettingVeth

    Properties from NMSettingVeth:
      peer -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        peer: str
        name: str

    props: Props = ...
    def __init__(self, peer: str = ...): ...
    def get_peer(self) -> str: ...
    @classmethod
    def new(cls) -> SettingVeth: ...

class SettingVethClass(GObject.GPointer): ...

class SettingVlan(Setting):
    """
    :Constructors:

    ::

        SettingVlan(**properties)
        new() -> NM.Setting

    Object NMSettingVlan

    Properties from NMSettingVlan:
      parent -> gchararray:

      id -> guint:

      flags -> NMVlanFlags:

      protocol -> gchararray:

      ingress-priority-map -> GStrv:

      egress-priority-map -> GStrv:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        egress_priority_map: list[str]
        flags: VlanFlags
        id: int
        ingress_priority_map: list[str]
        parent: str
        protocol: str
        name: str

    props: Props = ...
    def __init__(
        self,
        egress_priority_map: Sequence[str] = ...,
        flags: VlanFlags = ...,
        id: int = ...,
        ingress_priority_map: Sequence[str] = ...,
        parent: str = ...,
        protocol: str = ...,
    ): ...
    def add_priority(self, map: VlanPriorityMap, from_: int, to: int) -> bool: ...
    def add_priority_str(self, map: VlanPriorityMap, str: str) -> bool: ...
    def clear_priorities(self, map: VlanPriorityMap) -> None: ...
    def get_flags(self) -> int: ...
    def get_id(self) -> int: ...
    def get_num_priorities(self, map: VlanPriorityMap) -> int: ...
    def get_parent(self) -> str: ...
    def get_priority(self, map: VlanPriorityMap, idx: int) -> tuple[bool, int, int]: ...
    def get_protocol(self) -> str: ...
    @classmethod
    def new(cls) -> SettingVlan: ...
    def remove_priority(self, map: VlanPriorityMap, idx: int) -> None: ...
    def remove_priority_by_value(
        self, map: VlanPriorityMap, from_: int, to: int
    ) -> bool: ...
    def remove_priority_str_by_value(self, map: VlanPriorityMap, str: str) -> bool: ...

class SettingVlanClass(GObject.GPointer): ...

class SettingVpn(Setting):
    """
    :Constructors:

    ::

        SettingVpn(**properties)
        new() -> NM.Setting

    Object NMSettingVpn

    Properties from NMSettingVpn:
      service-type -> gchararray:

      user-name -> gchararray:

      persistent -> gboolean:

      data -> GHashTable:

      secrets -> GHashTable:

      timeout -> guint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        data: dict[str, str]
        persistent: bool
        secrets: dict[str, str]
        service_type: str
        timeout: int
        user_name: str
        name: str

    props: Props = ...
    def __init__(
        self,
        data: dict[str, str] = ...,
        persistent: bool = ...,
        secrets: dict[str, str] = ...,
        service_type: str = ...,
        timeout: int = ...,
        user_name: str = ...,
    ): ...
    def add_data_item(self, key: str, item: str | None = None) -> None: ...
    def add_secret(self, key: str, secret: str | None = None) -> None: ...
    def foreach_data_item(self, func: Callable[..., None], *user_data: Any) -> None: ...
    def foreach_secret(self, func: Callable[..., None], *user_data: Any) -> None: ...
    def get_data_item(self, key: str) -> str: ...
    def get_data_keys(self) -> list[str] | None: ...
    def get_num_data_items(self) -> int: ...
    def get_num_secrets(self) -> int: ...
    def get_persistent(self) -> bool: ...
    def get_secret(self, key: str) -> str: ...
    def get_secret_keys(self) -> list[str] | None: ...
    def get_service_type(self) -> str: ...
    def get_timeout(self) -> int: ...
    def get_user_name(self) -> str: ...
    @classmethod
    def new(cls) -> SettingVpn: ...
    def remove_data_item(self, key: str) -> bool: ...
    def remove_secret(self, key: str) -> bool: ...

class SettingVpnClass(GObject.GPointer): ...

class SettingVrf(Setting):
    """
    :Constructors:

    ::

        SettingVrf(**properties)
        new() -> NM.Setting

    Object NMSettingVrf

    Properties from NMSettingVrf:
      table -> guint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        table: int
        name: str

    props: Props = ...
    def __init__(self, table: int = ...): ...
    def get_table(self) -> int: ...
    @classmethod
    def new(cls) -> SettingVrf: ...

class SettingVrfClass(GObject.GPointer): ...

class SettingVxlan(Setting):
    """
    :Constructors:

    ::

        SettingVxlan(**properties)
        new() -> NM.Setting

    Object NMSettingVxlan

    Properties from NMSettingVxlan:
      parent -> gchararray:

      id -> guint:

      local -> gchararray:

      remote -> gchararray:

      source-port-min -> guint:

      source-port-max -> guint:

      destination-port -> guint:

      tos -> guint:

      ttl -> guint:

      ageing -> guint:

      limit -> guint:

      learning -> gboolean:

      proxy -> gboolean:

      rsc -> gboolean:

      l2-miss -> gboolean:

      l3-miss -> gboolean:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        ageing: int
        destination_port: int
        id: int
        l2_miss: bool
        l3_miss: bool
        learning: bool
        limit: int
        local: str
        parent: str
        proxy: bool
        remote: str
        rsc: bool
        source_port_max: int
        source_port_min: int
        tos: int
        ttl: int
        name: str

    props: Props = ...
    def __init__(
        self,
        ageing: int = ...,
        destination_port: int = ...,
        id: int = ...,
        l2_miss: bool = ...,
        l3_miss: bool = ...,
        learning: bool = ...,
        limit: int = ...,
        local: str = ...,
        parent: str = ...,
        proxy: bool = ...,
        remote: str = ...,
        rsc: bool = ...,
        source_port_max: int = ...,
        source_port_min: int = ...,
        tos: int = ...,
        ttl: int = ...,
    ): ...
    def get_ageing(self) -> int: ...
    def get_destination_port(self) -> int: ...
    def get_id(self) -> int: ...
    def get_l2_miss(self) -> bool: ...
    def get_l3_miss(self) -> bool: ...
    def get_learning(self) -> bool: ...
    def get_limit(self) -> int: ...
    def get_local(self) -> str: ...
    def get_parent(self) -> str: ...
    def get_proxy(self) -> bool: ...
    def get_remote(self) -> str: ...
    def get_rsc(self) -> bool: ...
    def get_source_port_max(self) -> int: ...
    def get_source_port_min(self) -> int: ...
    def get_tos(self) -> int: ...
    def get_ttl(self) -> int: ...
    @classmethod
    def new(cls) -> SettingVxlan: ...

class SettingVxlanClass(GObject.GPointer): ...

class SettingWifiP2P(Setting):
    """
    :Constructors:

    ::

        SettingWifiP2P(**properties)
        new() -> NM.Setting

    Object NMSettingWifiP2P

    Properties from NMSettingWifiP2P:
      peer -> gchararray:

      wps-method -> guint:

      wfd-ies -> GBytes:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        peer: str
        wfd_ies: GLib.Bytes
        wps_method: int
        name: str

    props: Props = ...
    def __init__(
        self, peer: str = ..., wfd_ies: GLib.Bytes = ..., wps_method: int = ...
    ): ...
    def get_peer(self) -> str: ...
    def get_wfd_ies(self) -> GLib.Bytes: ...
    def get_wps_method(self) -> SettingWirelessSecurityWpsMethod: ...
    @classmethod
    def new(cls) -> SettingWifiP2P: ...

class SettingWifiP2PClass(GObject.GPointer): ...

class SettingWimax(Setting):
    """
    :Constructors:

    ::

        SettingWimax(**properties)
        new() -> NM.Setting

    Object NMSettingWimax

    Properties from NMSettingWimax:
      network-name -> gchararray:

      mac-address -> gchararray:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        mac_address: str
        network_name: str
        name: str

    props: Props = ...
    def __init__(self, mac_address: str = ..., network_name: str = ...): ...
    def get_mac_address(self) -> str: ...
    def get_network_name(self) -> str: ...
    @classmethod
    def new(cls) -> SettingWimax: ...

class SettingWimaxClass(GObject.GPointer): ...

class SettingWireGuard(Setting):
    """
    :Constructors:

    ::

        SettingWireGuard(**properties)
        new() -> NM.Setting

    Object NMSettingWireGuard

    Properties from NMSettingWireGuard:
      fwmark -> guint:

      ip4-auto-default-route -> NMTernary:

      ip6-auto-default-route -> NMTernary:

      listen-port -> guint:

      mtu -> guint:

      peer-routes -> gboolean:

      private-key -> gchararray:

      private-key-flags -> NMSettingSecretFlags:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        fwmark: int
        ip4_auto_default_route: Ternary
        ip6_auto_default_route: Ternary
        listen_port: int
        mtu: int
        peer_routes: bool
        private_key: str
        private_key_flags: SettingSecretFlags
        name: str

    props: Props = ...
    def __init__(
        self,
        fwmark: int = ...,
        ip4_auto_default_route: Ternary = ...,
        ip6_auto_default_route: Ternary = ...,
        listen_port: int = ...,
        mtu: int = ...,
        peer_routes: bool = ...,
        private_key: str = ...,
        private_key_flags: SettingSecretFlags = ...,
    ): ...
    def append_peer(self, peer: WireGuardPeer) -> None: ...
    def clear_peers(self) -> int: ...
    def get_fwmark(self) -> int: ...
    def get_ip4_auto_default_route(self) -> Ternary: ...
    def get_ip6_auto_default_route(self) -> Ternary: ...
    def get_listen_port(self) -> int: ...
    def get_mtu(self) -> int: ...
    def get_peer(self, idx: int) -> WireGuardPeer: ...
    def get_peer_by_public_key(
        self, public_key: str
    ) -> tuple[WireGuardPeer | None, int]: ...
    def get_peer_routes(self) -> bool: ...
    def get_peers_len(self) -> int: ...
    def get_private_key(self) -> str: ...
    def get_private_key_flags(self) -> SettingSecretFlags: ...
    @classmethod
    def new(cls) -> SettingWireGuard: ...
    def remove_peer(self, idx: int) -> bool: ...
    def set_peer(self, peer: WireGuardPeer, idx: int) -> None: ...

class SettingWireGuardClass(GObject.GPointer): ...

class SettingWired(Setting):
    """
    :Constructors:

    ::

        SettingWired(**properties)
        new() -> NM.Setting

    Object NMSettingWired

    Properties from NMSettingWired:
      port -> gchararray:

      speed -> guint:

      duplex -> gchararray:

      auto-negotiate -> gboolean:

      mac-address -> gchararray:

      cloned-mac-address -> gchararray:

      generate-mac-address-mask -> gchararray:

      mac-address-blacklist -> GStrv:

      mac-address-denylist -> GStrv:

      mtu -> guint:

      s390-subchannels -> GStrv:

      s390-nettype -> gchararray:

      s390-options -> GHashTable:

      wake-on-lan -> guint:

      wake-on-lan-password -> gchararray:

      accept-all-mac-addresses -> NMTernary:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        accept_all_mac_addresses: Ternary
        auto_negotiate: bool
        cloned_mac_address: str
        duplex: str
        generate_mac_address_mask: str
        mac_address: str
        mac_address_blacklist: list[str]
        mac_address_denylist: list[str]
        mtu: int
        port: str
        s390_nettype: str
        s390_options: dict[str, str]
        s390_subchannels: list[str]
        speed: int
        wake_on_lan: int
        wake_on_lan_password: str
        name: str

    props: Props = ...
    def __init__(
        self,
        accept_all_mac_addresses: Ternary = ...,
        auto_negotiate: bool = ...,
        cloned_mac_address: str = ...,
        duplex: str = ...,
        generate_mac_address_mask: str = ...,
        mac_address: str = ...,
        mac_address_blacklist: Sequence[str] = ...,
        mac_address_denylist: Sequence[str] = ...,
        mtu: int = ...,
        port: str = ...,
        s390_nettype: str = ...,
        s390_options: dict[str, str] = ...,
        s390_subchannels: Sequence[str] = ...,
        speed: int = ...,
        wake_on_lan: int = ...,
        wake_on_lan_password: str = ...,
    ): ...
    def add_mac_blacklist_item(self, mac: str) -> bool: ...
    def add_mac_denylist_item(self, mac: str) -> bool: ...
    def add_s390_option(self, key: str, value: str) -> bool: ...
    def clear_mac_blacklist_items(self) -> None: ...
    def clear_mac_denylist_items(self) -> None: ...
    def get_accept_all_mac_addresses(self) -> Ternary: ...
    def get_auto_negotiate(self) -> bool: ...
    def get_cloned_mac_address(self) -> str: ...
    def get_duplex(self) -> str: ...
    def get_generate_mac_address_mask(self) -> str: ...
    def get_mac_address(self) -> str: ...
    def get_mac_address_blacklist(self) -> list[str]: ...
    def get_mac_address_denylist(self) -> list[str]: ...
    def get_mac_blacklist_item(self, idx: int) -> str: ...
    def get_mac_denylist_item(self, idx: int) -> str: ...
    def get_mtu(self) -> int: ...
    def get_num_mac_blacklist_items(self) -> int: ...
    def get_num_mac_denylist_items(self) -> int: ...
    def get_num_s390_options(self) -> int: ...
    def get_port(self) -> str: ...
    def get_s390_nettype(self) -> str: ...
    def get_s390_option(self, idx: int) -> tuple[bool, str, str]: ...
    def get_s390_option_by_key(self, key: str) -> str: ...
    def get_s390_subchannels(self) -> list[str]: ...
    def get_speed(self) -> int: ...
    def get_valid_s390_options(self) -> list[str]: ...
    def get_wake_on_lan(self) -> SettingWiredWakeOnLan: ...
    def get_wake_on_lan_password(self) -> str: ...
    @classmethod
    def new(cls) -> SettingWired: ...
    def remove_mac_blacklist_item(self, idx: int) -> None: ...
    def remove_mac_blacklist_item_by_value(self, mac: str) -> bool: ...
    def remove_mac_denylist_item(self, idx: int) -> None: ...
    def remove_mac_denylist_item_by_value(self, mac: str) -> bool: ...
    def remove_s390_option(self, key: str) -> bool: ...

class SettingWiredClass(GObject.GPointer): ...

class SettingWireless(Setting):
    """
    :Constructors:

    ::

        SettingWireless(**properties)
        new() -> NM.Setting

    Object NMSettingWireless

    Properties from NMSettingWireless:
      ssid -> GBytes:

      mode -> gchararray:

      band -> gchararray:

      channel -> guint:

      bssid -> gchararray:

      rate -> guint:

      tx-power -> guint:

      mac-address -> gchararray:

      cloned-mac-address -> gchararray:

      generate-mac-address-mask -> gchararray:

      mac-address-blacklist -> GStrv:

      mac-address-denylist -> GStrv:

      mtu -> guint:

      seen-bssids -> GStrv:

      hidden -> gboolean:

      powersave -> guint:

      mac-address-randomization -> guint:

      wake-on-wlan -> guint:

      ap-isolation -> NMTernary:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        ap_isolation: Ternary
        band: str
        bssid: str
        channel: int
        cloned_mac_address: str
        generate_mac_address_mask: str
        hidden: bool
        mac_address: str
        mac_address_blacklist: list[str]
        mac_address_denylist: list[str]
        mac_address_randomization: int
        mode: str
        mtu: int
        powersave: int
        rate: int
        seen_bssids: list[str]
        ssid: GLib.Bytes
        tx_power: int
        wake_on_wlan: int
        name: str

    props: Props = ...
    def __init__(
        self,
        ap_isolation: Ternary = ...,
        band: str = ...,
        bssid: str = ...,
        channel: int = ...,
        cloned_mac_address: str = ...,
        generate_mac_address_mask: str = ...,
        hidden: bool = ...,
        mac_address: str = ...,
        mac_address_blacklist: Sequence[str] = ...,
        mac_address_denylist: Sequence[str] = ...,
        mac_address_randomization: int = ...,
        mode: str = ...,
        mtu: int = ...,
        powersave: int = ...,
        rate: int = ...,
        seen_bssids: Sequence[str] = ...,
        ssid: GLib.Bytes = ...,
        tx_power: int = ...,
        wake_on_wlan: int = ...,
    ): ...
    def add_mac_blacklist_item(self, mac: str) -> bool: ...
    def add_mac_denylist_item(self, mac: str) -> bool: ...
    def add_seen_bssid(self, bssid: str) -> bool: ...
    def ap_security_compatible(
        self,
        s_wireless_sec: SettingWirelessSecurity,
        ap_flags: _80211ApFlags,
        ap_wpa: _80211ApSecurityFlags,
        ap_rsn: _80211ApSecurityFlags,
        ap_mode: _80211Mode,
    ) -> bool: ...
    def clear_mac_blacklist_items(self) -> None: ...
    def clear_mac_denylist_items(self) -> None: ...
    def get_ap_isolation(self) -> Ternary: ...
    def get_band(self) -> str: ...
    def get_bssid(self) -> str: ...
    def get_channel(self) -> int: ...
    def get_cloned_mac_address(self) -> str: ...
    def get_generate_mac_address_mask(self) -> str: ...
    def get_hidden(self) -> bool: ...
    def get_mac_address(self) -> str: ...
    def get_mac_address_blacklist(self) -> list[str]: ...
    def get_mac_address_denylist(self) -> list[str]: ...
    def get_mac_address_randomization(self) -> SettingMacRandomization: ...
    def get_mac_blacklist_item(self, idx: int) -> str: ...
    def get_mac_denylist_item(self, idx: int) -> str: ...
    def get_mode(self) -> str: ...
    def get_mtu(self) -> int: ...
    def get_num_mac_blacklist_items(self) -> int: ...
    def get_num_mac_denylist_items(self) -> int: ...
    def get_num_seen_bssids(self) -> int: ...
    def get_powersave(self) -> int: ...
    def get_rate(self) -> int: ...
    def get_seen_bssid(self, i: int) -> str: ...
    def get_ssid(self) -> GLib.Bytes: ...
    def get_tx_power(self) -> int: ...
    def get_wake_on_wlan(self) -> SettingWirelessWakeOnWLan: ...
    @classmethod
    def new(cls) -> SettingWireless: ...
    def remove_mac_blacklist_item(self, idx: int) -> None: ...
    def remove_mac_blacklist_item_by_value(self, mac: str) -> bool: ...
    def remove_mac_denylist_item(self, idx: int) -> None: ...
    def remove_mac_denylist_item_by_value(self, mac: str) -> bool: ...

class SettingWirelessClass(GObject.GPointer): ...

class SettingWirelessSecurity(Setting):
    """
    :Constructors:

    ::

        SettingWirelessSecurity(**properties)
        new() -> NM.Setting

    Object NMSettingWirelessSecurity

    Properties from NMSettingWirelessSecurity:
      key-mgmt -> gchararray:

      wep-tx-keyidx -> guint:

      auth-alg -> gchararray:

      proto -> GStrv:

      pairwise -> GStrv:

      group -> GStrv:

      pmf -> gint:

      leap-username -> gchararray:

      wep-key0 -> gchararray:

      wep-key1 -> gchararray:

      wep-key2 -> gchararray:

      wep-key3 -> gchararray:

      wep-key-flags -> NMSettingSecretFlags:

      wep-key-type -> NMWepKeyType:

      psk -> gchararray:

      psk-flags -> NMSettingSecretFlags:

      leap-password -> gchararray:

      leap-password-flags -> NMSettingSecretFlags:

      wps-method -> guint:

      fils -> gint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        auth_alg: str
        fils: int
        group: list[str]
        key_mgmt: str
        leap_password: str
        leap_password_flags: SettingSecretFlags
        leap_username: str
        pairwise: list[str]
        pmf: int
        proto: list[str]
        psk: str
        psk_flags: SettingSecretFlags
        wep_key_flags: SettingSecretFlags
        wep_key_type: WepKeyType
        wep_key0: str
        wep_key1: str
        wep_key2: str
        wep_key3: str
        wep_tx_keyidx: int
        wps_method: int
        name: str

    props: Props = ...
    def __init__(
        self,
        auth_alg: str = ...,
        fils: int = ...,
        group: Sequence[str] = ...,
        key_mgmt: str = ...,
        leap_password: str = ...,
        leap_password_flags: SettingSecretFlags = ...,
        leap_username: str = ...,
        pairwise: Sequence[str] = ...,
        pmf: int = ...,
        proto: Sequence[str] = ...,
        psk: str = ...,
        psk_flags: SettingSecretFlags = ...,
        wep_key_flags: SettingSecretFlags = ...,
        wep_key_type: WepKeyType = ...,
        wep_key0: str = ...,
        wep_key1: str = ...,
        wep_key2: str = ...,
        wep_key3: str = ...,
        wep_tx_keyidx: int = ...,
        wps_method: int = ...,
    ): ...
    def add_group(self, group: str) -> bool: ...
    def add_pairwise(self, pairwise: str) -> bool: ...
    def add_proto(self, proto: str) -> bool: ...
    def clear_groups(self) -> None: ...
    def clear_pairwise(self) -> None: ...
    def clear_protos(self) -> None: ...
    def get_auth_alg(self) -> str: ...
    def get_fils(self) -> SettingWirelessSecurityFils: ...
    def get_group(self, i: int) -> str: ...
    def get_key_mgmt(self) -> str: ...
    def get_leap_password(self) -> str: ...
    def get_leap_password_flags(self) -> SettingSecretFlags: ...
    def get_leap_username(self) -> str: ...
    def get_num_groups(self) -> int: ...
    def get_num_pairwise(self) -> int: ...
    def get_num_protos(self) -> int: ...
    def get_pairwise(self, i: int) -> str: ...
    def get_pmf(self) -> SettingWirelessSecurityPmf: ...
    def get_proto(self, i: int) -> str: ...
    def get_psk(self) -> str: ...
    def get_psk_flags(self) -> SettingSecretFlags: ...
    def get_wep_key(self, idx: int) -> str: ...
    def get_wep_key_flags(self) -> SettingSecretFlags: ...
    def get_wep_key_type(self) -> WepKeyType: ...
    def get_wep_tx_keyidx(self) -> int: ...
    def get_wps_method(self) -> SettingWirelessSecurityWpsMethod: ...
    @classmethod
    def new(cls) -> SettingWirelessSecurity: ...
    def remove_group(self, i: int) -> None: ...
    def remove_group_by_value(self, group: str) -> bool: ...
    def remove_pairwise(self, i: int) -> None: ...
    def remove_pairwise_by_value(self, pairwise: str) -> bool: ...
    def remove_proto(self, i: int) -> None: ...
    def remove_proto_by_value(self, proto: str) -> bool: ...
    def set_wep_key(self, idx: int, key: str) -> None: ...

class SettingWirelessSecurityClass(GObject.GPointer): ...

class SettingWpan(Setting):
    """
    :Constructors:

    ::

        SettingWpan(**properties)
        new() -> NM.Setting

    Object NMSettingWpan

    Properties from NMSettingWpan:
      mac-address -> gchararray:

      pan-id -> guint:

      short-address -> guint:

      page -> gint:

      channel -> gint:


    Properties from NMSetting:
      name -> gchararray:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        channel: int
        mac_address: str
        page: int
        pan_id: int
        short_address: int
        name: str

    props: Props = ...
    def __init__(
        self,
        channel: int = ...,
        mac_address: str = ...,
        page: int = ...,
        pan_id: int = ...,
        short_address: int = ...,
    ): ...
    def get_channel(self) -> int: ...
    def get_mac_address(self) -> str: ...
    def get_page(self) -> int: ...
    def get_pan_id(self) -> int: ...
    def get_short_address(self) -> int: ...
    @classmethod
    def new(cls) -> SettingWpan: ...

class SettingWpanClass(GObject.GPointer): ...

class SimpleConnection(GObject.Object, Connection):
    """
    :Constructors:

    ::

        SimpleConnection(**properties)

    Object NMSimpleConnection

    Signals from NMConnection:
      secrets-updated (gchararray)
      secrets-cleared ()
      changed ()

    Signals from GObject:
      notify (GParam)
    """
    @staticmethod
    def new() -> Connection: ...
    @staticmethod
    def new_clone(connection: Connection) -> Connection: ...
    @staticmethod
    def new_from_dbus(dict: GLib.Variant) -> Connection: ...

class SimpleConnectionClass(GObject.GPointer): ...

class SriovVF(GObject.GBoxed):
    """
    :Constructors:

    ::

        new(index:int) -> NM.SriovVF
    """
    def add_vlan(self, vlan_id: int) -> bool: ...
    @staticmethod
    def attribute_validate(name: str, value: GLib.Variant) -> tuple[bool, bool]: ...
    def dup(self) -> SriovVF: ...
    def equal(self, other: SriovVF) -> bool: ...
    def get_attribute(self, name: str) -> GLib.Variant: ...
    def get_attribute_names(self) -> list[str]: ...
    def get_index(self) -> int: ...
    def get_vlan_ids(self) -> list[int]: ...
    def get_vlan_protocol(self, vlan_id: int) -> SriovVFVlanProtocol: ...
    def get_vlan_qos(self, vlan_id: int) -> int: ...
    @classmethod
    def new(cls, index: int) -> SriovVF: ...
    def ref(self) -> None: ...
    def remove_vlan(self, vlan_id: int) -> bool: ...
    def set_attribute(self, name: str, value: GLib.Variant | None = None) -> None: ...
    def set_vlan_protocol(
        self, vlan_id: int, protocol: SriovVFVlanProtocol
    ) -> None: ...
    def set_vlan_qos(self, vlan_id: int, qos: int) -> None: ...
    def unref(self) -> None: ...

class TCAction(GObject.GBoxed):
    """
    :Constructors:

    ::

        new(kind:str) -> NM.TCAction
    """
    def dup(self) -> TCAction: ...
    def equal(self, other: TCAction) -> bool: ...
    def get_attribute(self, name: str) -> GLib.Variant: ...
    def get_attribute_names(self) -> list[str]: ...
    def get_kind(self) -> str: ...
    @classmethod
    def new(cls, kind: str) -> TCAction: ...
    def ref(self) -> None: ...
    def set_attribute(self, name: str, value: GLib.Variant | None = None) -> None: ...
    def unref(self) -> None: ...

class TCQdisc(GObject.GBoxed):
    """
    :Constructors:

    ::

        new(kind:str, parent:int) -> NM.TCQdisc
    """
    def dup(self) -> TCQdisc: ...
    def equal(self, other: TCQdisc) -> bool: ...
    def get_attribute(self, name: str) -> GLib.Variant: ...
    def get_attribute_names(self) -> list[str]: ...
    def get_handle(self) -> int: ...
    def get_kind(self) -> str: ...
    def get_parent(self) -> int: ...
    @classmethod
    def new(cls, kind: str, parent: int) -> TCQdisc: ...
    def ref(self) -> None: ...
    def set_attribute(self, name: str, value: GLib.Variant | None = None) -> None: ...
    def set_handle(self, handle: int) -> None: ...
    def unref(self) -> None: ...

class TCTfilter(GObject.GBoxed):
    """
    :Constructors:

    ::

        new(kind:str, parent:int) -> NM.TCTfilter
    """
    def dup(self) -> TCTfilter: ...
    def equal(self, other: TCTfilter) -> bool: ...
    def get_action(self) -> TCAction: ...
    def get_handle(self) -> int: ...
    def get_kind(self) -> str: ...
    def get_parent(self) -> int: ...
    @classmethod
    def new(cls, kind: str, parent: int) -> TCTfilter: ...
    def ref(self) -> None: ...
    def set_action(self, action: TCAction) -> None: ...
    def set_handle(self, handle: int) -> None: ...
    def unref(self) -> None: ...

class TeamLinkWatcher(GObject.GBoxed):
    """
    :Constructors:

    ::

        new_arp_ping(init_wait:int, interval:int, missed_max:int, target_host:str, source_host:str, flags:NM.TeamLinkWatcherArpPingFlags) -> NM.TeamLinkWatcher
        new_arp_ping2(init_wait:int, interval:int, missed_max:int, vlanid:int, target_host:str, source_host:str, flags:NM.TeamLinkWatcherArpPingFlags) -> NM.TeamLinkWatcher
        new_ethtool(delay_up:int, delay_down:int) -> NM.TeamLinkWatcher
        new_nsna_ping(init_wait:int, interval:int, missed_max:int, target_host:str) -> NM.TeamLinkWatcher
    """
    def dup(self) -> TeamLinkWatcher: ...
    def equal(self, other: TeamLinkWatcher) -> bool: ...
    def get_delay_down(self) -> int: ...
    def get_delay_up(self) -> int: ...
    def get_flags(self) -> TeamLinkWatcherArpPingFlags: ...
    def get_init_wait(self) -> int: ...
    def get_interval(self) -> int: ...
    def get_missed_max(self) -> int: ...
    def get_name(self) -> str: ...
    def get_source_host(self) -> str: ...
    def get_target_host(self) -> str: ...
    def get_vlanid(self) -> int: ...
    @classmethod
    def new_arp_ping(
        cls,
        init_wait: int,
        interval: int,
        missed_max: int,
        target_host: str,
        source_host: str,
        flags: TeamLinkWatcherArpPingFlags,
    ) -> TeamLinkWatcher: ...
    @classmethod
    def new_arp_ping2(
        cls,
        init_wait: int,
        interval: int,
        missed_max: int,
        vlanid: int,
        target_host: str,
        source_host: str,
        flags: TeamLinkWatcherArpPingFlags,
    ) -> TeamLinkWatcher: ...
    @classmethod
    def new_ethtool(cls, delay_up: int, delay_down: int) -> TeamLinkWatcher: ...
    @classmethod
    def new_nsna_ping(
        cls, init_wait: int, interval: int, missed_max: int, target_host: str
    ) -> TeamLinkWatcher: ...
    def ref(self) -> None: ...
    def unref(self) -> None: ...

class VariantAttributeSpec(GObject.GPointer): ...

class VpnConnection(ActiveConnection):
    """
    :Constructors:

    ::

        VpnConnection(**properties)

    Object NMVpnConnection

    Signals from NMVpnConnection:
      vpn-state-changed (guint, guint)

    Properties from NMVpnConnection:
      vpn-state -> NMVpnConnectionState:

      banner -> gchararray:


    Signals from NMActiveConnection:
      state-changed (guint, guint)

    Properties from NMActiveConnection:
      connection -> NMRemoteConnection:

      id -> gchararray:

      uuid -> gchararray:

      type -> gchararray:

      specific-object-path -> gchararray:

      devices -> GPtrArray:

      state -> NMActiveConnectionState:

      state-flags -> guint:

      default -> gboolean:

      ip4-config -> NMIPConfig:

      dhcp4-config -> NMDhcpConfig:

      default6 -> gboolean:

      ip6-config -> NMIPConfig:

      dhcp6-config -> NMDhcpConfig:

      vpn -> gboolean:

      master -> NMDevice:

      controller -> NMDevice:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        banner: str
        vpn_state: VpnConnectionState
        connection: RemoteConnection
        controller: Device | None
        default: bool
        default6: bool
        devices: list[Device]
        dhcp4_config: DhcpConfig
        dhcp6_config: DhcpConfig
        id: str
        ip4_config: IPConfig
        ip6_config: IPConfig
        master: Device | None
        specific_object_path: str
        state: ActiveConnectionState
        state_flags: int
        type: str
        uuid: str
        vpn: bool
        client: Client | None
        path: str

    props: Props = ...
    def get_banner(self) -> str: ...
    def get_vpn_state(self) -> VpnConnectionState: ...

class VpnConnectionClass(GObject.GPointer): ...

class VpnEditor(GObject.GInterface):
    """
    Interface NMVpnEditor

    Signals from GObject:
      notify (GParam)
    """
    def get_widget(self) -> GObject.Object: ...
    def update_connection(self, connection: Connection) -> bool: ...

class VpnEditorInterface(GObject.GPointer):
    """
    :Constructors:

    ::

        VpnEditorInterface()
    """

    g_iface: GObject.TypeInterface = ...
    get_widget: Callable[[VpnEditor], GObject.Object] = ...
    placeholder: Callable[[], None] = ...
    update_connection: Callable[[VpnEditor, Connection], bool] = ...
    changed: Callable[[VpnEditor], None] = ...

class VpnEditorPlugin(GObject.GInterface):
    """
    Interface NMVpnEditorPlugin

    Signals from GObject:
      notify (GParam)
    """
    def export(self, path: str, connection: Connection) -> bool: ...
    def get_capabilities(self) -> VpnEditorPluginCapability: ...
    def get_editor(self, connection: Connection) -> VpnEditor: ...
    def get_plugin_info(self) -> VpnPluginInfo: ...
    def get_suggested_filename(self, connection: Connection) -> str: ...
    def get_vt(self, vt_size: int) -> tuple[int, VpnEditorPluginVT]: ...
    def import_(self, path: str) -> Connection: ...
    @staticmethod
    def load(plugin_name: str, check_service: str) -> VpnEditorPlugin: ...
    @staticmethod
    def load_from_file(
        plugin_name: str,
        check_service: str,
        check_owner: int,
        check_file: Callable[..., bool],
        *user_data: Any,
    ) -> VpnEditorPlugin: ...
    def set_plugin_info(self, plugin_info: VpnPluginInfo | None = None) -> None: ...

class VpnEditorPluginInterface(GObject.GPointer):
    """
    :Constructors:

    ::

        VpnEditorPluginInterface()
    """

    g_iface: GObject.TypeInterface = ...
    get_editor: Callable[[VpnEditorPlugin, Connection], VpnEditor] = ...
    get_capabilities: Callable[[VpnEditorPlugin], VpnEditorPluginCapability] = ...
    import_from_file: None = ...
    export_to_file: Callable[[VpnEditorPlugin, str, Connection], bool] = ...
    get_suggested_filename: Callable[[VpnEditorPlugin, Connection], str] = ...
    notify_plugin_info_set: Callable[[VpnEditorPlugin, VpnPluginInfo], None] = ...
    get_vt: Callable[[VpnEditorPlugin, int], VpnEditorPluginVT] = ...

class VpnEditorPluginVT(GObject.GPointer): ...

class VpnPluginInfo(GObject.Object, Gio.Initable):  # type: ignore
    """
    :Constructors:

    ::

        VpnPluginInfo(**properties)
        new_from_file(filename:str) -> NM.VpnPluginInfo
        new_search_file(name:str=None, service:str=None) -> NM.VpnPluginInfo or None
        new_with_data(filename:str, keyfile:GLib.KeyFile) -> NM.VpnPluginInfo

    Object NMVpnPluginInfo

    Properties from NMVpnPluginInfo:
      name -> gchararray:

      filename -> gchararray:

      keyfile -> GKeyFile:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        filename: str
        name: str
        keyfile: GLib.KeyFile

    props: Props = ...
    def __init__(self, filename: str = ..., keyfile: GLib.KeyFile = ...): ...
    def get_aliases(self) -> list[str]: ...
    def get_auth_dialog(self) -> str: ...
    def get_editor_plugin(self) -> VpnEditorPlugin: ...
    def get_filename(self) -> str: ...
    def get_name(self) -> str: ...
    def get_plugin(self) -> str: ...
    def get_program(self) -> str: ...
    def get_service(self) -> str: ...
    @staticmethod
    def list_add(list: list[VpnPluginInfo], plugin_info: VpnPluginInfo) -> bool: ...
    @staticmethod
    def list_find_by_filename(
        list: list[VpnPluginInfo], filename: str
    ) -> VpnPluginInfo: ...
    @staticmethod
    def list_find_by_name(list: list[VpnPluginInfo], name: str) -> VpnPluginInfo: ...
    @staticmethod
    def list_find_by_service(
        list: list[VpnPluginInfo], service: str
    ) -> VpnPluginInfo: ...
    @staticmethod
    def list_find_service_type(list: list[VpnPluginInfo], name: str) -> str: ...
    @staticmethod
    def list_get_service_types(
        list: list[VpnPluginInfo], only_existing: bool, with_abbreviations: bool
    ) -> list[str]: ...
    @staticmethod
    def list_load() -> list[VpnPluginInfo]: ...
    @staticmethod
    def list_remove(list: list[VpnPluginInfo], plugin_info: VpnPluginInfo) -> bool: ...
    def load_editor_plugin(self) -> VpnEditorPlugin: ...
    def lookup_property(self, group: str, key: str) -> str: ...
    @classmethod
    def new_from_file(cls, filename: str) -> VpnPluginInfo: ...
    @classmethod
    def new_search_file(
        cls, name: str | None = None, service: str | None = None
    ) -> VpnPluginInfo | None: ...
    @classmethod
    def new_with_data(cls, filename: str, keyfile: GLib.KeyFile) -> VpnPluginInfo: ...
    def set_editor_plugin(self, plugin: VpnEditorPlugin | None = None) -> None: ...
    def supports_hints(self) -> bool: ...
    def supports_multiple(self) -> bool: ...
    @staticmethod
    def validate_filename(filename: str) -> bool: ...

class VpnPluginInfoClass(GObject.GPointer): ...

class VpnPluginOld(GObject.Object, Gio.Initable):  # type: ignore
    """
    :Constructors:

    ::

        VpnPluginOld(**properties)

    Object NMVpnPluginOld

    Signals from NMVpnPluginOld:
      ip4-config (GVariant)
      ip6-config (GVariant)
      state-changed (guint)
      config (GVariant)
      secrets-required (gchararray, GStrv)
      login-banner (gchararray)
      failure (guint)
      quit ()

    Properties from NMVpnPluginOld:
      service-name -> gchararray:

      state -> NMVpnServiceState:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        service_name: str
        state: VpnServiceState

    props: Props = ...
    parent: GObject.Object = ...
    def __init__(self, service_name: str = ..., state: VpnServiceState = ...): ...
    def disconnect(self) -> bool: ...  # type: ignore
    def do_config(self, config: GLib.Variant) -> None: ...
    def do_connect(self, connection: Connection) -> bool: ...
    def do_connect_interactive(
        self, connection: Connection, details: GLib.Variant
    ) -> bool: ...
    def do_disconnect(self) -> bool: ...
    def do_failure(self, reason: VpnPluginFailure) -> None: ...
    def do_ip4_config(self, ip4_config: GLib.Variant) -> None: ...
    def do_ip6_config(self, config: GLib.Variant) -> None: ...
    def do_login_banner(self, banner: str) -> None: ...
    def do_need_secrets(self, connection: Connection, setting_name: str) -> bool: ...
    def do_new_secrets(self, connection: Connection) -> bool: ...
    def do_quit(self) -> None: ...
    def do_state_changed(self, state: VpnServiceState) -> None: ...
    def failure(self, reason: VpnPluginFailure) -> None: ...
    def get_connection(self) -> Gio.DBusConnection: ...
    @staticmethod
    def get_secret_flags(
        data: dict[None, None], secret_name: str
    ) -> tuple[bool, SettingSecretFlags]: ...
    def get_state(self) -> VpnServiceState: ...
    @staticmethod
    def read_vpn_details(
        fd: int,
    ) -> tuple[bool, dict[None, None], dict[None, None]]: ...
    def secrets_required(self, message: str, hints: str) -> None: ...
    def set_ip4_config(self, ip4_config: GLib.Variant) -> None: ...
    def set_login_banner(self, banner: str) -> None: ...
    def set_state(self, state: VpnServiceState) -> None: ...

class VpnPluginOldClass(GObject.GPointer):
    """
    :Constructors:

    ::

        VpnPluginOldClass()
    """

    parent: GObject.ObjectClass = ...
    state_changed: Callable[[VpnPluginOld, VpnServiceState], None] = ...
    ip4_config: Callable[[VpnPluginOld, GLib.Variant], None] = ...
    login_banner: Callable[[VpnPluginOld, str], None] = ...
    failure: Callable[[VpnPluginOld, VpnPluginFailure], None] = ...
    quit: Callable[[VpnPluginOld], None] = ...
    config: Callable[[VpnPluginOld, GLib.Variant], None] = ...
    ip6_config: Callable[[VpnPluginOld, GLib.Variant], None] = ...
    connect: Callable[[VpnPluginOld, Connection], bool] = ...
    need_secrets: Callable[[VpnPluginOld, Connection, str], bool] = ...
    disconnect: Callable[[VpnPluginOld], bool] = ...
    new_secrets: Callable[[VpnPluginOld, Connection], bool] = ...
    connect_interactive: Callable[[VpnPluginOld, Connection, GLib.Variant], bool] = ...
    padding: list[None] = ...

class VpnServicePlugin(GObject.Object, Gio.Initable):  # type: ignore
    """
    :Constructors:

    ::

        VpnServicePlugin(**properties)

    Object NMVpnServicePlugin

    Signals from NMVpnServicePlugin:
      ip4-config (GVariant)
      ip6-config (GVariant)
      state-changed (guint)
      config (GVariant)
      secrets-required (gchararray, GStrv)
      login-banner (gchararray)
      failure (guint)
      quit ()

    Properties from NMVpnServicePlugin:
      service-name -> gchararray:

      watch-peer -> gboolean:

      state -> NMVpnServiceState:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        service_name: str
        state: VpnServiceState
        watch_peer: bool

    props: Props = ...
    parent: GObject.Object = ...
    def __init__(
        self,
        service_name: str = ...,
        state: VpnServiceState = ...,
        watch_peer: bool = ...,
    ): ...
    def disconnect(self) -> bool: ...  # type: ignore
    def do_config(self, config: GLib.Variant) -> None: ...
    def do_connect(self, connection: Connection) -> bool: ...
    def do_connect_interactive(
        self, connection: Connection, details: GLib.Variant
    ) -> bool: ...
    def do_disconnect(self) -> bool: ...
    def do_failure(self, reason: VpnPluginFailure) -> None: ...
    def do_ip4_config(self, ip4_config: GLib.Variant) -> None: ...
    def do_ip6_config(self, config: GLib.Variant) -> None: ...
    def do_login_banner(self, banner: str) -> None: ...
    def do_need_secrets(self, connection: Connection, setting_name: str) -> bool: ...
    def do_new_secrets(self, connection: Connection) -> bool: ...
    def do_quit(self) -> None: ...
    def do_state_changed(self, state: VpnServiceState) -> None: ...
    def failure(self, reason: VpnPluginFailure) -> None: ...
    def get_connection(self) -> Gio.DBusConnection: ...
    @staticmethod
    def get_secret_flags(
        data: dict[None, None], secret_name: str
    ) -> tuple[bool, SettingSecretFlags]: ...
    @staticmethod
    def read_vpn_details(
        fd: int,
    ) -> tuple[bool, dict[None, None], dict[None, None]]: ...
    def secrets_required(self, message: str, hints: str) -> None: ...
    def set_config(self, config: GLib.Variant) -> None: ...
    def set_ip4_config(self, ip4_config: GLib.Variant) -> None: ...
    def set_ip6_config(self, ip6_config: GLib.Variant) -> None: ...
    def set_login_banner(self, banner: str) -> None: ...
    def shutdown(self) -> None: ...

class VpnServicePluginClass(GObject.GPointer):
    """
    :Constructors:

    ::

        VpnServicePluginClass()
    """

    parent: GObject.ObjectClass = ...
    state_changed: Callable[[VpnServicePlugin, VpnServiceState], None] = ...
    ip4_config: Callable[[VpnServicePlugin, GLib.Variant], None] = ...
    login_banner: Callable[[VpnServicePlugin, str], None] = ...
    failure: Callable[[VpnServicePlugin, VpnPluginFailure], None] = ...
    quit: Callable[[VpnServicePlugin], None] = ...
    config: Callable[[VpnServicePlugin, GLib.Variant], None] = ...
    ip6_config: Callable[[VpnServicePlugin, GLib.Variant], None] = ...
    connect: Callable[[VpnServicePlugin, Connection], bool] = ...
    need_secrets: Callable[[VpnServicePlugin, Connection, str], bool] = ...
    disconnect: Callable[[VpnServicePlugin], bool] = ...
    new_secrets: Callable[[VpnServicePlugin, Connection], bool] = ...
    connect_interactive: Callable[
        [VpnServicePlugin, Connection, GLib.Variant], bool
    ] = ...
    padding: list[None] = ...

class WifiP2PPeer(Object):
    """
    :Constructors:

    ::

        WifiP2PPeer(**properties)

    Object NMWifiP2PPeer

    Properties from NMWifiP2PPeer:
      flags -> NM80211ApFlags:

      name -> gchararray:

      manufacturer -> gchararray:

      model -> gchararray:

      model-number -> gchararray:

      serial -> gchararray:

      wfd-ies -> GBytes:

      hw-address -> gchararray:

      strength -> guchar:

      last-seen -> gint:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        flags: _80211ApFlags
        hw_address: str
        last_seen: int
        manufacturer: str
        model: str
        model_number: str
        name: str
        serial: str
        strength: int
        wfd_ies: GLib.Bytes
        client: Client | None
        path: str

    props: Props = ...
    def connection_valid(self, connection: Connection) -> bool: ...
    def filter_connections(
        self, connections: Sequence[Connection]
    ) -> list[Connection]: ...
    def get_flags(self) -> _80211ApFlags: ...
    def get_hw_address(self) -> str: ...
    def get_last_seen(self) -> int: ...
    def get_manufacturer(self) -> str: ...
    def get_model(self) -> str: ...
    def get_model_number(self) -> str: ...
    def get_name(self) -> str: ...
    def get_serial(self) -> str: ...
    def get_strength(self) -> int: ...
    def get_wfd_ies(self) -> GLib.Bytes: ...

class WifiP2PPeerClass(GObject.GPointer): ...

class WimaxNsp(Object):
    """
    :Constructors:

    ::

        WimaxNsp(**properties)

    Object NMWimaxNsp

    Properties from NMWimaxNsp:
      name -> gchararray:

      signal-quality -> guint:

      network-type -> NMWimaxNspNetworkType:


    Properties from NMObject:
      path -> gchararray:

      client -> NMClient:


    Signals from GObject:
      notify (GParam)
    """
    class Props:
        name: str
        network_type: WimaxNspNetworkType
        signal_quality: int
        client: Client | None
        path: str

    props: Props = ...
    def connection_valid(self, connection: Connection) -> bool: ...
    def filter_connections(
        self, connections: Sequence[Connection]
    ) -> list[Connection]: ...
    def get_name(self) -> str: ...
    def get_network_type(self) -> WimaxNspNetworkType: ...
    def get_signal_quality(self) -> int: ...

class WimaxNspClass(GObject.GPointer): ...

class WireGuardPeer(GObject.GBoxed):
    """
    :Constructors:

    ::

        new() -> NM.WireGuardPeer
    """
    def append_allowed_ip(self, allowed_ip: str, accept_invalid: bool) -> bool: ...
    def clear_allowed_ips(self) -> None: ...
    def cmp(
        self, b: WireGuardPeer | None, compare_flags: SettingCompareFlags
    ) -> int: ...
    def get_allowed_ip(
        self, idx: int, out_is_valid: bool | None = None
    ) -> str | None: ...
    def get_allowed_ips_len(self) -> int: ...
    def get_endpoint(self) -> str: ...
    def get_persistent_keepalive(self) -> int: ...
    def get_preshared_key(self) -> str: ...
    def get_preshared_key_flags(self) -> SettingSecretFlags: ...
    def get_public_key(self) -> str: ...
    def is_sealed(self) -> bool: ...
    def is_valid(self, check_non_secrets: bool, check_secrets: bool) -> bool: ...
    @classmethod
    def new(cls) -> WireGuardPeer: ...
    def new_clone(self, with_secrets: bool) -> WireGuardPeer: ...
    def ref(self) -> WireGuardPeer: ...
    def remove_allowed_ip(self, idx: int) -> bool: ...
    def seal(self) -> None: ...
    def set_endpoint(self, endpoint: str, allow_invalid: bool) -> bool: ...
    def set_persistent_keepalive(self, persistent_keepalive: int) -> None: ...
    def set_preshared_key(
        self, preshared_key: str | None, accept_invalid: bool
    ) -> bool: ...
    def set_preshared_key_flags(
        self, preshared_key_flags: SettingSecretFlags
    ) -> None: ...
    def set_public_key(self, public_key: str | None, accept_invalid: bool) -> bool: ...
    def unref(self) -> None: ...

class ActivationStateFlags(enum.Enum):
    CONTROLLER_HAS_PORTS = 32
    EXTERNAL = 128
    IP4_READY = 8
    IP6_READY = 16
    IS_CONTROLLER = 1
    IS_PORT = 2
    LAYER2_READY = 4
    LIFETIME_BOUND_TO_PROFILE_VISIBILITY = 64
    NONE = 0

class BluetoothCapabilities(enum.Enum):
    DUN = 1
    NAP = 2
    NONE = 0

class CheckpointCreateFlags(enum.Enum):
    ALLOW_OVERLAPPING = 8
    DELETE_NEW_CONNECTIONS = 2
    DESTROY_ALL = 1
    DISCONNECT_NEW_DEVICES = 4
    NONE = 0
    NO_PRESERVE_EXTERNAL_PORTS = 16
    TRACK_INTERNAL_GLOBAL_DNS = 32

class ClientInstanceFlags(enum.Enum):
    INITIALIZED_BAD = 4
    INITIALIZED_GOOD = 2
    NONE = 0
    NO_AUTO_FETCH_PERMISSIONS = 1

class ConnectionSerializationFlags(enum.Enum):
    ALL = 0
    NO_SECRETS = 1
    ONLY_SECRETS = 2
    WITH_NON_SECRET = 1
    WITH_SECRETS = 2
    WITH_SECRETS_AGENT_OWNED = 4
    WITH_SECRETS_NOT_SAVED = 16
    WITH_SECRETS_SYSTEM_OWNED = 8

class DeviceCapabilities(enum.Enum):
    CARRIER_DETECT = 2
    IS_SOFTWARE = 4
    NM_SUPPORTED = 1
    NONE = 0
    SRIOV = 8

class DeviceInterfaceFlags(enum.Enum):
    CARRIER = 65536
    LLDP_CLIENT_ENABLED = 131072
    LOWER_UP = 2
    PROMISC = 4
    UP = 1

class DeviceModemCapabilities(enum.Enum):
    CDMA_EVDO = 2
    GSM_UMTS = 4
    LTE = 8
    NONE = 0
    POTS = 1

class DeviceReapplyFlags(enum.Enum):
    NONE = 0
    PRESERVE_EXTERNAL_IP = 1

class DeviceWifiCapabilities(enum.Enum):
    ADHOC = 128
    AP = 64
    CIPHER_CCMP = 8
    CIPHER_TKIP = 4
    CIPHER_WEP104 = 2
    CIPHER_WEP40 = 1
    FREQ_2GHZ = 512
    FREQ_5GHZ = 1024
    FREQ_6GHZ = 2048
    FREQ_VALID = 256
    IBSS_RSN = 8192
    MESH = 4096
    NONE = 0
    RSN = 32
    WPA = 16

class DhcpHostnameFlags(enum.Enum):
    FQDN_CLEAR_FLAGS = 8
    FQDN_ENCODED = 2
    FQDN_NO_UPDATE = 4
    FQDN_SERV_UPDATE = 1
    NONE = 0

class IPAddressCmpFlags(enum.Enum):
    NONE = 0
    WITH_ATTRS = 1

class IPRoutingRuleAsStringFlags(enum.Enum):
    AF_INET = 1
    AF_INET6 = 2
    NONE = 0
    VALIDATE = 4

class IPTunnelFlags(enum.Enum):
    IP6_IGN_ENCAP_LIMIT = 1
    IP6_MIP6_DEV = 8
    IP6_RCV_DSCP_COPY = 16
    IP6_USE_ORIG_FLOWLABEL = 4
    IP6_USE_ORIG_FWMARK = 32
    IP6_USE_ORIG_TCLASS = 2
    NONE = 0

class KeyfileHandlerFlags(enum.Enum):
    NONE = 0

class ManagerReloadFlags(enum.Enum):
    CONF = 1
    DNS_FULL = 4
    DNS_RC = 2

class MptcpFlags(enum.Enum):
    ALSO_WITHOUT_DEFAULT_ROUTE = 8
    ALSO_WITHOUT_SYSCTL = 4
    BACKUP = 64
    DISABLED = 1
    ENABLED = 2
    FULLMESH = 128
    NONE = 0
    SIGNAL = 16
    SUBFLOW = 32

class RadioFlags(enum.Enum):
    NONE = 0
    WLAN_AVAILABLE = 1
    WWAN_AVAILABLE = 2

class SecretAgentCapabilities(enum.Enum):
    LAST = 1
    NONE = 0
    VPN_HINTS = 1

class SecretAgentGetSecretsFlags(enum.Enum):
    ALLOW_INTERACTION = 1
    NONE = 0
    NO_ERRORS = 1073741824
    ONLY_SYSTEM = 2147483648
    REQUEST_NEW = 2
    USER_REQUESTED = 4
    WPS_PBC_ACTIVE = 8

class Setting8021xAuthFlags(enum.Enum):
    ALL = 511
    NONE = 0
    TLS_1_0_DISABLE = 1
    TLS_1_0_ENABLE = 32
    TLS_1_1_DISABLE = 2
    TLS_1_1_ENABLE = 64
    TLS_1_2_DISABLE = 4
    TLS_1_2_ENABLE = 128
    TLS_1_3_DISABLE = 16
    TLS_1_3_ENABLE = 256
    TLS_DISABLE_TIME_CHECKS = 8

class SettingDcbFlags(enum.Enum):
    ADVERTISE = 2
    ENABLE = 1
    NONE = 0
    WILLING = 4

class SettingSecretFlags(enum.Enum):
    AGENT_OWNED = 1
    NONE = 0
    NOT_REQUIRED = 4
    NOT_SAVED = 2

class SettingWiredWakeOnLan(enum.Enum):
    ARP = 32
    BROADCAST = 16
    DEFAULT = 1
    IGNORE = 32768
    MAGIC = 64
    MULTICAST = 8
    PHY = 2
    UNICAST = 4

class SettingWirelessSecurityWpsMethod(enum.Enum):
    AUTO = 2
    DEFAULT = 0
    DISABLED = 1
    PBC = 4
    PIN = 8

class SettingWirelessWakeOnWLan(enum.Enum):
    ALL = 510
    ANY = 2
    DEFAULT = 1
    DISCONNECT = 4
    EAP_IDENTITY_REQUEST = 32
    GTK_REKEY_FAILURE = 16
    IGNORE = 32768
    MAGIC = 8
    RFKILL_RELEASE = 128
    TCP = 256

class SettingsAddConnection2Flags(enum.Enum):
    BLOCK_AUTOCONNECT = 32
    IN_MEMORY = 2
    NONE = 0
    TO_DISK = 1

class SettingsConnectionFlags(enum.Enum):
    EXTERNAL = 8
    NM_GENERATED = 2
    NONE = 0
    UNSAVED = 1
    VOLATILE = 4

class SettingsUpdate2Flags(enum.Enum):
    BLOCK_AUTOCONNECT = 32
    IN_MEMORY = 2
    IN_MEMORY_DETACHED = 4
    IN_MEMORY_ONLY = 8
    NONE = 0
    NO_REAPPLY = 64
    TO_DISK = 1
    VOLATILE = 16

class TeamLinkWatcherArpPingFlags(enum.Enum):
    SEND_ALWAYS = 8
    VALIDATE_ACTIVE = 2
    VALIDATE_INACTIVE = 4

class VlanFlags(enum.Enum):
    GVRP = 2
    LOOSE_BINDING = 4
    MVRP = 8
    REORDER_HEADERS = 1

class VpnEditorPluginCapability(enum.Enum):
    EXPORT = 2
    IMPORT = 1
    IPV6 = 4
    NONE = 0

class ActiveConnectionState(enum.Enum):
    ACTIVATED = 2
    ACTIVATING = 1
    DEACTIVATED = 4
    DEACTIVATING = 3
    UNKNOWN = 0

class ActiveConnectionStateReason(enum.Enum):
    CONNECTION_REMOVED = 11
    CONNECT_TIMEOUT = 6
    DEPENDENCY_FAILED = 12
    DEVICE_DISCONNECTED = 3
    DEVICE_REALIZE_FAILED = 13
    DEVICE_REMOVED = 14
    IP_CONFIG_INVALID = 5
    LOGIN_FAILED = 10
    NONE = 1
    NO_SECRETS = 9
    SERVICE_START_FAILED = 8
    SERVICE_START_TIMEOUT = 7
    SERVICE_STOPPED = 4
    UNKNOWN = 0
    USER_DISCONNECTED = 2

class AgentManagerError(enum.Enum):
    FAILED = 0
    INVALIDIDENTIFIER = 2
    NOSECRETS = 4
    NOTREGISTERED = 3
    PERMISSIONDENIED = 1
    USERCANCELED = 5
    @staticmethod
    def quark() -> int: ...

class Capability(enum.Enum):
    OVS = 2
    TEAM = 1

class ClientError(enum.Enum):
    FAILED = 0
    MANAGER_NOT_RUNNING = 1
    OBJECT_CREATION_FAILED = 2
    @staticmethod
    def quark() -> int: ...

class ClientPermission(enum.Enum):
    CHECKPOINT_ROLLBACK = 14
    ENABLE_DISABLE_CONNECTIVITY_CHECK = 16
    ENABLE_DISABLE_NETWORK = 1
    ENABLE_DISABLE_STATISTICS = 15
    ENABLE_DISABLE_WIFI = 2
    ENABLE_DISABLE_WIMAX = 4
    ENABLE_DISABLE_WWAN = 3
    LAST = 17
    NETWORK_CONTROL = 6
    NONE = 0
    RELOAD = 13
    SETTINGS_MODIFY_GLOBAL_DNS = 12
    SETTINGS_MODIFY_HOSTNAME = 11
    SETTINGS_MODIFY_OWN = 10
    SETTINGS_MODIFY_SYSTEM = 9
    SLEEP_WAKE = 5
    WIFI_SCAN = 17
    WIFI_SHARE_OPEN = 8
    WIFI_SHARE_PROTECTED = 7

class ClientPermissionResult(enum.Enum):
    AUTH = 2
    NO = 3
    UNKNOWN = 0
    YES = 1

class ConnectionError(enum.Enum):
    FAILED = 0
    INVALIDPROPERTY = 7
    INVALIDSETTING = 5
    MISSINGPROPERTY = 6
    MISSINGSETTING = 4
    PROPERTYNOTFOUND = 2
    PROPERTYNOTSECRET = 3
    SETTINGNOTFOUND = 1
    @staticmethod
    def quark() -> int: ...

class ConnectionMultiConnect(enum.Enum):
    DEFAULT = 0
    MANUAL_MULTIPLE = 2
    MULTIPLE = 3
    SINGLE = 1

class ConnectivityState(enum.Enum):
    FULL = 4
    LIMITED = 3
    NONE = 1
    PORTAL = 2
    UNKNOWN = 0

class CryptoError(enum.Enum):
    DECRYPTION_FAILED = 4
    ENCRYPTION_FAILED = 5
    FAILED = 0
    INVALID_DATA = 1
    INVALID_PASSWORD = 2
    UNKNOWN_CIPHER = 3
    @staticmethod
    def quark() -> int: ...

class DeviceError(enum.Enum):
    CREATIONFAILED = 1
    FAILED = 0
    INCOMPATIBLECONNECTION = 3
    INVALIDARGUMENT = 10
    INVALIDCONNECTION = 2
    MISSINGDEPENDENCIES = 9
    NOTACTIVE = 4
    NOTALLOWED = 6
    NOTSOFTWARE = 5
    SPECIFICOBJECTNOTFOUND = 7
    VERSIONIDMISMATCH = 8
    @staticmethod
    def quark() -> int: ...

class DeviceState(enum.Enum):
    ACTIVATED = 100
    CONFIG = 50
    DEACTIVATING = 110
    DISCONNECTED = 30
    FAILED = 120
    IP_CHECK = 80
    IP_CONFIG = 70
    NEED_AUTH = 60
    PREPARE = 40
    SECONDARIES = 90
    UNAVAILABLE = 20
    UNKNOWN = 0
    UNMANAGED = 10

class DeviceStateReason(enum.Enum):
    AUTOIP_ERROR = 21
    AUTOIP_FAILED = 22
    AUTOIP_START_FAILED = 20
    BR2684_FAILED = 51
    BT_FAILED = 44
    CARRIER = 40
    CONFIG_FAILED = 4
    CONNECTION_ASSUMED = 41
    CONNECTION_REMOVED = 38
    DCB_FCOE_FAILED = 55
    DEPENDENCY_FAILED = 50
    DEVICE_HANDLER_FAILED = 68
    DHCP_ERROR = 16
    DHCP_FAILED = 17
    DHCP_START_FAILED = 15
    FIRMWARE_MISSING = 35
    GSM_APN_FAILED = 29
    GSM_PIN_CHECK_FAILED = 34
    GSM_REGISTRATION_DENIED = 31
    GSM_REGISTRATION_FAILED = 33
    GSM_REGISTRATION_NOT_SEARCHING = 30
    GSM_REGISTRATION_TIMEOUT = 32
    GSM_SIM_NOT_INSERTED = 45
    GSM_SIM_PIN_REQUIRED = 46
    GSM_SIM_PUK_REQUIRED = 47
    GSM_SIM_WRONG = 48
    INFINIBAND_MODE = 49
    IP_ADDRESS_DUPLICATE = 64
    IP_CONFIG_EXPIRED = 6
    IP_CONFIG_UNAVAILABLE = 5
    IP_METHOD_UNSUPPORTED = 65
    MODEM_AVAILABLE = 58
    MODEM_BUSY = 23
    MODEM_DIAL_FAILED = 27
    MODEM_DIAL_TIMEOUT = 26
    MODEM_FAILED = 57
    MODEM_INIT_FAILED = 28
    MODEM_MANAGER_UNAVAILABLE = 52
    MODEM_NOT_FOUND = 43
    MODEM_NO_CARRIER = 25
    MODEM_NO_DIAL_TONE = 24
    NEW_ACTIVATION = 60
    NONE = 0
    NOW_MANAGED = 2
    NOW_UNMANAGED = 3
    NO_SECRETS = 7
    OVSDB_FAILED = 63
    PARENT_CHANGED = 61
    PARENT_MANAGED_CHANGED = 62
    PEER_NOT_FOUND = 67
    PPP_DISCONNECT = 13
    PPP_FAILED = 14
    PPP_START_FAILED = 12
    REMOVED = 36
    SECONDARY_CONNECTION_FAILED = 54
    SHARED_FAILED = 19
    SHARED_START_FAILED = 18
    SIM_PIN_INCORRECT = 59
    SLEEPING = 37
    SRIOV_CONFIGURATION_FAILED = 66
    SSID_NOT_FOUND = 53
    SUPPLICANT_AVAILABLE = 42
    SUPPLICANT_CONFIG_FAILED = 9
    SUPPLICANT_DISCONNECT = 8
    SUPPLICANT_FAILED = 10
    SUPPLICANT_TIMEOUT = 11
    TEAMD_CONTROL_FAILED = 56
    UNKNOWN = 1
    UNMANAGED_BY_DEFAULT = 69
    UNMANAGED_EXTERNAL_DOWN = 70
    UNMANAGED_LINK_NOT_INIT = 71
    UNMANAGED_QUITTING = 72
    UNMANAGED_SLEEPING = 73
    UNMANAGED_USER_CONF = 74
    UNMANAGED_USER_EXPLICIT = 75
    UNMANAGED_USER_SETTINGS = 76
    UNMANAGED_USER_UDEV = 77
    USER_REQUESTED = 39

class DeviceType(enum.Enum):
    ADSL = 12
    BOND = 10
    BRIDGE = 13
    BT = 5
    DUMMY = 22
    ETHERNET = 1
    GENERIC = 14
    HSR = 33
    INFINIBAND = 9
    IP_TUNNEL = 17
    LOOPBACK = 32
    MACSEC = 21
    MACVLAN = 18
    MODEM = 8
    OLPC_MESH = 6
    OVS_BRIDGE = 26
    OVS_INTERFACE = 24
    OVS_PORT = 25
    PPP = 23
    TEAM = 15
    TUN = 16
    UNKNOWN = 0
    UNUSED1 = 3
    UNUSED2 = 4
    VETH = 20
    VLAN = 11
    VRF = 31
    VXLAN = 19
    WIFI = 2
    WIFI_P2P = 30
    WIMAX = 7
    WIREGUARD = 29
    WPAN = 27

class IPTunnelMode(enum.Enum):
    GRE = 2
    GRETAP = 10
    IP6GRE = 8
    IP6GRETAP = 11
    IP6IP6 = 6
    IPIP = 1
    IPIP6 = 7
    ISATAP = 4
    SIT = 3
    UNKNOWN = 0
    VTI = 5
    VTI6 = 9

class KeyfileHandlerType(enum.Enum):
    WARN = 1
    WRITE_CERT = 2

class KeyfileWarnSeverity(enum.Enum):
    DEBUG = 1000
    INFO = 2000
    INFO_MISSING_FILE = 2901
    WARN = 3000

class ManagerError(enum.Enum):
    ALREADYASLEEPORAWAKE = 8
    ALREADYENABLEDORDISABLED = 9
    CONNECTIONALREADYACTIVE = 6
    CONNECTIONNOTACTIVE = 5
    CONNECTIONNOTAVAILABLE = 4
    DEPENDENCYFAILED = 7
    FAILED = 0
    INVALIDARGUMENTS = 12
    MISSINGPLUGIN = 13
    PERMISSIONDENIED = 1
    UNKNOWNCONNECTION = 2
    UNKNOWNDEVICE = 3
    UNKNOWNLOGDOMAIN = 11
    UNKNOWNLOGLEVEL = 10
    @staticmethod
    def quark() -> int: ...

class Metered(enum.Enum):
    GUESS_NO = 4
    GUESS_YES = 3
    NO = 2
    UNKNOWN = 0
    YES = 1

class RollbackResult(enum.Enum):
    ERR_DEVICE_UNMANAGED = 2
    ERR_FAILED = 3
    ERR_NO_DEVICE = 1
    OK = 0

class SecretAgentError(enum.Enum):
    AGENTCANCELED = 4
    FAILED = 0
    INVALIDCONNECTION = 2
    NOSECRETS = 5
    PERMISSIONDENIED = 1
    USERCANCELED = 3
    @staticmethod
    def quark() -> int: ...

class Setting8021xCKFormat(enum.Enum):
    PKCS12 = 3
    RAW_KEY = 2
    UNKNOWN = 0
    X509 = 1

class Setting8021xCKScheme(enum.Enum):
    BLOB = 1
    PATH = 2
    PKCS11 = 3
    UNKNOWN = 0

class SettingCompareFlags(enum.Enum):
    DIFF_RESULT_NO_DEFAULT = 64
    DIFF_RESULT_WITH_DEFAULT = 32
    EXACT = 0
    FUZZY = 1
    IGNORE_AGENT_OWNED_SECRETS = 8
    IGNORE_ID = 2
    IGNORE_NOT_SAVED_SECRETS = 16
    IGNORE_SECRETS = 4
    IGNORE_TIMESTAMP = 128

class SettingConnectionAutoconnectSlaves(enum.Enum):
    DEFAULT = -1
    NO = 0
    YES = 1

class SettingConnectionDnsOverTls(enum.Enum):
    DEFAULT = -1
    NO = 0
    OPPORTUNISTIC = 1
    YES = 2

class SettingConnectionDownOnPoweroff(enum.Enum):
    DEFAULT = -1
    NO = 0
    YES = 1

class SettingConnectionLldp(enum.Enum):
    DEFAULT = -1
    DISABLE = 0
    ENABLE_RX = 1

class SettingConnectionLlmnr(enum.Enum):
    DEFAULT = -1
    NO = 0
    RESOLVE = 1
    YES = 2

class SettingConnectionMdns(enum.Enum):
    DEFAULT = -1
    NO = 0
    RESOLVE = 1
    YES = 2

class SettingDiffResult(enum.Enum):
    IN_A = 1
    IN_A_DEFAULT = 4
    IN_B = 2
    IN_B_DEFAULT = 8
    UNKNOWN = 0

class SettingIP4LinkLocal(enum.Enum):
    AUTO = 1
    DEFAULT = 0
    DISABLED = 2
    ENABLED = 3

class SettingIP6ConfigAddrGenMode(enum.Enum):
    DEFAULT = 3
    DEFAULT_OR_EUI64 = 2
    EUI64 = 0
    STABLE_PRIVACY = 1

class SettingIP6ConfigPrivacy(enum.Enum):
    DISABLED = 0
    PREFER_PUBLIC_ADDR = 1
    PREFER_TEMP_ADDR = 2
    UNKNOWN = -1

class SettingMacRandomization(enum.Enum):
    ALWAYS = 2
    DEFAULT = 0
    NEVER = 1

class SettingMacsecMode(enum.Enum):
    EAP = 1
    PSK = 0

class SettingMacsecOffload(enum.Enum):
    DEFAULT = -1
    MAC = 2
    OFF = 0
    PHY = 1

class SettingMacsecValidation(enum.Enum):
    CHECK = 1
    DISABLE = 0
    STRICT = 2

class SettingMacvlanMode(enum.Enum):
    BRIDGE = 2
    PASSTHRU = 4
    PRIVATE = 3
    SOURCE = 5
    UNKNOWN = 0
    VEPA = 1

class SettingProxyMethod(enum.Enum):
    AUTO = 1
    NONE = 0

class SettingSerialParity(enum.Enum):
    EVEN = 1
    NONE = 0
    ODD = 2

class SettingTunMode(enum.Enum):
    TAP = 2
    TUN = 1
    UNKNOWN = 0

class SettingWirelessPowersave(enum.Enum):
    DEFAULT = 0
    DISABLE = 2
    ENABLE = 3
    IGNORE = 1

class SettingWirelessSecurityFils(enum.Enum):
    DEFAULT = 0
    DISABLE = 1
    OPTIONAL = 2
    REQUIRED = 3

class SettingWirelessSecurityPmf(enum.Enum):
    DEFAULT = 0
    DISABLE = 1
    OPTIONAL = 2
    REQUIRED = 3

class SettingsError(enum.Enum):
    FAILED = 0
    INVALIDARGUMENTS = 7
    INVALIDCONNECTION = 3
    INVALIDHOSTNAME = 6
    NOTSUPPORTED = 2
    NOTSUPPORTEDBYPLUGIN = 9
    PERMISSIONDENIED = 1
    READONLYCONNECTION = 4
    UUIDEXISTS = 5
    VERSIONIDMISMATCH = 8
    @staticmethod
    def quark() -> int: ...

class SriovEswitchEncapMode(enum.Enum):
    BASIC = 1
    NONE = 0
    PRESERVE = -1

class SriovEswitchInlineMode(enum.Enum):
    LINK = 1
    NETWORK = 2
    NONE = 0
    PRESERVE = -1
    TRANSPORT = 3

class SriovEswitchMode(enum.Enum):
    LEGACY = 0
    PRESERVE = -1
    SWITCHDEV = 1

class SriovVFVlanProtocol(enum.Enum): ...

class State(enum.Enum):
    ASLEEP = 10
    CONNECTED_GLOBAL = 70
    CONNECTED_LOCAL = 50
    CONNECTED_SITE = 60
    CONNECTING = 40
    DISCONNECTED = 20
    DISCONNECTING = 30
    UNKNOWN = 0

class Ternary(enum.Enum):
    DEFAULT = -1
    FALSE = 0
    TRUE = 1

class UtilsSecurityType(enum.Enum):
    DYNAMIC_WEP = 4
    INVALID = 0
    LEAP = 3
    NONE = 1
    OWE = 10
    SAE = 9
    STATIC_WEP = 2
    WPA2_ENTERPRISE = 8
    WPA2_PSK = 7
    WPA3_SUITE_B_192 = 11
    WPA_ENTERPRISE = 6
    WPA_PSK = 5

class VersionInfoCapability(enum.Enum):
    UNUSED = 2147483647

class VlanPriorityMap(enum.Enum):
    EGRESS_MAP = 1
    INGRESS_MAP = 0

class VpnConnectionState(enum.Enum):
    ACTIVATED = 5
    CONNECT = 3
    DISCONNECTED = 7
    FAILED = 6
    IP_CONFIG_GET = 4
    NEED_AUTH = 2
    PREPARE = 1
    UNKNOWN = 0

class VpnConnectionStateReason(enum.Enum):
    CONNECTION_REMOVED = 11
    CONNECT_TIMEOUT = 6
    DEVICE_DISCONNECTED = 3
    IP_CONFIG_INVALID = 5
    LOGIN_FAILED = 10
    NONE = 1
    NO_SECRETS = 9
    SERVICE_START_FAILED = 8
    SERVICE_START_TIMEOUT = 7
    SERVICE_STOPPED = 4
    UNKNOWN = 0
    USER_DISCONNECTED = 2

class VpnPluginError(enum.Enum):
    ALREADYSTARTED = 2
    ALREADYSTOPPED = 4
    BADARGUMENTS = 6
    FAILED = 0
    INTERACTIVENOTSUPPORTED = 9
    INVALIDCONNECTION = 8
    LAUNCHFAILED = 7
    STARTINGINPROGRESS = 1
    STOPPINGINPROGRESS = 3
    WRONGSTATE = 5
    @staticmethod
    def quark() -> int: ...

class VpnPluginFailure(enum.Enum):
    BAD_IP_CONFIG = 2
    CONNECT_FAILED = 1
    LOGIN_FAILED = 0

class VpnServiceState(enum.Enum):
    INIT = 1
    SHUTDOWN = 2
    STARTED = 4
    STARTING = 3
    STOPPED = 6
    STOPPING = 5
    UNKNOWN = 0

class WepKeyType(enum.Enum):
    KEY = 1
    PASSPHRASE = 2
    UNKNOWN = 0

class WimaxNspNetworkType(enum.Enum):
    HOME = 1
    PARTNER = 2
    ROAMING_PARTNER = 3
    UNKNOWN = 0
