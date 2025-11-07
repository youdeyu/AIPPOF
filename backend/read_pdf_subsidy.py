"""
读取论文PDF并提取补贴模型相关信息
"""
import sys
import os

try:
    import PyPDF2
    has_pypdf2 = True
except ImportError:
    has_pypdf2 = False
    print("PyPDF2未安装，尝试使用pdfplumber...")

try:
    import pdfplumber
    has_pdfplumber = True
except ImportError:
    has_pdfplumber = False
    print("pdfplumber未安装")

import re

pdf_path = r"C:\Users\10046\Desktop\python代码测试\code1\final\documents\AI驱动下的个人养老金税收优惠政策优化：一个智能化决策框架的理论构想(2).pdf"

def extract_with_pdfplumber(pdf_path):
    """使用pdfplumber提取PDF文本"""
    print("=" * 80)
    print("使用 pdfplumber 提取PDF内容")
    print("=" * 80)
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                full_text += f"\n\n=== 第 {i} 页 ===\n\n{text}"
        
        return full_text

def extract_with_pypdf2(pdf_path):
    """使用PyPDF2提取PDF文本"""
    print("=" * 80)
    print("使用 PyPDF2 提取PDF内容")
    print("=" * 80)
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        full_text = ""
        
        for i, page in enumerate(pdf_reader.pages, 1):
            text = page.extract_text()
            if text:
                full_text += f"\n\n=== 第 {i} 页 ===\n\n{text}"
        
        return full_text

def search_subsidy_info(text):
    """搜索补贴相关信息"""
    print("\n" + "=" * 80)
    print("搜索补贴模型相关内容")
    print("=" * 80)
    
    # 关键词搜索
    keywords = [
        r'补贴.*三段',
        r'补贴.*两段',
        r'补贴.*分段',
        r'配比.*30%',
        r'配比.*6%',
        r'ratio.*0\.30',
        r'ratio.*0\.06',
        r'γ.*=.*0\.3',
        r'γ.*=.*0\.06',
        r'补贴率',
        r'匹配率',
        r'两部制',
        r'三部制',
        r'首档.*缴费',
        r'超额.*缴费',
        r'分层.*补贴'
    ]
    
    findings = {}
    
    for keyword in keywords:
        matches = re.finditer(keyword, text, re.IGNORECASE)
        for match in matches:
            # 提取匹配内容的上下文（前后200字符）
            start = max(0, match.start() - 200)
            end = min(len(text), match.end() + 200)
            context = text[start:end]
            
            if keyword not in findings:
                findings[keyword] = []
            findings[keyword].append(context)
    
    # 打印发现的内容
    if findings:
        print("\n找到以下相关内容：\n")
        for keyword, contexts in findings.items():
            print(f"\n【关键词: {keyword}】")
            print("-" * 80)
            for i, context in enumerate(contexts[:3], 1):  # 只显示前3个匹配
                print(f"\n匹配 {i}:")
                print(context.strip())
                print("-" * 40)
    else:
        print("\n未找到相关关键词")
    
    return findings

def extract_formulas(text):
    """提取包含公式的段落"""
    print("\n" + "=" * 80)
    print("提取补贴计算公式")
    print("=" * 80)
    
    # 查找包含补贴公式的段落
    formula_patterns = [
        r'补贴.*=.*\+.*',
        r'S.*=.*G.*\+.*',
        r'subsidy.*=.*',
        r'公式.*\d+.*补贴'
    ]
    
    formulas = []
    for pattern in formula_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 300)
            end = min(len(text), match.end() + 300)
            context = text[start:end]
            formulas.append(context)
    
    if formulas:
        print("\n找到以下公式：\n")
        for i, formula in enumerate(formulas[:5], 1):
            print(f"\n公式 {i}:")
            print(formula.strip())
            print("-" * 80)
    else:
        print("\n未找到公式相关内容")

def main():
    if not os.path.exists(pdf_path):
        print(f"❌ 文件不存在: {pdf_path}")
        return
    
    print(f"\n📄 PDF文件: {pdf_path}")
    print(f"文件大小: {os.path.getsize(pdf_path) / 1024:.2f} KB\n")
    
    # 尝试提取文本
    text = None
    
    if has_pdfplumber:
        try:
            text = extract_with_pdfplumber(pdf_path)
            print(f"\n✅ 成功提取 {len(text)} 个字符")
        except Exception as e:
            print(f"❌ pdfplumber提取失败: {e}")
    
    if not text and has_pypdf2:
        try:
            text = extract_with_pypdf2(pdf_path)
            print(f"\n✅ 成功提取 {len(text)} 个字符")
        except Exception as e:
            print(f"❌ PyPDF2提取失败: {e}")
    
    if not text:
        print("\n❌ 无法提取PDF文本，请安装 pdfplumber 或 PyPDF2:")
        print("   pip install pdfplumber")
        print("   或")
        print("   pip install PyPDF2")
        return
    
    # 保存完整文本
    output_file = "pdf_extracted_text.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"\n💾 完整文本已保存到: {output_file}")
    
    # 搜索补贴相关信息
    search_subsidy_info(text)
    
    # 提取公式
    extract_formulas(text)
    
    # 输出建议
    print("\n" + "=" * 80)
    print("📋 总结")
    print("=" * 80)
    print("\n请查看生成的 pdf_extracted_text.txt 文件获取完整内容")
    print("手动搜索以下关键词以确认补贴模型类型：")
    print("  - '三段式' 或 '三档'")
    print("  - '两段式' 或 '两档'")
    print("  - '30%' 和 '6%'")
    print("  - '配比率' 或 '匹配率'")

if __name__ == "__main__":
    main()
