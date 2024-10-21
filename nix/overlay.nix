{ version }: final: prev: {
  ignis = prev.callPackage ./ignis.nix { inherit version; };
}
