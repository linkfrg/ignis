{ self, version, gvc }: final: prev: {
  ignis = prev.callPackage ./ignis.nix { inherit self gvc version; };
}
