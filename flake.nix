{
  description = ''
    Flake for build ignis.
    ignis is a widget framework for building desktop shells,
    written and configurable in Python. 
  '';

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    gvc = {
      url = "github:linkfrg/libgnome-volume-control-wheel";
      flake = false; 
    };
  };

  outputs = { self, nixpkgs, gvc }:
    let
      supportedSystems = [
        "aarch64-linux"
        "x86_64-linux"
      ];

      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;

      version = import ./nix/version.nix { inherit self; };
    in
    {
      overlays.default = import ./nix/overlay.nix { inherit self gvc version; };

      packages = forAllSystems (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [
              self.overlays.default
            ];
          };
        in
        {
          inherit (pkgs) ignis;

          default = self.packages.${system}.ignis;
        }
      );
    };
}
