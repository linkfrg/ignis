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
    enable = mkEnableOption "Enable the Ignis widget framework";
    enableBluetoothService = mkOption {
      type = types.bool;
      default = true;
      description = "Enable the Bluetooth Service";
    };
    enableUPowerService = mkOption {
      type = types.bool;
      default = true;
      description = "Enable the UPower Service";
    };
    enableRecorderService = mkOption {
      type = types.bool;
      default = true;
      description = "Enable the Recorder Service";
    };
    enableNetworkService = mkOption {
      type = types.bool;
      default = true;
      description = "Enable the Network Service";
    };
    enableAudioService = mkOption {
      type = types.bool;
      default = true;
      description = "Enable the Audio Service";
    };
    enableSassCompilation = mkOption {
      type = types.bool;
      default = true;
      description = "Enable Sass compilation support";
    };
    extraPackages = mkOption {
      type = types.listOf types.package;
      default = [ ];
      example = [ pkgs.python312Packages.psutil ];
      description = ''
        Extra packages to be added to the PATH.
        This is useful for adding python packages that are needed by ignis
      '';
    };
  };

  config = mkIf cfg.enable (
    let
      tempPackages = [
        pkgs.bluez
        pkgs.gnome-bluetooth
        pkgs.libpulseaudio
      ];
      ignis =
        (inputs.ignis.packages.${pkgs.stdenv.hostPlatform.system}.ignis.overrideAttrs (
          final: prev: {
            mesonFlags = prev.mesonFlags ++ lib.optionals (!cfg.enableAudioService) [ "-Dbuild_gvc=false" ];
            serviceDepencies = lib.optionals cfg.enableBluetoothService [
                pkgs.bluez
                pkgs.gnome-bluetooth
              ]
              ++ lib.optionals cfg.enableRecorderService [
                pkgs.pipewire
                pkgs.gst_all_1.gstreamer
                pkgs.gst_all_1.gst-plugins-base
                pkgs.gst_all_1.gst-plugins-good
                pkgs.gst_all_1.gst-plugins-bad
                pkgs.gst_all_1.gst-plugins-ugly
              ]
              ++ lib.optionals cfg.enableNetworkService [ pkgs.networkmanager ]
              ++ lib.optionals cfg.enableAudioService [ pkgs.libpulseaudio ]
              ++ lib.optionals cfg.enableSassCompilation [ pkgs.dart-sass ];
          }
        )).override
          {
            extraPackages = cfg.extraPackages;
          };
    in
    {
      environment.systemPackages = [ ignis ];
      services.upower = mkIf cfg.enableUPowerService {
        enable = true;
      };
    }
  );
}
