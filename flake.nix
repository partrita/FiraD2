{
  description = "A flake for building FiraD2 fonts";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      d2coding = pkgs.fetchzip {
        url = "https://github.com/naver/d2codingfont/releases/download/VER1.3.2/D2Coding-Ver1.3.2-20180524.zip";
        stripRoot = false;
        sha256 = "0f1c9192eac7d56329dddc620f9f1666b707e9c8ed38fe1f988d0ae3e30b24e6";
      };
      fira_code = pkgs.fetchzip {
        url = "https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip";
        stripRoot = false;
        sha256 = "0949915ba8eb24d89fd93d10a7ff623f42830d7c5ffc3ecbf960e4ecad3e3e79";
      };
      fira_code_nerd = pkgs.fetchzip {
        url = "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/FiraCode.zip";
        stripRoot = false;
        sha256 = "7cc4ffd8f7a1fc914cdab7b149808298165ff7a7f40e40d82dea9ebe41e8ca0b";
      };
    in
    {
      packages.x86_64-linux.default = pkgs.stdenv.mkDerivation {
        pname = "firad2";
        version = "0.1.0";

        src = ./.;

        buildInputs = [
          pkgs.fontforge
          pkgs.python3
          pkgs.unzip
          pkgs.wget # The script uses it
        ];

        D2CODING_SRC = d2coding;
        FIRACODE_SRC = fira_code;
        FIRACODE_NERD_SRC = fira_code_nerd;

        buildPhase = ''
          chmod +x ./scripts/build.sh
          ./scripts/build.sh
        '';

        installPhase = ''
          mkdir -p $out
          cp -r built_fonts/* $out
        '';
      };

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
