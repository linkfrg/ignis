{
  self,
  gvc,
  ...
}:
{
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
    enableAdditionalServices = mkEnableOption "Enable additional services (e.g. the Upower service, to get battery status of devices and bluetooth devices.)";
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

  config = mkIf cfg.enable {
    nixpkgs.overlays = [
      (prev: final: {
        ignis = final.callPackage ./default.nix {
          inherit self gvc;
          extraPackages = cfg.extraPythonPackages;
        };
      })
    ];

    environment.systemPackages = [ pkgs.ignis ];
    services = mkIf cfg.enableAdditionalServices {
      upower.enable = true;
    };
  };
}
