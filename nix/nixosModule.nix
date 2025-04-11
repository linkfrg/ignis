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
    extraPythonPackages = lib.mkOption {
      type = types.listOf types.package;
      default = [ ];
      example = [ pkgs.python312Packages.psutil ];
      description = ''
        Extra python packages to be added to the PATH.
        This is useful for adding python packages that are not needed by ignis
      '';
    };
  };

  config = mkIf cfg.enable {
    nixpkgs.overlays = [
      (prev: final: {
        ignis = final.callPackage ./ignis.nix { inherit self; inherit version; extraPythonPackages = cfg.extraPythonPackages; };
      })
    ];

    environment.systemPackages = [ pkgs.ignis ];
    services.upower.enable = true;
  };
}
