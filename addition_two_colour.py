from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import ctypes
from ctypes import wintypes

class TotalStealthOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Total Stealth Overlay")
        self.setGeometry(100, 100, 300, 150)
        
        # Enhanced window flags
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | 
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )
        
        # Resizing variables
        self.resizing = False
        self.resize_edge = None
        self.resize_margin = 10
        self.min_size = (100, 50)
        
        # Dragging variables
        self.dragging = False
        self.drag_position = None
        
        self.setup_ui()
        
        # Add keyboard shortcuts for stealth options
        self.setup_keyboard_shortcuts()
        
        # Apply stealth immediately and maintain it
        QtCore.QTimer.singleShot(10, self.apply_permanent_stealth)  # Faster initial stealth
        
        # Keep stealth active continuously - more frequent checks
        self.stealth_timer = QtCore.QTimer()
        self.stealth_timer.timeout.connect(self.maintain_stealth)
        self.stealth_timer.start(50)  # Check every 50ms instead of 100ms
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Header with controls
        header_layout = QtWidgets.QHBoxLayout()
        
        # Status label
        self.status_label = QtWidgets.QLabel("TOTAL STEALTH")
        self.status_label.setStyleSheet("color: red; font-weight: bold; font-size: 10px;")
        header_layout.addWidget(self.status_label)
        
        header_layout.addStretch()
        
        # Control buttons - all will be stealth
        self.options_btn = QtWidgets.QPushButton("⚙")
        self.options_btn.setMaximumSize(25, 25)
        self.options_btn.setStyleSheet("QPushButton { background-color: blue; color: white; border: none; font-weight: bold; }")
        self.options_btn.clicked.connect(self.show_stealth_options)
        header_layout.addWidget(self.options_btn)
        
        self.minimize_btn = QtWidgets.QPushButton("−")
        self.minimize_btn.setMaximumSize(25, 25)
        self.minimize_btn.setStyleSheet("QPushButton { background-color: orange; color: white; border: none; font-weight: bold; }")
        self.minimize_btn.clicked.connect(self.toggle_minimize)
        header_layout.addWidget(self.minimize_btn)
        
        self.close_btn = QtWidgets.QPushButton("×")
        self.close_btn.setMaximumSize(25, 25)
        self.close_btn.setStyleSheet("QPushButton { background-color: red; color: white; border: none; font-weight: bold; }")
        self.close_btn.clicked.connect(self.close)
        header_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(header_layout)
        
        # Content area
        self.content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout()
        
        # Size display
        self.size_label = QtWidgets.QLabel("Size: 300x150")
        self.size_label.setStyleSheet("color: gray; font-size: 9px;")
        content_layout.addWidget(self.size_label)
        
        # Quick action buttons (all stealth)
        quick_layout = QtWidgets.QHBoxLayout()
        
        red_btn = QtWidgets.QPushButton("R")
        red_btn.setMaximumSize(20, 20)
        red_btn.setStyleSheet("QPushButton { background-color: red; color: white; border: none; font-size: 8px; }")
        red_btn.clicked.connect(lambda: self.stealth_color_change("red"))
        quick_layout.addWidget(red_btn)
        
        blue_btn = QtWidgets.QPushButton("B")
        blue_btn.setMaximumSize(20, 20)
        blue_btn.setStyleSheet("QPushButton { background-color: blue; color: white; border: none; font-size: 8px; }")
        blue_btn.clicked.connect(lambda: self.stealth_color_change("blue"))
        quick_layout.addWidget(blue_btn)
        
        green_btn = QtWidgets.QPushButton("G")
        green_btn.setMaximumSize(20, 20)
        green_btn.setStyleSheet("QPushButton { background-color: green; color: white; border: none; font-size: 8px; }")
        green_btn.clicked.connect(lambda: self.stealth_color_change("green"))
        quick_layout.addWidget(green_btn)
        
        small_btn = QtWidgets.QPushButton("S")
        small_btn.setMaximumSize(20, 20)
        small_btn.setStyleSheet("QPushButton { background-color: gray; color: white; border: none; font-size: 8px; }")
        small_btn.clicked.connect(lambda: self.stealth_resize(150, 80))
        quick_layout.addWidget(small_btn)
        
        big_btn = QtWidgets.QPushButton("L")
        big_btn.setMaximumSize(20, 20)
        big_btn.setStyleSheet("QPushButton { background-color: gray; color: white; border: none; font-size: 8px; }")
        big_btn.clicked.connect(lambda: self.stealth_resize(400, 200))
        quick_layout.addWidget(big_btn)
        
        content_layout.addLayout(quick_layout)
        
        # Info text - updated with keyboard shortcuts
        info_label = QtWidgets.QLabel("Drag edges to resize • Press ⚙ for keyboard shortcuts")
        info_label.setStyleSheet("color: gray; font-size: 8px;")
        info_label.setAlignment(QtCore.Qt.AlignCenter)
        content_layout.addWidget(info_label)
        
        self.content_widget.setLayout(content_layout)
        main_layout.addWidget(self.content_widget)
        
        self.setLayout(main_layout)
        
        # Apply styling
        self.apply_style()
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for ZERO-FLASH options"""
        # Size shortcuts
        QtWidgets.QShortcut(QtGui.QKeySequence("1"), self, lambda: self.stealth_resize(100, 60))   # Tiny
        QtWidgets.QShortcut(QtGui.QKeySequence("2"), self, lambda: self.stealth_resize(150, 80))   # Small
        QtWidgets.QShortcut(QtGui.QKeySequence("3"), self, lambda: self.stealth_resize(300, 150))  # Medium
        QtWidgets.QShortcut(QtGui.QKeySequence("4"), self, lambda: self.stealth_resize(400, 200))  # Large
        QtWidgets.QShortcut(QtGui.QKeySequence("5"), self, lambda: self.stealth_resize(500, 300))  # Huge
        
        # Color shortcuts
        QtWidgets.QShortcut(QtGui.QKeySequence("R"), self, lambda: self.stealth_color_change("red"))
        QtWidgets.QShortcut(QtGui.QKeySequence("B"), self, lambda: self.stealth_color_change("blue"))
        QtWidgets.QShortcut(QtGui.QKeySequence("G"), self, lambda: self.stealth_color_change("green"))
        QtWidgets.QShortcut(QtGui.QKeySequence("P"), self, lambda: self.stealth_color_change("purple"))
        
        # Position shortcuts
        QtWidgets.QShortcut(QtGui.QKeySequence("Q"), self, lambda: self.stealth_move_to_corner("top-left"))
        QtWidgets.QShortcut(QtGui.QKeySequence("W"), self, lambda: self.stealth_move_to_corner("top-right"))
        QtWidgets.QShortcut(QtGui.QKeySequence("E"), self, lambda: self.stealth_move_to_corner("center"))
        QtWidgets.QShortcut(QtGui.QKeySequence("A"), self, lambda: self.stealth_move_to_corner("bottom-left"))
        QtWidgets.QShortcut(QtGui.QKeySequence("D"), self, lambda: self.stealth_move_to_corner("bottom-right"))
        
    def stealth_move_to_corner(self, corner):
        """Move to corner with ZERO flash"""
        # Prevent visual updates
        self.setUpdatesEnabled(False)
        
        # Apply stealth BEFORE moving
        hwnd = int(self.winId())
        WDA_EXCLUDEFROMCAPTURE = 0x00000011
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        size = self.size()
        
        positions = {
            "top-left": (10, 10),
            "top-right": (screen.width() - size.width() - 10, 10),
            "bottom-left": (10, screen.height() - size.height() - 50),
            "bottom-right": (screen.width() - size.width() - 10, screen.height() - size.height() - 50),
            "center": ((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
        }
        
        if corner in positions:
            self.move(*positions[corner])
        
        # Re-enable updates
        self.setUpdatesEnabled(True)
        # Variables for minimize state
        self.is_minimized = False
        self.normal_size = None
        
        # Enhanced resizing variables
        self.resize_corner = None
        self.resize_start_size = None
        
    def apply_style(self):
        """Apply the red border styling"""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 220);
                border: 3px solid red;
                color: red;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        
    def show_stealth_options(self):
        """Show options WITHOUT any flash - keyboard shortcuts instead"""
        print("\n🎯 STEALTH OPTIONS (No visual dialogs!):")
        print("Keyboard Shortcuts:")
        print("• Press 1-5 for sizes: 1=Tiny, 2=Small, 3=Medium, 4=Large, 5=Huge")
        print("• Press R/B/G/P for colors: R=Red, B=Blue, G=Green, P=Purple")
        print("• Press Q/W/E/A/D for positions: Q=Top-Left, W=Top-Right, E=Center, A=Bottom-Left, D=Bottom-Right")
        print("• Current size: {}x{}".format(self.width(), self.height()))
        
        # DO NOT create any visible dialog - use keyboard only
        # This prevents ANY flashing
        self.setFocus()  # Ensure keyboard focus
        
    def stealth_color_change(self, color):
        """Change color without breaking stealth - NO FLASHING"""
        # Prevent any visual updates during change
        self.setUpdatesEnabled(False)
        
        # Apply stealth BEFORE making changes
        hwnd = int(self.winId())
        WDA_EXCLUDEFROMCAPTURE = 0x00000011
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        
        # Make the style change
        self.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(255, 255, 255, 220);
                border: 3px solid {color};
                color: {color};
                font-size: 11px;
                font-weight: bold;
            }}
        """)
        
        # Re-enable updates
        self.setUpdatesEnabled(True)
        print(f"✓ Color changed to {color} - NO FLASH, STEALTH MAINTAINED")
        
    def stealth_resize(self, width, height):
        """Resize without breaking stealth - NO FLASHING"""
        # Prevent visual updates during resize
        self.setUpdatesEnabled(False)
        
        # Apply stealth BEFORE resizing
        hwnd = int(self.winId())
        WDA_EXCLUDEFROMCAPTURE = 0x00000011
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        
        # Perform resize
        self.resize(width, height)
        self.update_size_label()
        
        # Re-enable updates
        self.setUpdatesEnabled(True)
        print(f"✓ Resized to {width}x{height} - NO FLASH, STEALTH MAINTAINED")
        
    def toggle_minimize(self):
        """Toggle minimize state - NO FLASHING"""
        # Prevent visual updates during minimize
        self.setUpdatesEnabled(False)
        
        # Apply stealth BEFORE minimize action
        hwnd = int(self.winId())
        WDA_EXCLUDEFROMCAPTURE = 0x00000011
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        
        if self.is_minimized:
            if self.normal_size:
                self.resize(self.normal_size)
            self.content_widget.show()
            self.minimize_btn.setText("−")
            self.is_minimized = False
        else:
            self.normal_size = self.size()
            self.resize(200, 35)
            self.content_widget.hide()
            self.minimize_btn.setText("□")
            self.is_minimized = True
            
        self.update_size_label()
        
        # Re-enable updates
        self.setUpdatesEnabled(True)
        print("✓ Minimize toggled - NO FLASH, STEALTH MAINTAINED")
        
    def update_size_label(self):
        """Update the size display"""
        size = self.size()
        self.size_label.setText(f"Size: {size.width()}x{size.height()}")
        
    def apply_permanent_stealth(self):
        """Apply stealth that never gets disabled"""
        try:
            hwnd = int(self.winId())
            
            # Apply all stealth techniques
            self.apply_window_display_affinity(hwnd)
            self.apply_extended_style(hwnd)
            self.apply_dwm_attributes(hwnd)
            
            print("✓ PERMANENT STEALTH ACTIVE!")
            print("✓ NOTHING will be visible during screen sharing!")
            self.status_label.setText("TOTAL STEALTH")
            self.status_label.setStyleSheet("color: green; font-weight: bold; font-size: 10px;")
            
        except Exception as e:
            print(f"Stealth application failed: {e}")
            self.status_label.setText("STEALTH FAILED")
            self.status_label.setStyleSheet("color: red; font-weight: bold; font-size: 10px;")
    
    def maintain_stealth(self):
        """Continuously maintain stealth - ULTRA AGGRESSIVE"""
        try:
            hwnd = int(self.winId())
            
            # Aggressively reapply stealth every cycle
            WDA_EXCLUDEFROMCAPTURE = 0x00000011
            ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
            
            # Reapply extended styles every cycle
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x80000
            WS_EX_NOACTIVATE = 0x8000000
            WS_EX_TOOLWINDOW = 0x80
            WS_EX_NOREDIRECTIONBITMAP = 0x00200000
            
            stealth_style = (WS_EX_LAYERED | WS_EX_NOACTIVATE | 
                           WS_EX_TOOLWINDOW | WS_EX_NOREDIRECTIONBITMAP)
            
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stealth_style)
            ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 240, 2)
            
            # Keep window always on top without activation
            HWND_TOPMOST = -1
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            SWP_NOACTIVATE = 0x0010
            SWP_NOREDRAW = 0x0008  # Prevent redraw flashing
            
            ctypes.windll.user32.SetWindowPos(
                hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_NOREDRAW
            )
            
            # DWM cloaking - reapply continuously
            try:
                DWMWA_CLOAKED = 14
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, DWMWA_CLOAKED, ctypes.byref(ctypes.c_int(2)), 4
                )
            except:
                pass
            
        except:
            pass  # Silently maintain stealth
    
    def apply_window_display_affinity(self, hwnd):
        """Exclude from screen capture - PERMANENT"""
        try:
            WDA_EXCLUDEFROMCAPTURE = 0x00000011
            result = ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
            if result:
                print("✓ SetWindowDisplayAffinity PERMANENT")
            else:
                print("✗ SetWindowDisplayAffinity failed")
        except Exception as e:
            print(f"SetWindowDisplayAffinity error: {e}")
    
    def apply_extended_style(self, hwnd):
        """Apply extended window styles - PERMANENT"""
        try:
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x80000
            WS_EX_NOACTIVATE = 0x8000000
            WS_EX_TOOLWINDOW = 0x80
            WS_EX_NOREDIRECTIONBITMAP = 0x00200000
            
            stealth_style = (WS_EX_LAYERED | WS_EX_NOACTIVATE | 
                           WS_EX_TOOLWINDOW | WS_EX_NOREDIRECTIONBITMAP)
            
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stealth_style)
            ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 240, 2)
            print("✓ Extended window styles PERMANENT")
            
        except Exception as e:
            print(f"Extended style error: {e}")
    
    def apply_dwm_attributes(self, hwnd):
        """Apply DWM attributes - PERMANENT"""
        try:
            DWMWA_CLOAKED = 14
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_CLOAKED, ctypes.byref(ctypes.c_int(2)), 4
            )
            
            DWMWA_EXCLUDED_FROM_PEEK = 12
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_EXCLUDED_FROM_PEEK, ctypes.byref(ctypes.c_int(1)), 4
            )
            
            print("✓ DWM attributes PERMANENT")
            
        except Exception as e:
            print(f"DWM attributes error: {e}")
            
    # Mouse events for dragging and resizing - all maintain stealth
    def get_resize_edge(self, pos):
        """Determine which edge/corner is being resized - ENHANCED"""
        rect = self.rect()
        margin = self.resize_margin
        
        left = pos.x() < margin
        right = pos.x() > rect.width() - margin
        top = pos.y() < margin
        bottom = pos.y() > rect.height() - margin
        
        # Check corners first (for better resize control)
        if left and top:
            return "top-left"
        elif right and top:
            return "top-right"
        elif left and bottom:
            return "bottom-left"
        elif right and bottom:
            return "bottom-right"
        # Then check edges
        elif left:
            return "left"
        elif right:
            return "right"
        elif top:
            return "top"
        elif bottom:
            return "bottom"
        else:
            return None
            
    def mousePressEvent(self, event):
        """Handle mouse press - NO FLASHING"""
        # Apply stealth immediately on any interaction
        try:
            hwnd = int(self.winId())
            WDA_EXCLUDEFROMCAPTURE = 0x00000011
            ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        except:
            pass
        
        if event.button() == QtCore.Qt.LeftButton:
            self.resize_edge = self.get_resize_edge(event.pos())
            
            if self.resize_edge:
                self.resizing = True
                self.resize_start_pos = event.globalPos()
                self.resize_start_geometry = self.geometry()
            else:
                self.dragging = True
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                
    def mouseMoveEvent(self, event):
        """Handle mouse move - NO FLASHING"""
        # Continuously apply stealth during movement
        try:
            hwnd = int(self.winId())
            WDA_EXCLUDEFROMCAPTURE = 0x00000011
            ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        except:
            pass
            
        if self.resizing and self.resize_edge:
            self.handle_resize(event.globalPos())
        elif self.dragging and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
        else:
            edge = self.get_resize_edge(event.pos())
            if edge in ["left", "right"]:
                self.setCursor(QtCore.Qt.SizeHorCursor)
            elif edge in ["top", "bottom"]:
                self.setCursor(QtCore.Qt.SizeVerCursor)
            elif edge in ["top-left", "bottom-right"]:
                self.setCursor(QtCore.Qt.SizeFDiagCursor)
            elif edge in ["top-right", "bottom-left"]:
                self.setCursor(QtCore.Qt.SizeBDiagCursor)
            else:
                self.setCursor(QtCore.Qt.ArrowCursor)
                
    def mouseReleaseEvent(self, event):
        """Handle mouse release - stealth maintained"""
        self.resizing = False
        self.dragging = False
        self.resize_edge = None
        self.drag_position = None
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.update_size_label()
        
    def handle_resize(self, global_pos):
        """Handle window resizing with ENHANCED drag control - ZERO FLASH"""
        # Apply stealth during resize
        try:
            hwnd = int(self.winId())
            WDA_EXCLUDEFROMCAPTURE = 0x00000011
            ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        except:
            pass
        
        diff = global_pos - self.resize_start_pos
        new_geo = QtCore.QRect(self.resize_start_geometry)
        
        # Enhanced resize logic for better control
        if "left" in self.resize_edge:
            new_width = max(self.min_size[0], new_geo.width() - diff.x())
            new_geo.setLeft(new_geo.right() - new_width)
        if "right" in self.resize_edge:
            new_geo.setRight(new_geo.right() + diff.x())
        if "top" in self.resize_edge:
            new_height = max(self.min_size[1], new_geo.height() - diff.y())
            new_geo.setTop(new_geo.bottom() - new_height)
        if "bottom" in self.resize_edge:
            new_geo.setBottom(new_geo.bottom() + diff.y())
            
        # Enforce minimum size more precisely
        if new_geo.width() < self.min_size[0]:
            if "left" in self.resize_edge:
                new_geo.setLeft(new_geo.right() - self.min_size[0])
            else:
                new_geo.setRight(new_geo.left() + self.min_size[0])
                
        if new_geo.height() < self.min_size[1]:
            if "top" in self.resize_edge:
                new_geo.setTop(new_geo.bottom() - self.min_size[1])
            else:
                new_geo.setBottom(new_geo.top() + self.min_size[1])
                
        self.setGeometry(new_geo)
        
        # Update size display during resize
        self.update_size_label()

class StealthDialog(QtWidgets.QDialog):
    """Dialog that's also invisible to screen capture"""
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Stealth Options")
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setModal(True)
        
        # Apply stealth to dialog too
        QtCore.QTimer.singleShot(50, self.apply_dialog_stealth)
        
        layout = QtWidgets.QVBoxLayout()
        
        layout.addWidget(QtWidgets.QLabel("STEALTH OPTIONS (Invisible to others)"))
        
        # Position buttons
        pos_layout = QtWidgets.QHBoxLayout()
        pos_layout.addWidget(QtWidgets.QPushButton("Top-Left"))
        pos_layout.addWidget(QtWidgets.QPushButton("Top-Right"))
        pos_layout.addWidget(QtWidgets.QPushButton("Center"))
        layout.addLayout(pos_layout)
        
        # Size buttons
        size_layout = QtWidgets.QHBoxLayout()
        size_layout.addWidget(QtWidgets.QPushButton("Small"))
        size_layout.addWidget(QtWidgets.QPushButton("Medium"))
        size_layout.addWidget(QtWidgets.QPushButton("Large"))
        layout.addLayout(size_layout)
        
        # Close button
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        
    def apply_dialog_stealth(self):
        """Make dialog also invisible to screen capture"""
        try:
            hwnd = int(self.winId())
            WDA_EXCLUDEFROMCAPTURE = 0x00000011
            ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
            print("✓ Dialog is also STEALTH!")
        except:
            pass

if __name__ == "__main__":
    print("TOTAL STEALTH OVERLAY - ZERO FLASH VERSION")
    print("=" * 60)
    print("🔥 ABSOLUTE ZERO FLASH - NOTHING EVER VISIBLE")
    print("• NO visible dialogs - keyboard shortcuts only")
    print("• Enhanced drag resizing from edges/corners")
    print("• Click ⚙ for keyboard shortcut list (no visual dialog)")
    print()
    print("🎮 KEYBOARD SHORTCUTS:")
    print("• 1-5: Sizes (1=Tiny, 2=Small, 3=Medium, 4=Large, 5=Huge)")
    print("• R/B/G/P: Colors (Red/Blue/Green/Purple)")
    print("• Q/W/E/A/D: Positions (Q=Top-Left, W=Top-Right, E=Center, A=Bottom-Left, D=Bottom-Right)")
    print()
    print("🖱️ MOUSE CONTROLS:")
    print("• Drag center: Move window")
    print("• Drag edges/corners: Resize window")
    print("• Quick buttons: R/B/G for colors, S/L for sizes")
    print()
    
    app = QtWidgets.QApplication(sys.argv)
    window = TotalStealthOverlay()
    window.show()
    
    print("🎯 ZERO-FLASH STEALTH OVERLAY RUNNING!")
    print("🎯 Your friend will NEVER see anything, not even for 1 millisecond!")
    
    sys.exit(app.exec_())
