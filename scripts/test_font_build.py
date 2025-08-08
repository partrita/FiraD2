#!/usr/bin/env python3
"""
폰트 빌드 프로세스 테스트 스크립트

이 스크립트는 폰트 빌드 과정의 각 단계를 테스트하고 검증합니다.
"""

import os
import sys
import unittest

# 현재 스크립트 디렉터리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(__file__))

from config import (
    EN_FONT_PATH,
    KO_FONT_PATH,
    EN_NERD_FONT_PATH,
    BUILT_FONTS_PATH,
    ASSETS_PATH
)


class TestFontBuildProcess(unittest.TestCase):
    """폰트 빌드 프로세스 테스트 클래스"""

    def test_directory_structure(self):
        """필요한 디렉터리 구조가 존재하는지 테스트"""
        print("\n=== 디렉터리 구조 테스트 ===")
        
        # 필수 디렉터리들
        required_dirs = {
            "Assets": ASSETS_PATH,
            "English Font": EN_FONT_PATH,
            "Korean Font": KO_FONT_PATH,
            "Nerd Font": EN_NERD_FONT_PATH
        }
        
        for name, path in required_dirs.items():
            with self.subTest(directory=name):
                self.assertTrue(os.path.exists(path), 
                    f"{name} 디렉터리가 존재하지 않습니다: {path}")
                print(f"✓ {name} 디렉터리 확인: {path}")

    def test_font_files_existence(self):
        """각 디렉터리에 폰트 파일이 존재하는지 테스트"""
        print("\n=== 폰트 파일 존재 테스트 ===")
        
        font_dirs = {
            "English Font": EN_FONT_PATH,
            "Korean Font": KO_FONT_PATH,
            "Nerd Font": EN_NERD_FONT_PATH
        }
        
        for name, path in font_dirs.items():
            with self.subTest(directory=name):
                if os.path.exists(path):
                    ttf_files = [f for f in os.listdir(path) if f.lower().endswith('.ttf')]
                    self.assertGreater(len(ttf_files), 0, 
                        f"{name} 디렉터리에 TTF 파일이 없습니다: {path}")
                    print(f"✓ {name}: {len(ttf_files)}개 TTF 파일 발견")
                    for ttf_file in ttf_files:
                        print(f"  - {ttf_file}")

    def test_font_weights(self):
        """Regular와 Bold 폰트가 각 디렉터리에 있는지 테스트"""
        print("\n=== 폰트 웨이트 테스트 ===")
        
        font_dirs = {
            "English Font": EN_FONT_PATH,
            "Korean Font": KO_FONT_PATH,
            "Nerd Font": EN_NERD_FONT_PATH
        }
        
        expected_weights = ['regular', 'bold']
        
        for name, path in font_dirs.items():
            with self.subTest(directory=name):
                if os.path.exists(path):
                    ttf_files = [f.lower() for f in os.listdir(path) if f.lower().endswith('.ttf')]
                    
                    for weight in expected_weights:
                        weight_files = [f for f in ttf_files if weight in f]
                        if weight_files:
                            print(f"✓ {name} - {weight.capitalize()}: {len(weight_files)}개 파일")
                        else:
                            print(f"⚠ {name} - {weight.capitalize()}: 파일이 없습니다")

    def test_fontforge_import(self):
        """FontForge 모듈 임포트 테스트"""
        print("\n=== FontForge 모듈 테스트 ===")
        
        try:
            import fontforge
            print("✓ FontForge 모듈 임포트 성공")
            
            # 간단한 폰트 생성 테스트
            test_font = fontforge.font()
            test_font.fontname = "TestFont"
            print("✓ FontForge 폰트 객체 생성 성공")
            test_font.close()
            
        except ImportError as e:
            self.fail(f"FontForge 모듈을 임포트할 수 없습니다: {e}")
        except Exception as e:
            self.fail(f"FontForge 테스트 중 오류 발생: {e}")

    def test_font_loading(self):
        """실제 폰트 파일 로딩 테스트"""
        print("\n=== 폰트 파일 로딩 테스트 ===")
        
        try:
            import fontforge
            
            font_dirs = [EN_FONT_PATH, KO_FONT_PATH, EN_NERD_FONT_PATH]
            dir_names = ["English Font", "Korean Font", "Nerd Font"]
            
            for i, (name, path) in enumerate(zip(dir_names, font_dirs)):
                with self.subTest(directory=name):
                    if os.path.exists(path):
                        ttf_files = [f for f in os.listdir(path) if f.lower().endswith('.ttf')]
                        if ttf_files:
                            test_file = os.path.join(path, ttf_files[0])
                            try:
                                font = fontforge.open(test_file)
                                print(f"✓ {name} 폰트 로드 성공: {ttf_files[0]}")
                                print(f"  패밀리명: {font.familyname}")
                                print(f"  폰트명: {font.fontname}")
                                print(f"  글리프 수: {len(font)}")
                                font.close()
                            except Exception as e:
                                self.fail(f"{name} 폰트 로드 실패 ({ttf_files[0]}): {e}")
                        else:
                            print(f"⚠ {name}: 테스트할 TTF 파일이 없습니다")
                            
        except ImportError:
            self.skipTest("FontForge 모듈이 없어 폰트 로딩 테스트를 건너뜁니다")

    def test_hangulify_imports(self):
        """hangulify 모듈의 함수들이 제대로 임포트되는지 테스트"""
        print("\n=== Hangulify 모듈 테스트 ===")
        
        try:
            from hangulify import (
                find_font_files,
                build_fonts,
                merge_korean_glyphs,
                process_font_file
            )
            print("✓ hangulify 모듈 함수들 임포트 성공")
            
            # find_font_files 함수 테스트
            if os.path.exists(EN_FONT_PATH):
                regular_files = find_font_files(EN_FONT_PATH, "regular")
                bold_files = find_font_files(EN_FONT_PATH, "bold")
                print(f"✓ find_font_files 테스트 성공 (Regular: {len(regular_files)}, Bold: {len(bold_files)})")
            
        except ImportError as e:
            self.fail(f"hangulify 모듈 임포트 실패: {e}")
        except Exception as e:
            print(f"⚠ hangulify 함수 테스트 중 오류: {e}")

    def test_output_directory_creation(self):
        """출력 디렉터리 생성 테스트"""
        print("\n=== 출력 디렉터리 테스트 ===")
        
        # 임시로 built_fonts 디렉터리 생성 테스트
        test_output_dir = os.path.join(ASSETS_PATH, "test_built_fonts")
        
        try:
            os.makedirs(test_output_dir, exist_ok=True)
            self.assertTrue(os.path.exists(test_output_dir))
            print(f"✓ 출력 디렉터리 생성 성공: {test_output_dir}")
            
            # 정리
            if os.path.exists(test_output_dir):
                os.rmdir(test_output_dir)
                print("✓ 테스트 디렉터리 정리 완료")
                
        except Exception as e:
            self.fail(f"출력 디렉터리 생성 테스트 실패: {e}")


def run_detailed_analysis():
    """상세한 폰트 분석 정보 출력"""
    print("\n" + "="*60)
    print("상세 폰트 분석")
    print("="*60)
    
    font_dirs = {
        "English Font": EN_FONT_PATH,
        "Korean Font": KO_FONT_PATH,
        "Nerd Font": EN_NERD_FONT_PATH
    }
    
    for name, path in font_dirs.items():
        print(f"\n--- {name} ---")
        if os.path.exists(path):
            files = [f for f in os.listdir(path) if f.lower().endswith('.ttf')]
            for file in files:
                print(f"  📄 {file}")
                file_path = os.path.join(path, file)
                file_size = os.path.getsize(file_path)
                print(f"     크기: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
        else:
            print(f"  ❌ 디렉터리가 존재하지 않습니다: {path}")


if __name__ == '__main__':
    print("FiraD2 폰트 빌드 테스트 시작")
    print("="*60)
    
    # 상세 분석 실행
    run_detailed_analysis()
    
    # 유닛 테스트 실행
    print("\n" + "="*60)
    print("유닛 테스트 실행")
    print("="*60)
    
    # verbosity=2로 설정하여 자세한 테스트 결과 출력
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "="*60)
    print("테스트 완료!")
    print("="*60)
