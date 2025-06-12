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
    services = {
      bluetooth = lib.mkEnableOption "Whether to enable upower";
      upower = lib.mkEnableOption "Enable UPower service";
      recorder = lib.mkEnableOption "Enable Recorder service";
      network = lib.mkEnableOption "Enable Network service";
      audio = lib.mkEnableOption "Enable Audio service";
    };
    enableSassCompilation = lib.mkEnableOption "Enable Sass compilation support";
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
      ignis =
        (inputs.ignis.packages.${pkgs.stdenv.hostPlatform.system}.ignis.overrideAttrs (
          final: prev: {
            mesonFlags = prev.mesonFlags ++ lib.optionals (!cfg.services.audio) [ "-Dbuild_gvc=false" ];
          }
        )).override
          {
            extraPackages = cfg.extraPackages;
            serviceDependencies = lib.optionals cfg.services.bluetooth [
                pkgs.bluez
                pkgs.gnome-bluetooth
              ]
              ++ lib.optionals cfg.services.recorder [
                pkgs.pipewire
                pkgs.gst_all_1.gstreamer
                pkgs.gst_all_1.gst-plugins-base
                pkgs.gst_all_1.gst-plugins-good
                pkgs.gst_all_1.gst-plugins-bad
                pkgs.gst_all_1.gst-plugins-ugly
              ]
              ++ lib.optionals cfg.services.network [ pkgs.networkmanager ]
              ++ lib.optionals cfg.services.audio [ pkgs.libpulseaudio ]
              ++ lib.optionals cfg.enableSassCompilation [ pkgs.dart-sass ];
          };
    in
    {
      environment.systemPackages = [ ignis ];
      assertions = [
        {
          assertion = !(cfg.services.bluetooth && !(hardware.bluetooth.enable));
          message = "To use bluetooth services of ignis you must put 'hardware.bluetooth.enable = true' in your configuration";
        }
        {
          assertion = !(cfg.services.upower && !(services.upower.enable));
          message = "To use upower services of ignis you must put 'services.upower.enable = true' in your configuration";
        }
        {
          assertion = !(cfg.services.recorder && !(services.pipewire.enable));
          message = "To use recorder services of ignis you must put 'services.pipewire.enable = true' in your configuration";
        }
        {
          assertion = !(cfg.services.network && !(networking.networkmanager.enable));
          message = "To use network services of ignis you must put 'networking.networkmanager.enable = true' in your configuration";
        }
        {
          assertion = !(cfg.services.audio && !(services.pipewire.enable));
          message = "To use audio services of ignis you must put 'services.pipewire.enable = true' in your configuration";
        }
      ];
    }
  );
}
