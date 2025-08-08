# FiraD2 - FiraCode with Korean Hangul Support

![GitHub release (latest by date)](https://img.shields.io/github/v/release/partrita/FiraD2?style=flat-square)
![License](https://img.shields.io/github/license/partrita/FiraD2?style=flat-square)
![Build Status](https://img.shields.io/github/actions/workflow/status/partrita/FiraD2/release-font.yml?style=flat-square)

**FiraD2** is a programming font that combines the best of FiraCode's ligatures and coding features with D2Coding's excellent Korean Hangul support. This font provides optimal readability for code that includes both English and Korean text.

## ✨ Features

- **Perfect Korean Support**: Incorporates D2Coding's Hangul glyphs (U+3131-U+318E, U+AC00-U+D7A3)
- **Programming Ligatures**: Maintains FiraCode's popular programming ligatures (→, >=, !=, etc.)
- **Multiple Variants**: Regular fonts, Nerd Font versions with icons, and web fonts
- **Optimized Spacing**: Carefully adjusted character widths for better readability
- **Cross-platform**: Works on Windows, macOS, and Linux

## 📥 Download

Download the latest fonts from the [Releases](https://github.com/partrita/FiraD2/releases) page.

### Font Variants Explained

| File | Description | Best For |
|------|-------------|----------|
| `FiraD2-Regular.ttf` | Main font for general use | Code editors, IDEs |
| `FiraD2-Bold.ttf` | Bold variant | Emphasis, headers |
| `FiraD2-Regular.woff2` | Web font format | Web applications |
| `FiraD2NerdFont-Regular.ttf` | With programming icons | Terminal, Vim/Neovim |
| `FiraD2NerdFont-Bold.ttf` | Bold with icons | Terminal emphasis |

### Installation

#### Windows
1. Download the `.ttf` files
2. Right-click and select "Install" or "Install for all users"
3. Restart your applications

#### macOS  
1. Download the `.ttf` files
2. Double-click to open Font Book
3. Click "Install Font"
4. Restart your applications

#### Linux
1. Download the `.ttf` files
2. Copy to `~/.local/share/fonts/` or `/usr/share/fonts/`
3. Run `fc-cache -fv`
4. Restart your applications

## 🛠️ Building from Source

### Prerequisites

Before building, you need:
- Python 3.7+
- FontForge with Python bindings
- wget and unzip utilities

### Method 1: Using Nix (Recommended)

The easiest way to build FiraD2 with all dependencies managed:

```bash
# Clone the repository
git clone https://github.com/partrita/FiraD2.git
cd FiraD2

# Enter Nix development environment
nix develop

# Build fonts (downloads assets automatically)
python scripts/build.py build

# Exit when done
exit
```

### Method 2: Using Docker

Build in a containerized environment:

```bash
# Clone and build Docker image
git clone https://github.com/partrita/FiraD2.git
cd FiraD2
docker build -t firad2 .

# Run interactive container
docker run -it -v "$(pwd)":/app firad2

# Inside container: build fonts
python3 scripts/build.py build

# Exit container
exit
```

### Method 3: Manual Setup

For advanced users who want to set up dependencies manually:

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install fontforge python3-fontforge wget unzip
```

#### macOS
```bash
brew install fontforge wget
pip3 install fontforge-python
```

#### Manual Build Process
```bash
# Clone repository
git clone https://github.com/partrita/FiraD2.git
cd FiraD2

# Download required font assets (you'll need to do this manually)
# - FiraCode: https://github.com/tonsky/FiraCode/releases
# - D2Coding: https://github.com/naver/d2codingfont/releases  
# - FiraCode NerdFont: https://github.com/ryanoasis/nerd-fonts/releases

# Extract fonts to assets/ directories:
# assets/en_font/        - FiraCode TTF files
# assets/ko_font/        - D2Coding TTF files  
# assets/en_nerd_font/   - FiraCode NerdFont TTF files

# Build fonts
python3 scripts/build.py build

# Clean up (optional)
python3 scripts/build.py clean
```

### Build Commands

| Command | Description |
|---------|-------------|
| `python scripts/build.py build` | Build fonts from existing assets |
| `python scripts/build.py test` | Test font building process |
| `python scripts/build.py clean` | Clean generated files |

## 🎨 Usage Examples

### VS Code
Add to your `settings.json`:
```json
{
    "editor.fontFamily": "FiraD2, Consolas, monospace",
    "editor.fontLigatures": true,
    "editor.fontSize": 14
}
```

### Terminal (with Nerd Font variant)
```bash
# Check if font is installed
fc-list | grep FiraD2

# Configure your terminal to use FiraD2NerdFont-Regular
```

### Web Projects
```css
@font-face {
    font-family: 'FiraD2';
    src: url('path/to/FiraD2-Regular.woff2') format('woff2');
    font-display: swap;
}

code, pre {
    font-family: 'FiraD2', 'Fira Code', monospace;
}
```

## ⚙️ Configuration

The `scripts/config.py` file contains build configuration options:

- `KOREAN_FONT_WIDTH`: Width for Korean characters
- `ENGLISH_FONT_WIDTH`: Width for English characters  
- `TARGET_EM`: Target em size for font scaling
- Font source paths and output directories

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test the build process
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📋 Requirements

### Source Fonts
- **FiraCode**: Base programming font with ligatures
- **D2Coding**: Korean coding font for Hangul support
- **FiraCode Nerd Font**: Icon-enhanced variant

### Build Dependencies
- Python 3.7+
- FontForge with Python bindings
- Basic Unix utilities (wget, unzip)

## 🐛 Known Issues

- Some terminal emulators may not display ligatures correctly
- Web font loading might require proper CORS headers
- Font metrics may need adjustment for specific applications

## 📄 License

This project is licensed under the [SIL Open Font License 1.1](LICENSE).

### Font Licenses
- **FiraCode**: SIL OFL 1.1
- **D2Coding**: SIL OFL 1.1  
- **Nerd Fonts**: MIT License

## 🙏 Acknowledgments

- [FiraCode](https://github.com/tonsky/FiraCode) by Nikita Prokopov
- [D2Coding](https://github.com/naver/d2codingfont) by NAVER
- [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) project

---

**Made with ❤️ for developers who work with Korean and English code**
