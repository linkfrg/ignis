{
  inputs,
  lib,
  pkgs,
  config,
  ...
}:
with lib;
let
  cfg = config.programs.ignis;
in
{
  options.programs.ignis = {
    enable = mkEnableOption "Enable the Ignis widget framework.";
    enableBluetoothService = mkEnableOption "Enables all dependencies needed for the Bluetooth Service";
    enableUPowerService = mkEnableOption "Enables all dependencies needed for the UPower Service";
    enableRecorderService = mkEnableOption "Enables all dependencies needed for the Recorder Service";
    enableNetworkService = mkEnableOption "Enables all dependencies needed for the Network Service";
    enableAudioService = mkEnableOption "Enables all dependencies needed for the Audio Service";
    enableSassCompilation = mkEnableOption "Enables Sass compilation";
    extraPythonPackages = lib.mkOption {
      type = types.listOf types.package;
      default = [ ];
      example = [ pkgs.python312Packages.psutil ];
      description = ''
        Extra python packages to be added to the PATH.
        This is useful for adding python packages that are needed by ignis
      '';
    };
  };

  config = mkIf cfg.enable (
    let
      # tempPackages = cfg.extraPythonPackages ++ [
      #   pkgs.bluez
      #   pkgs.gnome-bluetooth
      # ];
      # ++ lib.optionals cfg.enableRecorderService [
      #   pkgs.pipewire
      #   pkgs.gst_all_1.gstreamer
      #   pkgs.gst_all_1.gst-plugins-base
      #   pkgs.gst_all_1.gst-plugins-good
      #   pkgs.gst_all_1.gst-plugins-bad
      #   pkgs.gst_all_1.gst-plugins-ugly
      # ]
      # ++ lib.optionals cfg.enableNetworkService [ pkgs.networkmanager ]
      # ++ lib.optionals cfg.enableAudioService [ pkgs.libpulseaudio ]
      # ++ lib.optionals cfg.enableSassCompilation [ pkgs.dart-sass ];

      ignis = inputs.ignis.packages.${pkgs.stdenv.hostPlatform.system}.ignis.overrideAttrs (
        final: prev: {
          extraPackages = cfg.extraPythonPackages ++ [
            pkgs.bluez
            pkgs.gnome-bluetooth
          ]       
          ++ lib.optionals cfg.enableNetworkService [ pkgs.networkmanager ]
      ++ lib.optionals cfg.enableAudioService [ pkgs.libpulseaudio ]
      ++ lib.optionals cfg.enableSassCompilation [ pkgs.dart-sass ];
          mesonFlags = prev.mesonFlags ++ lib.optionals (!cfg.enableAudioService) [ "-Dbuild_gvc=false" ];
        }
      );
    in
    {
      environment.systemPackages = [ ignis ];
      services.upower = mkIf cfg.enableUPowerService {
        enable = true;
      };
    }
  );
}
