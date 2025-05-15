{ self
, lib
, wrapGAppsHook4
, pkg-config
, meson
, ninja
, git
, glib
, gtk4
, gtk4-layer-shell
, gobject-introspection
, librsvg
, python312Packages
, gvc
, extraPackages ? []
, version ? "git"
}:
  let
    inherit (lib)
      licenses
      platforms
    ;
    inherit (python312Packages)
      buildPythonPackage
      pygobject3
      pycairo
      click
      loguru
    ;
  in buildPythonPackage {

  inherit version;
  pname = "ignis";
  src = "${self}";

  format = "other";

  nativeBuildInputs = [
    pkg-config
    meson
    ninja
    git
    gobject-introspection
    wrapGAppsHook4
  ];

  dependencies = extraPackages ++ [
    glib
    gtk4
    gtk4-layer-shell
    gobject-introspection
    librsvg

    pygobject3
    pycairo
    click
    loguru
  ];

  lib.debug.traceVal dependencies

  patchPhase = ''
    mkdir -p ./subprojects/gvc
    cp -r ${gvc}/* ./subprojects/gvc
  '';

  mesonFlags = [
    "-DCOMMITHASH=${self.rev or "dirty"}"
  ];

  #? avoid double wrapping. we manually pass args to wrapper
  dontWrapGApps = true;
  preFixup = ''
    makeWrapperArgs+=(
      "''${gappsWrapperArgs[@]}"
      --set LD_LIBRARY_PATH "$out/lib:${gtk4-layer-shell}/lib:$LD_LIBRARY_PATH"
    )
  '';

  meta = {
    description = ''
      A widget framework for building desktop shells,
      written and configurable in Python.
    '';
    homepage = "https://github.com/linkfrg/ignis";
    changelog = "https://github.com/linkfrg/ignis/releases";
    license = licenses.lgpl21Plus;
    platforms = platforms.linux;
    maintainers = [ ];
    mainProgram = "ignis";
  };
}