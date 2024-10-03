project(
    'ignis',
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
install_subdir(
    'ignis',
    install_dir: pylibdir,
)

config = configuration_data()
config.set('LIB_DIR', libdir)
config.set('COMMIT', run_command('git', 'rev-parse', 'HEAD').stdout().strip())
config.set('BRANCH', run_command('git', 'branch', '--show-current').stdout().strip())
config.set('COMMIT_MSG', run_command('git', 'log', '-1', '--pretty=%B').stdout().strip())

install_data(
    files('bin/ignis'),
    install_dir: bindir,
    install_mode: 'rwxr-xr-x',
)

configure_file(
    input: 'ignis/__commit__.py.in',
    output: '__commit__.py',
    configuration: config,
    install_dir: pkginstalldir
)

configure_file(
    input: 'ignis/__lib_dir__.py.in',
    output: '__lib_dir__.py',
    configuration: config,
    install_dir: pkginstalldir
)