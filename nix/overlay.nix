{ self, version }: final: prev: {
  ignis = prev.callPackage ./ignis.nix { inherit self; inherit version; };
}
