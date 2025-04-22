Nix
============


Installation
------------


.. warning::
    This will install the latest (git) version of Ignis.
    Please refer to the `latest documentation <https://linkfrg.github.io/ignis/latest/index.html>`_.

Add Ignis to your flake's inputs:

.. code-block:: nix

    {
      inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
        home-manager = {
          url = "github:nix-community/home-manager";
          inputs.nixpkgs.follows = "nixpkgs";
        };
        ignis = {
          url = "github:linkfrg/ignis";
          # ! impotant for override
          # NIX won't allow override dependencies if the input data
          # doesn't follow your system pkgs
          inputs.nixpkgs.follows = "nixpkgs";
        };
      };
    }

Output data can be added in different ways.
In the example below, the home manager is installed as a NixOS module

Don't forget to pass ``inputs``
to ``extraSpecialArgs`` for Home Manager
or ``specialArgs`` for NixOS host configuration

.. code-block:: nix

    {
      outputs = { self, nixpkgs, home-manager, ... }@inputs: let
        system = "x86_64-linux";
        lib = nixpkgs.lib;
        extraSpecialArgs = { inherit system inputs; };  # <- passing inputs to the attribute set for home-manager
        specialArgs = { inherit system inputs; };       # <- passing inputs to the attribute set for NixOS
      in {
        nixosConfigurations = {
          dummy-hostname = lib.nixosSystem {
            modules = [
              inherit specialArgs;  # <- this will make inputs available anywhere in the NixOS configuration
              ./path/to/configuration.nix
              home-manager.nixosModules.home-manager {
                home-manager = {
                  inherit extraSpecialArgs;  # <- this will make inputs available anywhere in the HM configuration
                  useGlobalPkgs = true;
                  useUserPackages = true;
                  users.yourUserName = import ./path/to/home.nix;
                };
              }
            ];
          };
        };
      };
    }

Then add the following to ``environment.systemPackages`` or ``home.packages``:

.. code-block:: nix

    inputs.ignis.packages.${system}.ignis


Overriding
----------

Sometimes you may need to add extra dependencies.

Use a function ``<pkg>.override`` for this.
You can read more about this function `here <https://ryantm.github.io/nixpkgs/using/overrides/>`_.

For example, in the ``~/.config/ignis/config.py`` you use the following python packages

* psutil
* jinja2
* pillow
* materialyoucolor

By adding Ignis to the system configuration, override the list of extraPackages

The derivation of ignis pkg has special input arg ``extraPackages ? []``

**configuration.nix**

.. code-block:: nix

    { config, pkgs, lib, inputs, ... }: {
    # snip ...
      environment.systemPackages = [
        (inputs.ignis.packages.${pkgs.stdenv.hostPlatform.system}.ignis.override {
          extraPackages = [
            pkgs.python312Packages.psutil
            pkgs.python312Packages.jinja2
            pkgs.python312Packages.pillow
            pkgs.python312Packages.materialyoucolor
            # add more dependencies here ...
          ];
        })
        pkgs.firefox
        pkgs.neovim
        # add more pkgs here ...
      ];
    # snip ...
    }

If you are using home-manager

**home.nix**

.. code-block:: nix

    { config, pkgs, lib, inputs, ... }: {
    # snip ...
      home.packages = [
        (inputs.ignis.packages.${pkgs.stdenv.hostPlatform.system}.ignis.override {
          extraPackages = [
            pkgs.python312Packages.psutil
            pkgs.python312Packages.jinja2
            pkgs.python312Packages.pillow
            pkgs.python312Packages.materialyoucolor
            # add more dependencies here ...
          ];
        })
        pkgs.firefox
        pkgs.neovim
        # add more pkgs here ...
      ];
    # snip ...
    }


.. hint::
    You can even add Ignis with extra dependencies to your system ``Python``

It can be useful if the LSP server of your favorite text editor can't find Ignis modules


**home.nix**

.. code-block:: nix

    { config, pkgs, inputs, ... }: {
      # snip ...
      home.packages = with pkgs; [
        (python3.withPackages(ps: with ps; [
          (inputs.ignis.packages.${pkgs.stdenv.hostPlatform.system}.ignis.override {
            extraPackages = [
              pkgs.python312Packages.psutil
              pkgs.python312Packages.jinja2
              pkgs.python312Packages.pillow
              pkgs.python312Packages.materialyoucolor
            ];
          })
        ]))
      ];
      # snip ...
    }


.. warning::
    Please remember you need to choose one of the described methods.
    If you add Ignis as a package don't add it to the system ``Python``.
    You may face the fact that when Ignis is launched,
    it won't find extra dependencies


Tips and tricks
---------------

Some services such as ``upower``, ``hyprland``
expect that they are already present in the system.
You need to take care of their launch yourself.

For example, to use ``upower`` add the following to your configuration

**configuration.nix**

.. code-block:: nix

    services.upower.enable = true;


