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
    <link rel="stylesheet" href="style.css">
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
