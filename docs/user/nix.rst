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

outputs can be added in different ways.
Don't forget to pass ``inputs``
to ``extraSpecialArgs`` for Home Manager
or ``specialArgs`` for NixOS host configuration

Then add the following to ``environment.systemPackages`` or ``home.packages``:

.. code-block:: nix

    inputs.ignis.packages.${system}.ignis


Overriding
----------

Sometimes you may need to add extra dependencies.

Use the ``<pkg>.override`` function for this.

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


Tips
--------

Adding Ignis to system Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can make Ignis accessible for the system python interpreter.
This is especially useful if the LSP server of your text editor is not able to find Ignis.

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
    it won't find extra dependencies.


The basic Flake example
^^^^^^^^^^^^^^^^^^^^^^^

**flake.nix**

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
          inputs.nixpkgs.follows = "nixpkgs";
        };
      };

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

