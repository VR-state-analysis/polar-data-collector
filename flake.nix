{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }@attrs:
    flake-utils.lib.eachSystem flake-utils.lib.defaultSystems (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in rec {
        devShells.default = pkgs.mkShell { buildInputs = with pkgs; [
          (python3.withPackages (ps: with ps; [
            pyside6
          ]))
          black
        ];
      };
        packages.server = pkgs.buildGoModule {
          pname = "polar-data-collector";
          name = "polar-data-collector";
          src = ./server;
          vendorHash = "sha256-WA7PLEaT7lpBkIQHXbRSrQO7mfip4mRS7xMck6lVAFs=";
        };
      });
}

