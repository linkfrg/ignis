{ 
  self,
  lib,
  stdenv,
  pkg-config,
  meson,
  ninja,
  git,
  makeWrapper,
  glib,
  gtk4,
  gtk4-layer-shell,
  libpulseaudio,
  python312Packages,
  gst_all_1,
  pipewire,
  dart-sass,
  gobject-introspection,
  networkmanager,
  gnome-bluetooth,
  librsvg,
  gvc,
  version ? "git"
}:
  let
    inherit (lib)
      concatStringsSep
      licenses
      platforms
      maintainers;
  in stdenv.mkDerivation {

  inherit version;
  pname = "ignis";
  src = "${self}";

  nativeBuildInputs = [
    pkg-config
    meson
    ninja
    git
    makeWrapper
  ];

  buildInputs = [
    glib
    gtk4
    gtk4-layer-shell
    libpulseaudio
    python312Packages.pygobject3
    python312Packages.pycairo
    python312Packages.click
    python312Packages.charset-normalizer
    gst_all_1.gstreamer
    gst_all_1.gst-plugins-base
    gst_all_1.gst-plugins-good
    gst_all_1.gst-plugins-bad
    gst_all_1.gst-plugins-ugly
    pipewire
    dart-sass
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
    wrapProgram $out/bin/ignis \
      --prefix-each PATH ":" "${gst_all_1.gstreamer}/bin ${dart-sass}/bin" \
      --set PYTHONPATH "${concatStringsSep ":" (map (pkg: "${pkg}/lib/python3.12/site-packages") [
        python312Packages.markupsafe
        python312Packages.pygobject3
        python312Packages.pycairo
        python312Packages.loguru
        python312Packages.certifi
        python312Packages.idna
        python312Packages.urllib3
        python312Packages.click
        python312Packages.charset-normalizer
      ])}:$out/lib/python3.12/site-packages:$PYTHONPATH" \
      --set GI_TYPELIB_PATH "$out/lib:${concatStringsSep ":" (map (pkg: "${pkg}/lib/girepository-1.0") [
        glib
        gobject-introspection
        networkmanager
        gst_all_1.gstreamer
        gnome-bluetooth
      ])}:$GI_TYPELIB_PATH" \
      --set LD_LIBRARY_PATH "$out/lib:${gtk4-layer-shell}/lib:${glib}/lib:$LD_LIBRARY_PATH" \
      --set GST_PLUGIN_PATH "${concatStringsSep ":" (map (pkg: "${pkg}/lib/gstreamer-1.0") [
        gst_all_1.gst-plugins-base
        gst_all_1.gst-plugins-good
        gst_all_1.gst-plugins-bad
        gst_all_1.gst-plugins-ugly
        pipewire
      ])}:$GST_PLUGIN_PATH" \
      --set GDK_PIXBUF_MODULE_FILE "$(echo ${librsvg.out}/lib/gdk-pixbuf-2.0/*/loaders.cache)"
  '';

  meta = {
    description = ''
      A widget framework for building desktop shells,
      written and configurable in Python.
    '';
    homepage = "https://github.com/linkfrg/ignis";
    changelog = "https://github.com/linkfrg/ignis/releases/tag/v${version}";
    license = licenses.gpl3;
    platforms = platforms.linux;
    maintainers = with maintainers; [ frdiener somokill MOIS3Y];
    mainProgram = "ignis";
  };
}
