{ self
, lib
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
, version ? "git"
}:
  let
    inherit (lib)
      concatStringsSep
      licenses
      platforms
      maintainers
    ;
    inherit (python312Packages)
      buildPythonPackage
      pygobject3
      pycairo
      click
      charset-normalizer
      markupsafe
      loguru
      certifi
      idna
      urllib3
    ;
    inherit (gst_all_1)
      gstreamer
      gst-plugins-base
      gst-plugins-good
      gst-plugins-bad
      gst-plugins-ugly
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
  ];

  dependencies = extraPackages ++ [
    glib
    gtk4
    gtk4-layer-shell
    gobject-introspection
    dart-sass
    gstreamer
    libpulseaudio
    pipewire
    networkmanager
    gnome-bluetooth

    pygobject3
    pycairo
    click
    charset-normalizer
    markupsafe
    loguru
    certifi
    idna
    urllib3

  ];

  patchPhase = ''
    mkdir -p ./subprojects/gvc
    cp -r ${gvc}/* ./subprojects/gvc
  '';

  buildPhase = ''
    cd ..
    meson setup build --prefix=$out -DCOMMITHASH=${self.rev or "dirty"}
    ninja -C build
  '';

  installPhase = ''
    ninja -C build install
  '';

  makeWrapperArgs = [
    ''--set GI_TYPELIB_PATH "$out/lib:${concatStringsSep ":" (map (pkg: "${pkg}/lib/girepository-1.0") [
        glib
        gobject-introspection
        gstreamer
        networkmanager
        gnome-bluetooth
    ])}:$GI_TYPELIB_PATH"''
    ''--set LD_LIBRARY_PATH "$out/lib:${gtk4-layer-shell}/lib:${glib}/lib:$LD_LIBRARY_PATH"''
    ''--set GST_PLUGIN_PATH "${concatStringsSep ":" (map (pkg: "${pkg}/lib/gstreamer-1.0") [
        gst-plugins-base
        gst-plugins-good
        gst-plugins-bad
        gst-plugins-ugly
        pipewire
    ])}:$GST_PLUGIN_PATH"''
    ''--set GDK_PIXBUF_MODULE_FILE "$(echo ${librsvg.out}/lib/gdk-pixbuf-2.0/*/loaders.cache)"''
  ];

  meta = {
    description = ''
      A widget framework for building desktop shells,
      written and configurable in Python.
    '';
    homepage = "https://github.com/linkfrg/ignis";
    changelog = "https://github.com/linkfrg/ignis/releases";
    license = licenses.gpl3;
    platforms = platforms.linux;
    maintainers = with maintainers; [ frdiener somokill ];
    mainProgram = "ignis";
  };
}