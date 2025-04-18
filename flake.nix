{
  description = "A widget framework for building desktop shells, written and configurable in Python";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      supportedSystems = [
        "aarch64-linux"
        "x86_64-linux"
      ];

      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;

      version = import ./nix/version.nix { inherit self; };
    in
    {
      overlays.default = final: prev: {
        ignis = prev.callPackage ./nix/ignis.nix {
          inherit version;
          rev = self.rev or "dirty";
        };
      };

      packages = forAllSystems (
        system:
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
