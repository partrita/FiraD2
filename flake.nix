{
  description = "A flake for building FiraD2 fonts";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in
    {
      devShells.x86_64-linux.default = pkgs.mkShell {
        buildInputs = [
          pkgs.fontforge
          pkgs.python3
          pkgs.wget
          pkgs.unzip
        ];
      };
    };
}
