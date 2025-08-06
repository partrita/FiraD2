import os
from typing import Any
import re
import fontforge

from config import (
    BUILT_FONTS_PATH,
    ENGLISH_FONT_NF_PATH,
    ENGLISH_FONT_PATH,
    ENGLISH_FONT_NF_WIDTH,
    ENGLISH_FONT_WIDTH,
    KOREAN_FONT_PATH,
    OLD_FONT_NAME,
    NEW_FONT_NAME,
)

# 글리프의 사이드 베어링을 조정하는 값입니다.
BEARING_ADJUSTMENT: int = 200

# Mono 폰트의 Em 단위
EN_MONO_EM: int = 1300


def update_family_name(original_family_name, old_str, new_str):
    """
    폰트 이름을 변경합니다.

    Args:
        original_family_name (str): 원래 폰트 이름.
        old_str (str): 변경하려는 이전 문자열. 공백과 대소문자는 무시됩니다.
        new_str (str): 변경할 새로운 문자열.

    Returns:
        str: 변경된 폰트 이름.
    """
    # old_str의 공백을 제거하고 정규표현식으로 만듭니다.
    pattern = re.compile(re.escape(old_str.replace(" ", "")), re.IGNORECASE)

    # original_family_name에서 모든 공백을 제거하고 변경 작업을 수행합니다.
    cleaned_original_name = original_family_name.replace(" ", "")

    # 정규표현식을 사용해 변경합니다.
    return pattern.sub(new_str, cleaned_original_name)


def adjust_glyph_bearing(glyph: Any, adjustment: int) -> Any:
    """글리프의 왼쪽 및 오른쪽 사이드 베어링을 조정합니다."""
    glyph.left_side_bearing = adjustment // 2 + int(glyph.left_side_bearing)
    glyph.right_side_bearing = adjustment // 2 + int(glyph.right_side_bearing)
    return glyph


def process_hangul_glyphs(font: fontforge.font) -> fontforge.font:
    """한글 글리프를 선택하고 베어링을 조정합니다."""
    hangul_range = font.selection.select(("unicode", "ranges"), 0x3131, 0x318E)
    hangul_range.select(("unicode", "ranges", "more"), 0xAC00, 0xD7A3)

    for glyph_id in hangul_range:
        glyph = font[glyph_id]
        is_jetbrains_font = int(glyph.width) in (
            ENGLISH_FONT_WIDTH,
            ENGLISH_FONT_NF_WIDTH,
        )

        if not glyph.references:
            if is_jetbrains_font:
                adjust_glyph_bearing(glyph, BEARING_ADJUSTMENT)
        else:
            for ref in glyph.references:
                ref_glyph = font[ref[0]]
                is_jetbrains_font_ref = int(ref_glyph.width) in (
                    ENGLISH_FONT_WIDTH,
                    ENGLISH_FONT_NF_WIDTH,
                )
                if is_jetbrains_font_ref:
                    adjust_glyph_bearing(ref_glyph, BEARING_ADJUSTMENT)
    return font


def get_font_style(font: fontforge.font, original_filename: str = None) -> str:
    """
    폰트 객체나 파일명에서 폰트 스타일을 추출합니다.

    Args:
        font: fontforge.font 객체
        original_filename: 원본 파일명 (선택사항)

    Returns:
        str: 폰트 스타일
    """
    # 파일명이 제공된 경우 파일명에서 스타일 추출
    if original_filename:
        base_name = os.path.splitext(original_filename)[0]
        if "Regular" in base_name:
            return "Regular"
        style_parts = base_name.split("-")
        if len(style_parts) > 1:
            return style_parts[-1]

    # 폰트 객체에서 스타일 정보 추출
    # 1. fontname에서 추출 시도
    if hasattr(font, "fontname") and font.fontname:
        fontname_parts = font.fontname.split("-")
        if len(fontname_parts) > 1:
            return fontname_parts[-1]

    # 2. weight와 다른 속성들을 확인
    style_parts = []

    if hasattr(font, "weight") and font.weight:
        weight = font.weight.lower()
        if "bold" in weight:
            style_parts.append("Bold")
        elif "light" in weight:
            style_parts.append("Light")
        elif "medium" in weight:
            style_parts.append("Medium")

    # 3. 기울임체 확인 (이탤릭 각도로 판단)
    if hasattr(font, "italicangle") and font.italicangle != 0:
        style_parts.append("Italic")

    # 4. OS/2 테이블에서 weight 확인
    try:
        if hasattr(font, "os2_weight"):
            weight_value = font.os2_weight
            if weight_value >= 700:
                if "Bold" not in style_parts:
                    style_parts.append("Bold")
            elif weight_value <= 300:
                if "Light" not in style_parts:
                    style_parts.append("Light")
    except Exception:
        pass

    # 5. 스타일이 없으면 Regular 반환
    if not style_parts:
        return "Regular"

    return "".join(style_parts)


def format_style_name(style: str) -> str:
    """스타일 이름을 포맷팅합니다(예: 'BoldItalic' -> 'Bold Italic')."""
    formatted = []
    for i, char in enumerate(style):
        if char.isupper() and i > 0 and not style[i - 1].isupper():
            formatted.append(" ")
        formatted.append(char)
    return "".join(formatted).strip()


def update_font_metadata(
    font: fontforge.font, style: str, old_name: str, new_name: str
) -> None:
    """
    폰트의 메타데이터(패밀리 이름, 폰트 이름, 스타일 등)를 업데이트합니다.

    Args:
        font: fontforge.font 객체.
        style: 폰트 스타일(예: "Regular", "Bold").
        old_name: 변경하려는 원래 폰트 이름.
        new_name: 새로 지정할 폰트 이름.
    """
    # 폰트 패밀리 이름을 업데이트합니다.
    # old_name의 공백을 제거하고 대소문자를 무시하는 정규표현식 패턴을 생성합니다.
    pattern = re.compile(re.escape(old_name.replace(" ", "")), re.IGNORECASE)

    # original_family_name에서 공백을 제거한 후, 정규표현식을 이용해 대체합니다.
    cleaned_original_name = font.familyname.replace(" ", "")
    new_family_name = pattern.sub(new_name, cleaned_original_name)

    # 폰트 메타데이터를 업데이트합니다.
    font.familyname = new_family_name
    formatted_style = format_style_name(style)

    font.fontname = f"{new_family_name}-{style}"
    font.fullname = f"{new_family_name} {formatted_style}"
    font.appendSFNTName("English (US)", "Preferred Family", new_family_name)
    font.appendSFNTName("English (US)", "Family", new_family_name)
    font.appendSFNTName("English (US)", "Compatible Full", font.fullname)
    font.appendSFNTName("English (US)", "SubFamily", formatted_style)


def re_encode_for_nerd_font(font: fontforge.font) -> None:
    """Nerd Font의 특정 글리프 매핑 문제를 수정합니다(예: 하트, 오른쪽 삼각형 아이콘)."""
    try:
        # 'heart' 글리프 매핑 수정
        if "heart" in font:
            font.selection.select(0xF08D0)
            font.copy()
            font.selection.select(0x2665)
            font.paste()
            font.selection.select(0xF08D0)
            font.clear()
            print("[INFO] 'heart' 글리프 매핑을 수정했습니다.")

        # 'triangleright' 글리프 매핑 수정
        if "triangleright" in font:
            font.selection.select(0x25BA)
            font.copy()
            font.selection.select(0x22B2)
            font.paste()
            font.selection.select(0x25BA)
            font.clear()
            print("[INFO] 'triangleright' 글리프 매핑을 수정했습니다.")

    except Exception as e:
        print(f"[WARNING] 글리프 매핑 수정 중 오류 발생: {e}")


def generate_font_files(font: fontforge.font, style: str) -> None:
    """최종 TTF 및 WOFF2 폰트 파일을 생성하고 내보냅니다."""
    output_filename_base = f"{font.familyname.replace(' ', '')}-{style}"
    output_ttf_path = os.path.join(BUILT_FONTS_PATH, f"{output_filename_base}.ttf")
    output_woff2_path = os.path.join(BUILT_FONTS_PATH, f"{output_filename_base}.woff2")

    try:
        font.generate(output_ttf_path)
        print(f"[INFO] {output_ttf_path} 내보내기 완료")
    except Exception as e:
        print(f"[ERROR] {font.fontname}에 대한 TTF 생성 실패: {e}")

    try:
        font.generate(output_woff2_path)
        print(f"[INFO] {output_woff2_path} 내보내기 완료")
    except Exception as e:
        print(f"[ERROR] {font.fontname}에 대한 WOFF2 생성 실패: {e}")


def scale_font_em_units(font: fontforge.font, target_em: int) -> None:
    """
    폰트의 Em 단위를 조정하고 모든 글리프를 스케일링합니다.

    Args:
        font: fontforge.font 객체
        target_em: 목표 Em 단위 값
    """
    if font.em == target_em:
        return

    scale_factor = target_em / font.em

    # Em 단위 먼저 변경
    font.em = target_em

    # 모든 글리프 선택하여 스케일링
    font.selection.all()

    # FontForge의 transform 메서드를 사용하여 스케일링
    # transform(scale_x, skew_x, skew_y, scale_y, translate_x, translate_y)
    font.transform((scale_factor, 0, 0, scale_factor, 0, 0))

    print(
        f"[INFO] 한글 폰트 Em 단위를 {int(target_em / scale_factor)}에서 {target_em}로 조정했습니다."
    )


def merge_korean_glyphs(
    target_font: fontforge.font, source_font: fontforge.font
) -> None:
    """
    한국어 글리프를 소스 폰트에서 타겟 폰트로 복사합니다.

    Args:
        target_font: 글리프를 받을 대상 폰트
        source_font: 글리프를 복사할 소스 폰트
    """
    try:
        # 한글 범위의 글리프들을 복사
        hangul_ranges = [
            (0x1100, 0x11FF),  # 한글 자모
            (0x3130, 0x318F),  # 한글 호환 자모
            (0xA960, 0xA97F),  # 한글 자모 확장-A
            (0xAC00, 0xD7AF),  # 한글 음절
            (0xD7B0, 0xD7FF),  # 한글 자모 확장-B
        ]

        copied_count = 0
        for start, end in hangul_ranges:
            for codepoint in range(start, end + 1):
                if codepoint in source_font:
                    source_glyph = source_font[codepoint]
                    # 글리프가 실제로 존재하는지 확인
                    if source_glyph.isWorthOutputting():
                        # 소스 글리프를 선택하고 복사
                        source_font.selection.select(codepoint)
                        source_font.copy()

                        # 타겟 폰트에서 해당 위치를 선택하고 붙여넣기
                        target_font.selection.select(codepoint)
                        target_font.paste()
                        copied_count += 1

        print(f"[INFO] {copied_count}개의 한글 글리프를 복사했습니다.")

    except Exception as e:
        print(f"[ERROR] 한글 글리프 병합 중 오류 발생: {e}")


def process_font_file(
    en_font: fontforge.font,
    ko_font: fontforge.font,
    is_nerd_font: bool,
    font_filename: str,
) -> None:
    """
    단일 폰트 파일을 처리하여 한글 글리프를 병합하고 메타데이터를 업데이트합니다.

    Args:
        en_font: 영문 폰트 객체
        ko_font: 한글 폰트 객체
        is_nerd_font: Nerd Font 여부
        font_filename: 원본 폰트 파일명
    """
    if is_nerd_font:
        re_encode_for_nerd_font(en_font)

    # D2Coding 폰트의 글리프를 JetBrains Mono 폰트에 병합합니다.
    merge_korean_glyphs(en_font, ko_font)

    style = get_font_style(en_font, font_filename)
    update_font_metadata(en_font, style, old_name=OLD_FONT_NAME, new_name=NEW_FONT_NAME)

    generate_font_files(en_font, style)


def build_fonts() -> None:
    """
    메인 폰트 빌드 프로세스입니다. D2 Coding 폰트를 열고 처리한 다음,
    각 Monospace 및 Nerd Font 파일과 병합합니다.
    """
    os.makedirs(BUILT_FONTS_PATH, exist_ok=True)

    ko_font = fontforge.open(KOREAN_FONT_PATH)

    # D2Coding 폰트의 Em 단위를 Mono와 동일하게 조정
    scale_font_em_units(ko_font, EN_MONO_EM)

    process_hangul_glyphs(ko_font)

    font_dirs_to_process = [
        (ENGLISH_FONT_PATH, False),
        (ENGLISH_FONT_NF_PATH, True),
    ]

    for dir_path, is_nerd_font in font_dirs_to_process:
        if not os.path.exists(dir_path):
            print(
                f"[WARNING] 폰트 디렉터리를 찾을 수 없습니다: {dir_path}. 건너뜁니다."
            )
            continue

        for filename in os.listdir(dir_path):
            if filename.lower().endswith(".ttf"):
                font_file_path = os.path.join(dir_path, filename)
                en_font = fontforge.open(font_file_path)
                process_font_file(en_font, ko_font, is_nerd_font, filename)
                en_font.close()

    ko_font.close()


if __name__ == "__main__":
    build_fonts()
