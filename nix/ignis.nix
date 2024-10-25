{ pkgs, version ? "git", ... }:
let
  inherit (pkgs.lib) concatStringsSep;
in
pkgs.stdenv.mkDerivation {
  inherit version;

  pname = "ignis";

  src = ./..;

  nativeBuildInputs = [
    pkgs.pkg-config
    pkgs.meson
    pkgs.ninja
    pkgs.git
    pkgs.makeWrapper
  ];

  buildInputs = [
    pkgs.glib
    pkgs.gtk4
    pkgs.gtk4-layer-shell
    pkgs.libpulseaudio
    pkgs.python312Packages.pygobject3
    pkgs.python312Packages.pycairo
    pkgs.python312Packages.click
    pkgs.python312Packages.charset-normalizer
  ];

  runtimeInputs = [
    pkgs.gst_all_1.gstreamer
    pkgs.gst_all_1.gst-plugins-base
    pkgs.dart-sass
  ];

  patchPhase = ''
    substituteInPlace ignis/utils/sass.py \
      --replace-fail '/bin/sass' '${pkgs.dart-sass}/bin/sass'
  '';

  buildPhase = ''
    cd ..
    meson setup build --prefix=$out --libdir=lib/ignis
    ninja -C build
  '';

  installPhase = ''
    ninja -C build install
    wrapProgram $out/bin/ignis \
      --set PATH "${pkgs.gst_all_1.gstreamer}/bin:${pkgs.dart-sass}/bin:$PATH" \
      --set PYTHONPATH "${concatStringsSep ":" (map (pkg: "${pkg}/lib/python3.12/site-packages") [
        pkgs.python312Packages.markupsafe
        pkgs.python312Packages.pygobject3
        pkgs.python312Packages.pycairo
        pkgs.python312Packages.loguru
        pkgs.python312Packages.certifi
        pkgs.python312Packages.idna
        pkgs.python312Packages.urllib3
        pkgs.python312Packages.requests
        pkgs.python312Packages.click
        pkgs.python312Packages.charset-normalizer
      ])}:$out/lib/python3.12/site-packages:$PYTHONPATH" \
      --set GI_TYPELIB_PATH "$out/lib:${concatStringsSep ":" (map (pkg: "${pkg}/lib/girepository-1.0") [
        pkgs.glib
        pkgs.gobject-introspection
        pkgs.networkmanager
        pkgs.gobject-introspection-unwrapped
        pkgs.gst_all_1.gstreamer
        pkgs.gst_all_1.gst-plugins-base
        pkgs.gst_all_1.gst-plugins-ugly
      ])}:$GI_TYPELIB_PATH" \
      --set LD_LIBRARY_PATH "$out/lib:${pkgs.gtk4-layer-shell}/lib:${pkgs.glib}/lib:$LD_LIBRARY_PATH" \
      --set GST_PLUGIN_PATH "${concatStringsSep ":" (map (pkg: "${pkg}/lib/gstreamer-1.0") [
        pkgs.gst_all_1.gst-plugins-base
        pkgs.gst_all_1.gst-plugins-good
        pkgs.gst_all_1.gst-plugins-ugly
      ])}:$GST_PLUGIN_PATH"
  '';

  meta = with pkgs.lib; {
    description = "Full-featured Python framework for building desktop shells using GTK4";
    homepage = "https://github.com/linkfrg/ignis";
    changelog = "https://github.com/linkfrg/ignis/releases/tag/v${version}";
    license = licenses.gpl3;
    maintainers = with maintainers; [ frdiener somokill ];
    mainProgram = "ignis";
  };
}
