import os
import json
from datetime import datetime

# 配置
ROOT_DIR = '.'
OUTPUT_FILE = 'index.html'
IGNORE_DIRS = {'.git', '.idea', '__pycache__', 'node_modules'}
IGNORE_FILES = {OUTPUT_FILE, os.path.basename(__file__)}

def get_file_info(file_path):
    """获取文件信息"""
    stat = os.stat(file_path)
    return {
        'name': os.path.basename(file_path).replace('.html', ''),
        'path': file_path.replace('\\', '/'),
        'mtime': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
        'size': f"{stat.st_size / 1024:.1f} KB"
    }

def scan_directory():
    """扫描目录结构"""
    categories = {}
    
    for root, dirs, files in os.walk(ROOT_DIR):
        # 过滤目录
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        # 计算相对路径作为分类名称
        rel_path = os.path.relpath(root, ROOT_DIR)
        
        if rel_path == '.':
            category_name = '未分类'
        else:
            # 使用文件夹名作为分类名
            category_name = os.path.basename(root)
            # 如果有多级目录，可以使用 path/to/folder
            # category_name = rel_path.replace('\\', '/')
            
        html_files = [f for f in files if f.endswith('.html') and f not in IGNORE_FILES]
        
        if html_files:
            if category_name not in categories:
                categories[category_name] = []
                
            for f in html_files:
                file_path = os.path.join(rel_path, f)
                if rel_path == '.':
                    file_path = f
                categories[category_name].append(get_file_info(file_path))
    
    return categories

def generate_html(categories):
    """生成HTML文件"""
    
    # 准备JSON数据供前端使用
    categories_json = json.dumps(categories, ensure_ascii=False)
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科普演示导航</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --primary-color: #3b82f6;
            --secondary-color: #1e293b;
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-color: #e2e8f0;
            --text-muted: #94a3b8;
            --border-color: #334155;
            --hover-color: #38bdf8;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        body {{
            background-color: var(--bg-color);
            color: var(--text-color);
            min-height: 100vh;
            background-image: radial-gradient(circle at 10% 20%, rgba(28, 58, 173, 0.1) 0%, transparent 20%),
                              radial-gradient(circle at 90% 80%, rgba(124, 58, 237, 0.1) 0%, transparent 20%);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 50px;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 15px;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }}
        
        .subtitle {{
            color: var(--text-muted);
            font-size: 1.1rem;
        }}
        
        .search-container {{
            max-width: 600px;
            margin: 30px auto;
            position: relative;
        }}
        
        .search-input {{
            width: 100%;
            padding: 15px 25px;
            padding-left: 50px;
            background: var(--secondary-color);
            border: 1px solid var(--border-color);
            border-radius: 30px;
            color: white;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
        }}
        
        .search-input:focus {{
            border-color: var(--primary-color);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
        }}
        
        .search-icon {{
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
        }}
        
        .category-section {{
            margin-bottom: 40px;
            animation: fadeIn 0.5s ease;
        }}
        
        .category-title {{
            font-size: 1.5rem;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--hover-color);
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            position: relative;
            overflow: hidden;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            border-color: var(--primary-color);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }}
        
        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, var(--primary-color), #8b5cf6);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .card:hover::before {{
            opacity: 1;
        }}
        
        .card-icon {{
            font-size: 2rem;
            margin-bottom: 15px;
            color: var(--primary-color);
        }}
        
        .card-title {{
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 10px;
            color: #fff;
        }}
        
        .card-meta {{
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: auto;
            display: flex;
            justify-content: space-between;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .empty-state {{
            text-align: center;
            padding: 50px;
            color: var(--text-muted);
        }}
        
        footer {{
            text-align: center;
            margin-top: 60px;
            color: var(--text-muted);
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-project-diagram"></i> 科普演示导航中心</h1>
            <p class="subtitle">探索 算法、人工智能 与 计算机科学 的奥秘</p>
            
            <div class="search-container">
                <i class="fas fa-search search-icon"></i>
                <input type="text" id="searchInput" class="search-input" placeholder="搜索演示项目...">
            </div>
        </header>
        
        <div id="content">
            <!-- 内容将通过JS动态生成 -->
        </div>
        
        <footer>
            <p>上次更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </footer>
    </div>

    <script>
        // 数据源
        const categories = {categories_json};
        
        // 图标映射
        const iconMap = {{
            'AI': 'fa-brain',
            'Algorithm': 'fa-code-branch',
            '未分类': 'fa-folder',
            'Network': 'fa-network-wired',
            'OS': 'fa-microchip'
        }};
        
        const contentDiv = document.getElementById('content');
        const searchInput = document.getElementById('searchInput');
        
        // 渲染函数
        function render(filterText = '') {{
            contentDiv.innerHTML = '';
            let hasContent = false;
            
            for (const [category, files] of Object.entries(categories)) {{
                // 过滤文件
                const filteredFiles = files.filter(f => 
                    f.name.toLowerCase().includes(filterText.toLowerCase())
                );
                
                if (filteredFiles.length === 0) continue;
                
                hasContent = true;
                const section = document.createElement('div');
                section.className = 'category-section';
                
                const icon = iconMap[category] || 'fa-folder-open';
                
                section.innerHTML = `
                    <h2 class="category-title">
                        <i class="fas ${{icon}}"></i> ${{category}}
                    </h2>
                    <div class="grid">
                        ${{filteredFiles.map(file => `
                            <a href="${{file.path}}" class="card" target="_blank">
                                <div class="card-icon">
                                    <i class="fas fa-file-code"></i>
                                </div>
                                <div class="card-title">${{file.name}}</div>
                                <div class="card-meta">
                                    <span><i class="far fa-clock"></i> ${{file.mtime}}</span>
                                    <span>${{file.size}}</span>
                                </div>
                            </a>
                        `).join('')}}
                    </div>
                `;
                
                contentDiv.appendChild(section);
            }}
            
            if (!hasContent) {{
                contentDiv.innerHTML = `
                    <div class="empty-state">
                        <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 20px;"></i>
                        <p>未找到匹配的项目</p>
                    </div>
                `;
            }}
        }}
        
        // 初始渲染
        render();
        
        // 搜索事件
        searchInput.addEventListener('input', (e) => {{
            render(e.target.value);
        }});
    </script>
</body>
</html>
"""
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"成功生成 {OUTPUT_FILE}")
    print(f"包含 {len(categories)} 个分类")

if __name__ == '__main__':
    data = scan_directory()
    generate_html(data)
