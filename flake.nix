{
  description = "Flake for build ignis";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [
        "aarch64-linux"
        "x86_64-linux"
      ];

      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;

      version = import ./nix/version.nix { inherit self; };
    in
    {
      overlays.default = import ./nix/overlay.nix { inherit version; };

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
