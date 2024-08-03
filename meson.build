project(
    'ignis',
    version: '0.1',
    license: 'GPL-3.0-only',
    default_options: ['warning_level=2', 'werror=false']
)


# Find Python installation
python = import('python').find_installation()

# Set folders
prefix = get_option('prefix')
datadir = join_paths(prefix, get_option('datadir'))
libdir = join_paths(prefix, get_option('libdir'))
bindir = get_option('bindir')

pylibdir = python.get_install_dir()

pkgdatadir = join_paths(datadir, meson.project_name())

pkginstalldir = join_paths(pylibdir, meson.project_name())

# Dependencies
dependency('glib-2.0')
dependency('gobject-introspection-1.0')
dependency('gio-2.0')
dependency('gtk4')
dependency('pygobject-3.0')
dependency('gtk4-layer-shell-0')

# gvc
subproject('gvc',
    default_options: [
        'package_name=' + meson.project_name(),
        'pkgdatadir=' + pkgdatadir,
        'pkglibdir=' + libdir,
        'static=false',
        'introspection=true',
        'alsa=false'
    ]
)

# Do installation
install_data(
    files('bin/ignis'),
    install_dir: bindir,
    install_mode: 'rwxr-xr-x',
)

install_subdir(
    'ignis',
    install_dir: pylibdir,
)

config = configuration_data()
config.set('LIBDIR', libdir)
config.set('VERSION', meson.project_version())
config.set('COMMIT', run_command('git', 'rev-parse', 'HEAD').stdout().strip())

configure_file(
    input: 'ignis/__init__.py.in',
    output: '__init__.py',
    configuration: config,
    install_dir: pkginstalldir
)

configure_file(
    input: 'ignis/version.py.in',
    output: 'version.py',
    configuration: config,
    install_dir: pkginstalldir
)