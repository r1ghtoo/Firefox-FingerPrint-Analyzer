import sys
import os
import json
import html,time
import subprocess
from collections import defaultdict
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem,QLabel, QFileDialog, QProgressDialog, QTreeWidget, QTreeWidgetItem,
    QGroupBox, QHeaderView, QSpinBox, QDialog, QColorDialog, QComboBox, QFormLayout,
    QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt6.QtGui import QFont, QColor

DEFAULT_SETTINGS = {
    'font_size': 14,
    'font_family': 'Microsoft YaHei',
    'primary_color': '#07C160',
    'accent_color': '#576B95',
    'bg_color': '#EDEDED',
    'card_color': '#FFFFFF',
    'firefox_path': r''# 新增
}

class SettingsDialog(QDialog):
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.settings = settings.copy()
        self.setWindowTitle("设置")
        self.setFixedSize(400, 350)
        self.setStyleSheet("""
            QDialog { background: #EDEDED; }
            QLabel { color: #191919; font-size: 14px; }
            QSpinBox, QComboBox { 
                background: white; border: 1px solid #E5E5E5; 
                border-radius: 6px; padding: 8px; min-width: 150px;
            }
            QPushButton { 
                background: #07C160; color: white; border: none; 
                border-radius: 6px; padding: 10px 20px; font-weight: 600;
            }
            QPushButton:hover { background: #06AD56; }
            QPushButton#colorBtn { background: white; border: 1px solid #E5E5E5; min-width: 150px; }
            QGroupBox { 
                background: white; border: none; border-radius: 8px; 
                margin-top: 8px; padding: 16px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        font_group = QGroupBox("字体设置")
        font_layout = QFormLayout(font_group)
        
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems(['Microsoft YaHei', 'PingFang SC', 'SimHei', 'Arial', 'Consolas', 'Segoe UI'])
        self.font_family_combo.setCurrentText(self.settings['font_family'])
        font_layout.addRow("字体:", self.font_family_combo)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 28)
        self.font_size_spin.setValue(self.settings['font_size'])
        font_layout.addRow("大小:", self.font_size_spin)
        
        layout.addWidget(font_group)
        
        color_group = QGroupBox("颜色设置")
        color_layout = QFormLayout(color_group)
        
        self.color_btns = {}
        color_labels = {'primary_color': '主题色', 'accent_color': '强调色', 'bg_color': '背景色', 'card_color': '卡片色'}
        for key, label in color_labels.items():
            btn = QPushButton()
            btn.setObjectName("colorBtn")
            btn.setStyleSheet(f"background: {self.settings[key]}; border: 1px solid #E5E5E5;")
            btn.clicked.connect(lambda checked, k=key: self.pick_color(k))
            self.color_btns[key] = btn
            color_layout.addRow(f"{label}:", btn)
        
        layout.addWidget(color_group)
        
        btn_layout = QHBoxLayout()
        reset_btn = QPushButton("恢复默认")
        reset_btn.setStyleSheet("background: #576B95;")
        reset_btn.clicked.connect(self.reset_defaults)
        btn_layout.addWidget(reset_btn)
        
        save_btn = QPushButton("保存设置")
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def pick_color(self, key):
        color = QColorDialog.getColor(QColor(self.settings[key]), self, "选择颜色")
        if color.isValid():
            self.settings[key] = color.name()
            self.color_btns[key].setStyleSheet(f"background: {color.name()}; border: 1px solid #E5E5E5;")
    
    def reset_defaults(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.font_family_combo.setCurrentText(self.settings['font_family'])
        self.font_size_spin.setValue(self.settings['font_size'])
        for key, btn in self.color_btns.items():
            btn.setStyleSheet(f"background: {self.settings[key]}; border: 1px solid #E5E5E5;")
    
    def get_settings(self):
        self.settings['font_family'] = self.font_family_combo.currentText()
        self.settings['font_size'] = self.font_size_spin.value()
        return self.settings

def get_style(s):
    rainbow_border = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF6B6B, stop:0.25 #FFE66D, stop:0.5 #4ECDC4, stop:0.75 #45B7D1, stop:1 #96E6A1)"
    return f"""
    * {{ font-family: "{s['font_family']}", sans-serif; font-size: {s['font_size']}px; }}
    QMainWindow {{ background: {s['bg_color']}; }}
    QGroupBox {{ 
        background: {s['card_color']}; color: #191919; border: none; border-radius: 8px; 
        margin-top: 8px; padding: 16px; padding-top: 24px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin; left: 16px; top: 8px; 
        color: {s['accent_color']}; font-weight: 600;
    }}
    QLineEdit {{ 
        background: #F7F7F7; color: #191919; border: 1px solid #E5E5E5; 
        border-radius: 6px; padding: 10px 12px;
    }}
    QLineEdit:focus {{ border-color: {s['primary_color']}; background: white; }}
    QPushButton {{ 
        background: {s['primary_color']}; color: white; border: 3px solid transparent; 
        border-radius: 8px; padding: 12px 24px; font-weight: 600;
    }}
    QPushButton:hover {{ 
        border: 3px solid;
        border-image: {rainbow_border} 1;border-radius: 8px;
    }}
    QPushButton:pressed {{ 
        border: 4px solid; 
        border-image: {rainbow_border} 1;
        background: {s['primary_color']}cc;
    }}
    QPushButton#stopBtn {{ background: #FA5151; }}
    QPushButton#stopBtn:hover {{ 
        background: #FA5151; 
        border: 3px solid; 
        border-image: {rainbow_border} 1;
    }}
    QPushButton#secondaryBtn {{ background: {s['accent_color']}; padding: 10px 16px; }}
    QPushButton#secondaryBtn:hover {{ 
        border: 3px solid; 
        border-image: {rainbow_border} 1;
    }}
    QPushButton#dangerBtn {{ background: #FA5151; padding: 10px 16px; }}
    QPushButton#dangerBtn:hover {{ 
        border: 3px solid; 
        border-image: {rainbow_border} 1;
    }}
    QTabWidget::pane {{ 
        background: {s['card_color']}; border: none; border-radius: 8px; margin-top: -1px;
    }}
    QTabBar::tab {{ 
        background: #F7F7F7; color: {s['accent_color']}; padding: 12px 24px; 
        border: none; margin-right: 2px; border-top-left-radius: 8px; border-top-right-radius: 8px;
    }}
    QTabBar::tab:selected {{ background: {s['card_color']}; color: {s['primary_color']}; font-weight: 600; }}
    QTabBar::tab:hover {{ background: #EDEDED; }}
    QTableWidget, QTreeWidget {{ 
        background: {s['card_color']}; color: #191919; border: none; 
        gridline-color: #F0F0F0; alternate-background-color: #FAFAFA;
    }}
    QTableWidget::item, QTreeWidget::item {{ padding: 8px; border-bottom: 1px solid #F0F0F0; }}
    QTableWidget::item:selected, QTreeWidget::item:selected {{ background: #E8F5E9; color: #191919; }}
    QHeaderView::section {{ 
        background: #F7F7F7; color: {s['accent_color']}; padding: 12px 8px; 
        border: none; border-bottom: 2px solid {s['primary_color']}; font-weight: 600;
    }}
    QLabel {{ color: #191919; }}
    QLabel#titleLabel {{ color: {s['accent_color']}; font-weight: 600; }}
    QScrollBar:vertical {{ background: #F7F7F7; width: 8px; border-radius: 4px; }}
    QScrollBar::handle:vertical {{ background: #C0C0C0; border-radius: 4px; min-height: 30px; }}
    QScrollBar::handle:vertical:hover {{ background: #A0A0A0; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    """

class LogParser(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def run(self):
        result = {'stats': defaultdict(lambda: defaultdict(int)), 'network': [], 'console': [], 'canvas': []}
        canvas_interfaces = {
            'HTMLCanvasElement': ['toDataURL', 'getContext', 'toBlob'],
            'CanvasRenderingContext2D': [
                'fillText', 'strokeText', 'measureText', 'getImageData', 'putImageData',
                'fillRect', 'strokeRect', 'arc', 'ellipse', 'bezierCurveTo', 'quadraticCurveTo',
                'createRadialGradient', 'createLinearGradient', 'drawImage', 'fill', 'stroke',
                'isPointInPath', 'createPattern'
            ],
            'TextMetrics': ['width', 'actualBoundingBoxAscent', 'actualBoundingBoxDescent',
                           'actualBoundingBoxLeft', 'actualBoundingBoxRight',
                           'fontBoundingBoxAscent', 'fontBoundingBoxDescent'],
            'OffscreenCanvas': ['getContext', 'convertToBlob'],
            'OffscreenCanvasRenderingContext2D': ['fillText', 'strokeText', 'getImageData'],}

        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            total = len(lines)
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith('JavaScript error:') or not line:
                    continue
                try:
                    data = json.loads(line)
                    log_type = data.get('type', '')
                    iface = data.get('interface','Unknown')
                    member = data.get('member', data.get('method', 'Unknown'))
                    result['stats'][iface][member] += 1
                    # Canvas指纹检测
                    if iface in canvas_interfaces:
                        if member in canvas_interfaces[iface] or not canvas_interfaces[iface]:
                            result['canvas'].append(data)
                    
                    # 网络/Cookie检测
                    is_network = (
                        (iface == 'Window' and member == 'fetch') or
                        (iface == 'XMLHttpRequest' and member in ('open', 'send', 'setRequestHeader')) or
                        iface in ('Request', 'Response')
                    )
                    is_cookie = (iface == 'Document' and 'cookie' in member.lower())
                    
                    if is_network or is_cookie:
                        result['network'].append(data)
                    
                    if log_type == 'console':
                        result['console'].append(data)
                except json.JSONDecodeError:
                    pass
                if i % 100 == 0:
                    self.progress.emit(int((i + 1) / total * 100))
            self.progress.emit(100)
        except Exception as e:
            print(f"Error: {e}")
        self.finished.emit(result)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.process = None
        self.settings = DEFAULT_SETTINGS.copy()
        self.qsettings = QSettings('DOMAnalyzer', 'Settings')
        self.load_settings()
        
        self.setWindowTitle("RUYI DOM/BOM/Fingerprint Analyzer")
        self.setMinimumSize(1200, 750)
        self.apply_style()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        ctrl_group = QGroupBox("控制面板")
        ctrl_layout = QVBoxLayout(ctrl_group)
        ctrl_layout.setSpacing(12)
        
        url_layout = QHBoxLayout()
        url_label = QLabel("目标网址:")
        url_label.setObjectName("titleLabel")
        url_label.setFixedWidth(70)
        url_layout.addWidget(url_label)
        self.url_input = QLineEdit("https://demo.fingerprint.com/playground")
        url_layout.addWidget(self.url_input)
        ctrl_layout.addLayout(url_layout)

        file_layout = QHBoxLayout()
        browser_layout = QHBoxLayout()
        browser_label = QLabel("浏览器:")
        browser_label.setObjectName("titleLabel")
        browser_label.setFixedWidth(70)
        browser_layout.addWidget(browser_label)
        self.browser_input = QLineEdit(self.settings.get('firefox_path', DEFAULT_SETTINGS['firefox_path']))
        browser_layout.addWidget(self.browser_input)
        self.browser_browse_btn = QPushButton("选择")
        self.browser_browse_btn.setObjectName("secondaryBtn")
        self.browser_browse_btn.setFixedWidth(70)
        self.browser_browse_btn.clicked.connect(self.browse_browser)
        browser_layout.addWidget(self.browser_browse_btn)
        ctrl_layout.addLayout(browser_layout)

        file_label = QLabel("日志路径:")
        file_label.setObjectName("titleLabel")
        file_label.setFixedWidth(70)
        file_layout.addWidget(file_label)
        self.file_input = QLineEdit("C:/firefox/domtrace.txt")
        file_layout.addWidget(self.file_input)
        self.browse_btn = QPushButton("选择")
        self.browse_btn.setObjectName("secondaryBtn")
        self.browse_btn.setFixedWidth(70)
        self.browse_btn.clicked.connect(self.browse_file)
        self.open_log_btn = QPushButton("打开")
        self.open_log_btn.setObjectName("secondaryBtn")
        self.open_log_btn.setFixedWidth(70)
        self.open_log_btn.clicked.connect(self.open_log_file)
        file_layout.addWidget(self.open_log_btn)
        file_layout.addWidget(self.browse_btn)
        ctrl_layout.addLayout(file_layout)
        
        btn_layout = QHBoxLayout()
        self.toggle_btn = QPushButton("启动浏览器 && 开始记录")
        self.toggle_btn.clicked.connect(self.toggle_browser)
        btn_layout.addWidget(self.toggle_btn)
        
        self.clear_btn = QPushButton("清除日志")
        self.clear_btn.setObjectName("dangerBtn")
        self.clear_btn.setFixedWidth(100)
        self.clear_btn.clicked.connect(self.clear_log)
        btn_layout.addWidget(self.clear_btn)
        
        self.settings_btn = QPushButton("设置")
        self.settings_btn.setObjectName("secondaryBtn")
        self.settings_btn.setFixedWidth(80)
        self.settings_btn.clicked.connect(self.open_settings)
        btn_layout.addWidget(self.settings_btn)
        
        ctrl_layout.addLayout(btn_layout)
        layout.addWidget(ctrl_group)
        
        self.tabs = QTabWidget()
        
        # Tab1: 统计
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.setContentsMargins(0, 8, 0, 0)
        self.stats_tree = QTreeWidget()
        self.stats_tree.setHeaderLabels(["接口 / 方法", "调用次数"])
        self.stats_tree.setAlternatingRowColors(True)
        self.stats_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.stats_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.stats_tree.header().resizeSection(1, 120)
        stats_layout.addWidget(self.stats_tree)
        self.tabs.addTab(stats_widget, "📊 总体统计")
        
        # Tab2: 网络/Cookie
        network_widget = QWidget()
        network_layout = QVBoxLayout(network_widget)
        network_layout.setContentsMargins(0, 8, 0, 0)
        self.network_table = QTableWidget()
        self.network_table.setColumnCount(6)
        self.network_table.setHorizontalHeaderLabels(["序号", "类型", "接口", "方法", "参数/值", "调用栈"])
        self.network_table.setAlternatingRowColors(True)
        self.network_table.setWordWrap(True)
        self.network_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # 前4列自适应内容宽度
        for col in range(4):
            self.network_table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        # 后2列拉伸
        self.network_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.network_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        network_layout.addWidget(self.network_table)
        self.tabs.addTab(network_widget, "🌐 网络/Cookie")
        
        # Tab3: Console
        console_widget = QWidget()
        console_layout = QVBoxLayout(console_widget)
        console_layout.setContentsMargins(0, 8, 0, 0)
        self.console_table = QTableWidget()
        self.console_table.setColumnCount(4)
        self.console_table.setHorizontalHeaderLabels(["序号", "类型", "内容", "来源"])
        self.console_table.setAlternatingRowColors(True)
        self.console_table.setWordWrap(True)
        self.console_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.console_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.console_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.console_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.console_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        console_layout.addWidget(self.console_table)
        self.tabs.addTab(console_widget, "📝 Console")

        canvas_widget = QWidget()
        canvas_layout = QVBoxLayout(canvas_widget)
        canvas_layout.setContentsMargins(0, 8, 0, 0)
        self.canvas_table = QTableWidget()
        self.canvas_table.setColumnCount(5)
        self.canvas_table.setHorizontalHeaderLabels(["序号", "接口", "方法", "参数/返回值", "调用栈"])
        self.canvas_table.setAlternatingRowColors(True)
        self.canvas_table.setWordWrap(True)
        self.canvas_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        for col in range(3):
            self.canvas_table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        self.canvas_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.canvas_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        canvas_layout.addWidget(self.canvas_table)
        self.tabs.addTab(canvas_widget, "🎨 Canvas指纹")


        layout.addWidget(self.tabs, 1)

    def open_log_file(self):
        log_file = self.file_input.text()
        if os.path.exists(log_file):
            os.startfile(log_file)  # Windows
        else:
            QMessageBox.warning(self, "错误", "日志文件不存在")

    def load_settings(self):
        for key in DEFAULT_SETTINGS:
            self.settings[key] = self.qsettings.value(key, DEFAULT_SETTINGS[key])
            if key == 'font_size':
                self.settings[key] = int(self.settings[key])
    
    def save_settings(self):
        for key, value in self.settings.items():
            self.qsettings.setValue(key, value)
    
    def apply_style(self):
        self.setStyleSheet(get_style(self.settings))
    
    def open_settings(self):
        dialog = SettingsDialog(self, self.settings)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.settings = dialog.get_settings()
            self.save_settings()
            self.apply_style()
    
    def clear_log(self):
        log_file = self.file_input.text()
        reply = QMessageBox.question(self, "确认清除", f"确定要清除日志文件吗？\n{log_file}",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if os.path.exists(log_file):
                    os.remove(log_file)
                self.stats_tree.clear()
                self.network_table.setRowCount(0)
                self.console_table.setRowCount(0)
                QMessageBox.information(self, "成功", "日志已清除")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"清除失败: {e}")
    
    def browse_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "选择日志保存位置", "", "Text Files (*.txt)")
        if path:
            self.file_input.setText(path)

    def browse_browser(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择Firefox可执行文件", "", "Executable (*.exe);;All Files (*)")
        if path:
            self.browser_input.setText(path)
            self.settings['firefox_path'] = path
            self.save_settings()
    
    def toggle_browser(self):
        if self.process is None:
            self.start_browser()
        else:
            self.stop_browser()

    def _cleanup_firefox(self):
        """清理Firefox残留"""
        import glob
        
        # 杀掉残留进程
        if sys.platform == 'win32':
            os.system('taskkill /f /im firefox.exe >nul 2>&1')
        else:
            os.system('pkill -9 firefox2>/dev/null')
        
        time.sleep(0.5)


    def start_browser(self):
        self._cleanup_firefox()

        url = self.url_input.text()
        log_file = self.file_input.text()
        firefox_path = self.browser_input.text()  # 改这一行
        
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        cmd = f'"{firefox_path}" "{url}" 2>"{log_file}"'
        self.process = subprocess.Popen(cmd, shell=True)
        self.toggle_btn.setText("关闭浏览器 && 停止记录")
        self.toggle_btn.setObjectName("stopBtn")
        self.toggle_btn.setStyle(self.toggle_btn.style())

    def stop_browser(self):
        if self.process:
            subprocess.run("taskkill /F /IM firefox.exe", shell=True, capture_output=True)
            self.process = None
        
        self.toggle_btn.setText("启动浏览器 && 开始记录")
        self.toggle_btn.setObjectName("")
        self.toggle_btn.setStyle(self.toggle_btn.style())
        self.parse_log()
    
    def parse_log(self):
        log_file = self.file_input.text()
        if not os.path.exists(log_file):
            return
        
        self.progress_dialog = QProgressDialog("正在解析日志文件...", None, 0, 100, self)
        self.progress_dialog.setWindowTitle("解析中")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setMinimumWidth(350)
        self.progress_dialog.setStyleSheet(f"""
            QProgressDialog {{ background: white; border-radius: 8px; }}
            QLabel {{ color: #191919; font-size: {self.settings['font_size']}px; padding: 16px; }}
            QProgressBar {{ 
                border: none; border-radius: 6px; background: #F0F0F0; 
                text-align: center; color: #191919; min-height: 20px;
            }}
            QProgressBar::chunk {{ background: {self.settings['primary_color']}; border-radius: 6px; }}
        """)
        self.progress_dialog.show()
        
        self.parser = LogParser(log_file)
        self.parser.progress.connect(self.progress_dialog.setValue)
        self.parser.finished.connect(self.display_results)
        self.parser.start()
    
    def display_results(self, result):
        self.progress_dialog.close()
        
        # 统计 - 按字母顺序排序
        self.stats_tree.clear()
        total =0
        for iface, members in sorted(result['stats'].items(), key=lambda x: x[0].lower()):
            iface_total = sum(members.values())
            total += iface_total
            parent = QTreeWidgetItem([iface, f"{iface_total:,}"])
            parent.setForeground(0, QColor(self.settings['accent_color']))
            for member, count in sorted(members.items(), key=lambda x: x[0].lower()):
                child = QTreeWidgetItem([f".{member}", f"{count:,}"])
                parent.addChild(child)
            self.stats_tree.addTopLevelItem(parent)

        summary = QTreeWidgetItem([f"总计 ({len(result['stats'])} 个接口)", f"{total:,}"])
        summary.setForeground(0, QColor(self.settings['primary_color']))
        summary.setFont(0, QFont("", -1, QFont.Weight.Bold))
        summary.setFont(1, QFont("", -1, QFont.Weight.Bold))
        self.stats_tree.insertTopLevelItem(0, summary)
        self.stats_tree.expandAll()
        if total == 0:
            empty_item = QTreeWidgetItem(["未检测到任何接口调用", ""])
            empty_item.setForeground(0, QColor("#999999"))
            self.stats_tree.addTopLevelItem(empty_item)
        
        # 网络/Cookie
        self.network_table.setRowCount(len(result['network']))
        for i, item in enumerate(result['network']):
            seq = str(item.get('seq', ''))
            log_type = item.get('type', '')
            iface = item.get('interface', '')
            member = item.get('member', '')
            if'args' in item:
                value = json.dumps(item['args'], ensure_ascii=False, indent=2)
            elif 'value' in item:
                value = str(item['value'])
            else:
                value = ''
            
            stack = item.get('stack', [])
            if stack:
                s = stack[0]
                file_name = s.get('file', '')
                stack_str = f"{s.get('func', '')} @ {file_name}:{s.get('line', '')}:{s.get('col', '')}"
            else:
                stack_str = ''
            
            self.network_table.setItem(i, 0, QTableWidgetItem(seq))
            self.network_table.setItem(i, 1, QTableWidgetItem(log_type))
            self.network_table.setItem(i, 2, QTableWidgetItem(iface))
            self.network_table.setItem(i, 3, QTableWidgetItem(member))
            
            value_item = QTableWidgetItem(value)
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            self.network_table.setItem(i, 4, value_item)
            
            stack_item = QTableWidgetItem(stack_str)
            stack_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            self.network_table.setItem(i, 5, stack_item)
        if len(result['network']) == 0:
            self.network_table.setRowCount(1)
            empty_item = QTableWidgetItem("未检测到网络请求或Cookie操作")
            empty_item.setForeground(QColor("#999999"))
            self.network_table.setItem(0, 0, empty_item)
            self.network_table.setSpan(0, 0, 1, 6)

        # Console
        self.console_table.setRowCount(len(result['console']))
        for i, item in enumerate(result['console']):
            seq = str(item.get('seq', ''))
            method = item.get('method', 'log')
            args = item.get('args', [])
            # 完整显示args内容
            content = json.dumps(args, ensure_ascii=False, indent=2)
            file_info = item.get('file', '')
            line = item.get('line', '')
            source = f"{file_info.split('/')[-1]}:{line}" if file_info else ''
            
            self.console_table.setItem(i, 0, QTableWidgetItem(seq))
            method_item = QTableWidgetItem(method)
            color_map = {'error': '#FA5151', 'warn': '#FFC300', 'info': '#576B95', 'log': '#191919'}
            method_item.setForeground(QColor(color_map.get(method, '#191919')))
            self.console_table.setItem(i, 1, method_item)
            
            content_item = QTableWidgetItem(content)
            content_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            self.console_table.setItem(i, 2, content_item)
            
            self.console_table.setItem(i, 3, QTableWidgetItem(source))

        if len(result['console']) == 0:
            self.console_table.setRowCount(1)
            empty_item = QTableWidgetItem("未检测到Console日志")
            empty_item.setForeground(QColor("#999999"))
            self.console_table.setItem(0, 0, empty_item)
            self.console_table.setSpan(0, 0, 1, 4)

        # Canvas指纹
        self.canvas_table.setRowCount(len(result['canvas']))
        for i, item in enumerate(result['canvas']):
            seq = str(item.get('seq', ''))
            iface = item.get('interface', '')
            member = item.get('member', '')
            
            # 参数和返回值
            value_parts = []
            if 'args' in item:
                value_parts.append(f"args: {json.dumps(item['args'], ensure_ascii=False)}")
            if 'return' in item:
                ret = item['return']
                # 截断base64数据
                if isinstance(ret, str) and ret.startswith('data:image'):
                    ret = ret[:80] + '...[base64]'
                value_parts.append(f"return: {ret}")
            if'value' in item:
                value_parts.append(f"value: {item['value']}")
            value = '\n'.join(value_parts)
            
            stack = item.get('stack', [])
            if stack:
                s = stack[0]
                file_name = s.get('file', '')
                stack_str = f"{s.get('func', '')} @ {file_name}:{s.get('line', '')}:{s.get('col', '')}"
            else:
                stack_str = ''
            
            self.canvas_table.setItem(i, 0, QTableWidgetItem(seq))
            self.canvas_table.setItem(i, 1, QTableWidgetItem(iface))
            self.canvas_table.setItem(i, 2, QTableWidgetItem(member))
            value_item = QTableWidgetItem(value)
            value_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            self.canvas_table.setItem(i, 3, value_item)
            
            stack_item = QTableWidgetItem(stack_str)
            stack_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            self.canvas_table.setItem(i, 4, stack_item)
        
        if len(result['canvas']) == 0:
            self.canvas_table.setRowCount(1)
            empty_item = QTableWidgetItem("未检测到Canvas指纹相关调用")
            empty_item.setForeground(QColor("#999999"))
            self.canvas_table.setItem(0, 0, empty_item)
            self.canvas_table.setSpan(0, 0, 1, 5)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())