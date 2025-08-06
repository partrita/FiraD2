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
          pkgs.wget
        ];

        buildPhase = ''
          set -e

          echo "[INFO] Setting up build environment..."
          export DOWNLOAD_PATH="assets"
          export BUILT_FONTS_PATH="built_fonts"
          mkdir -p "$DOWNLOAD_PATH"
          mkdir -p "$BUILT_FONTS_PATH"

          echo "[INFO] Extracting font archives..."
          unzip -o "${d2coding}" -d "$DOWNLOAD_PATH"
          unzip -o "${fira_code}" -d "$DOWNLOAD_PATH"
          unzip -o "${fira_code_nerd}" -d "$DOWNLOAD_PATH"

          echo "[INFO] Cleaning up non-regular ttf files..."
          find "$DOWNLOAD_PATH" -type f -name "*.ttf" | while read -r file; do
              if [[ "$file" == *D2Coding* ]]; then
                  echo "  - Keeping D2Coding font file: $file"
                  continue
              fi
              if [[ "$file" != *Regular* ]]; then
                  echo "  - Removing: $file"
                  rm "$file"
              fi
          done

          echo "[INFO] Building fonts..."
          python3 -c 'from scripts.hangulify import build_fonts; build_fonts()'
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
