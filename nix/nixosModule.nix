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
    enableUPowerService = mkEnableOption "Enables the UPower Service needed for retrieving battery information of devices";
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
      ignis = inputs.ignis.packages.${pkgs.stdenv.hostPlatform.system}.ignis.overrideAttrs (final: prev: {
        extraPackages = cfg.extraPythonPackages;
      });
    in{
      environment.systemPackages = [ ignis ];
      services = mkIf cfg.enableUPowerService {
        upower.enable = true;
      };
    }
  );
}
