{
  lib,
  dart-sass,
  fetchFromGitHub,
  git,
  glib,
  gnome-bluetooth,
  gst_all_1,
  gtk4,
  gtk4-layer-shell,
  gobject-introspection,
  libpulseaudio,
  librsvg,
  makeWrapper,
  meson,
  networkmanager,
  ninja,
  pipewire,
  pkg-config,
  python3,
  stdenv,
  rev ? "dirty",
  version ? "git",
  ...
}:

let
  inherit (builtins) concatStringsSep;

  python = python3.withPackages (
    ps: with ps; [
      click
      loguru
      pycairo
      pygobject3
    ]
  );

  gvc = fetchFromGitHub {
    owner = "linkfrg";
    repo = "libgnome-volume-control-wheel";
    rev = "2d1cb33dacdae43127bb843a48b159ea7b8925d0";
    hash = "sha256-ikF9EzFlsRH8i4+SVUHETF4Jk1ob2JX1RLsuMdzrQOQ=";
  };
in
stdenv.mkDerivation {
  inherit version;

  pname = "ignis";

  src = ./..;

  nativeBuildInputs = [
    git
    makeWrapper
    meson
    ninja
    pkg-config
    python
  ];

  buildInputs =
    [
      dart-sass
      glib
      gtk4
      gtk4-layer-shell
      libpulseaudio
      pipewire
    ]
    ++ (with gst_all_1; [
      gstreamer
      gst-plugins-base
      gst-plugins-good
      gst-plugins-bad
      gst-plugins-ugly
    ])
    ++ (with python.pkgs; [
      click
      pycairo
      pygobject3
    ]);

  patchPhase = ''
    mkdir -p ./subprojects/gvc
    cp -r ${gvc}/* ./subprojects/gvc

    substituteInPlace bin/ignis \
      --replace '/usr/bin/env python3' ${python.interpreter}
  '';

  buildPhase = ''
    runHook preBuild

    cd ..
    meson setup build --prefix="$out" -DCOMMITHASH="${rev}"
    ninja -C build

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    ninja -C build install
    wrapProgram $out/bin/ignis \
      --prefix-each PATH ":" "${gst_all_1.gstreamer}/bin ${dart-sass}/bin" \
      --prefix-each PYTHONPATH : "$out/${python.sitePackages} ${python}/${python.sitePackages}" \
      --set GI_TYPELIB_PATH "$out/lib:${
        concatStringsSep ":" (
          map (pkg: "${pkg}/lib/girepository-1.0") [
            glib
            gobject-introspection
            networkmanager
            gst_all_1.gstreamer
            gnome-bluetooth
          ]
        )
      }:$GI_TYPELIB_PATH" \
      --set LD_LIBRARY_PATH "$out/lib:${gtk4-layer-shell}/lib:${glib}/lib:$LD_LIBRARY_PATH" \
      --set GST_PLUGIN_PATH "${
        concatStringsSep ":" (
          map (pkg: "${pkg}/lib/gstreamer-1.0") [
            gst_all_1.gst-plugins-base
            gst_all_1.gst-plugins-good
            gst_all_1.gst-plugins-bad
            gst_all_1.gst-plugins-ugly
            pipewire
          ]
        )
      }:$GST_PLUGIN_PATH" \
      --set GDK_PIXBUF_MODULE_FILE "$(echo ${librsvg.out}/lib/gdk-pixbuf-2.0/*/loaders.cache)"

    runHook postInstall
  '';

  meta = {
    description = "A widget framework for building desktop shells, written and configurable in Python";
    homepage = "https://github.com/linkfrg/ignis";
    changelog = "https://github.com/linkfrg/ignis/releases/tag/v${version}";
    license = lib.licenses.gpl3;
    mainProgram = "ignis";
  };
}
