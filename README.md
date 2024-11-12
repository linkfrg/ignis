# Ignis

[![docs](https://github.com/linkfrg/ignis/actions/workflows/latest_docs.yaml/badge.svg)](https://github.com/linkfrg/ignis/actions/workflows/latest_docs.yaml)

__Ignis is a Python framework for building desktop shells using GTK4.__

## Features
- Configured in Python
- Uses GTK4
- Provides built-in services to interact with various parts of your system
- Working with widgets is easier than in pure PyGObject

> [!NOTE]
> Ignis is still a work in progress.
> API is a subject to change.

## Getting started
See [Documentation](https://linkfrg.github.io/ignis)

## Supported Desktops
- wlroots-based Wayland compositors (e.g., __Sway__) 
- __Hyprland__
- Smithay based compositors (e.g., __COSMIC__)
- __KDE Plasma__ on wayland

and all other compositors that implement the Layer Shell protocol.

## Examples
* A simple bar, see [examples](./examples/bar)
![simple-bar](./examples/bar/simple-bar.png)

* [My own configuration](https://github.com/linkfrg/dotfiles/)
![My own configuration](https://github.com/linkfrg/dotfiles/blob/main/assets/1.png?raw=true)


## Contributing
Check out the [Developer Guide](https://linkfrg.github.io/ignis/latest/dev/index.html)

## Special Thanks

[AGS](https://github.com/aylur/ags) - For inspiration
