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
, dart-sass
, libpulseaudio
, pipewire
, networkmanager
, gnome-bluetooth
, python312Packages
, gst_all_1
, gvc
, extraPackages ? []
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
    inherit (gst_all_1)
      gstreamer
      gst-plugins-base
      gst-plugins-good
      gst-plugins-bad
      gst-plugins-ugly
    ;
    version = import ./version.nix { inherit self; };
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
    dart-sass
    gstreamer
    gst-plugins-base
    gst-plugins-good
    gst-plugins-bad
    gst-plugins-ugly
    librsvg
    libpulseaudio
    pipewire
    networkmanager
    gnome-bluetooth

    pygobject3
    pycairo
    click
    loguru
  ];

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
      "${gappsWrapperArgs[@]}"
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