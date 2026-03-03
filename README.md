# PDF 工具集

一个简单、美观且免费的本地 PDF 处理桌面应用程序。

## 功能特性

*   **合并 PDF**: 将多个 PDF 文件合并为一个，支持在列表中拖拽调整合并顺序。
*   **拆分 PDF**:
    *   将所有页面拆分为独立的 PDF 文件。
    *   提取特定页码（或范围，例如：1,3,5-7）生成新的 PDF 文件。
*   **占位功能**: 主页提供了几个典型的“敬请期待”占位卡片（如压缩PDF、PDF转Word等），方便未来功能扩充。

## 环境依赖

*   Python 3.7+
*   [PyQt6](https://pypi.org/project/PyQt6/) (用于提供美观的图形用户界面)
*   [pypdf](https://pypi.org/project/pypdf/) (用于处理 PDF 的合并与拆分核心逻辑)

## 安装与运行指南

1.  **克隆或下载本代码库**
2.  **创建虚拟环境（可选但推荐）**
    ```bash
    python3 -m venv venv
    source venv/bin/activate # Linux/Mac
    venv\Scripts\activate # Windows
    ```
3.  **安装依赖库**
    项目根目录下提供了一个 `requirements.txt` 文件，您可以直接运行以下命令安装：
    ```bash
    pip install -r requirements.txt
    ```
4.  **运行程序**
    ```bash
    python main.py
    ```

## 目录结构说明

*   `main.py`: 应用程序的主入口，负责窗口初始化与页面导航控制。
*   `ui/`: 存放所有界面相关的代码文件。
    *   `home_page.py`: 主页面及其卡片组件的实现。
    *   `merge_page.py`: 合并 PDF 页面的实现。
    *   `split_page.py`: 拆分 PDF 页面的实现。
*   `utils/`: 存放底层功能逻辑文件。
    *   `pdf_utils.py`: 封装了通过 `pypdf` 进行合并、拆分和提取 PDF 的具体实现。
*   `requirements.txt`: 列出了项目运行必须安装的依赖库。
