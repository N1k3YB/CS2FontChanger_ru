import sys
import os
import shutil
import fontTools
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QLabel, QPushButton, QFileDialog, QMessageBox, 
                            QProgressBar, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import (QPainter, QColor, QPen, QLinearGradient, QPalette, QFont,
                        QPainterPath, QBrush)

# Шаблоны конфигурации
GLOBAL_CONF_TEMPLATE = '''<?xml version='1.0'?>
<!DOCTYPE fontconfig SYSTEM 'fonts.dtd'>
<fontconfig>

	<!-- ##Style: common -->

	<!-- Global Replacements - Active if set to true above -->
	<!-- Add your own replacements here -->
	<!-- Clone "match" blocks below for each replacement -->
	<match target="font">
		<test name="family">
			<string>Stratum2</string>
		</test>
		<edit name="family" mode="assign">
			<string>FONTNAME</string>
		</edit>
	</match>
	<match target="pattern">
		<test name="family">
			<string>Stratum2</string>
		</test>
		<edit name="family" mode="prepend" binding="strong">
			<string>FONTNAME</string>
		</edit>
	</match>

	<match target="font">
		<test name="family">
			<string>Stratum2 Bold</string>
		</test>
		<edit name="family" mode="assign">
			<string>FONTNAME</string>
		</edit>
	</match>
	<match target="pattern">
		<test name="family">
			<string>Stratum2 Bold</string>
		</test>
		<edit name="family" mode="prepend" binding="strong">
			<string>FONTNAME</string>
		</edit>
	</match>

	<match target="font">
		<test name="family">
			<string>Arial</string>
		</test>
		<edit name="family" mode="assign">
			<string>FONTNAME</string>
		</edit>
	</match>
	<match target="pattern">
		<test name="family">
			<string>Arial</string>
		</test>
		<edit name="family" mode="prepend" binding="strong">
			<string>FONTNAME</string>
		</edit>
	</match>

	<match target="font">
		<test name="family">
			<string>Times New Roman</string>
		</test>
		<edit name="family" mode="assign">
			<string>FONTNAME</string>
		</edit>
	</match>
	<match target="pattern">
		<test name="family">
			<string>Times New Roman</string>
		</test>
		<edit name="family" mode="prepend" binding="strong">
			<string>FONTNAME</string>
		</edit>
	</match>

	<match target="font">
		<test name="family">
			<string>Courier New</string>
		</test>
		<edit name="family" mode="assign">
			<string>FONTNAME</string>
		</edit>
	</match>
	<match target="pattern">
		<test name="family">
			<string>Courier New</string>
		</test>
		<edit name="family" mode="prepend" binding="strong">
			<string>FONTNAME</string>
		</edit>
	</match>

	<match target="font">
		<test name="family">
			<string>notosans</string>
		</test>
		<edit name="family" mode="assign">
			<string>FONTNAME</string>
		</edit>
	</match>
	<match target="pattern">
		<test name="family">
			<string>notosans</string>
		</test>
		<edit name="family" mode="prepend" binding="strong">
			<string>FONTNAME</string>
		</edit>
	</match>

	<match target="font">
		<test name="family">
			<string>notoserif</string>
		</test>
		<edit name="family" mode="assign">
			<string>FONTNAME</string>
		</edit>
	</match>
	<match target="pattern">
		<test name="family">
			<string>notoserif</string>
		</test>
		<edit name="family" mode="prepend" binding="strong">
			<string>FONTNAME</string>
		</edit>
	</match>

	<match target="font">
		<test name="family">
			<string>notomono-regular</string>
		</test>
		<edit name="family" mode="assign">
			<string>FONTNAME</string>
		</edit>
	</match>
	<match target="pattern">
		<test name="family">
			<string>notomono-regular</string>
		</test>
		<edit name="family" mode="prepend" binding="strong">
			<string>FONTNAME</string>
		</edit>
	</match>

	<match target="font">
		<test name="family">
			<string>noto</string>
		</test>
		<edit name="family" mode="assign">
			<string>FONTNAME</string>
		</edit>
	</match>
	<match target="pattern">
		<test name="family">
			<string>noto</string>
		</test>
		<edit name="family" mode="prepend" binding="strong">
			<string>FONTNAME</string>
		</edit>
	</match>
	
</fontconfig>
'''

FONTS_CONF_TEMPLATE = '''<?xml version='1.0'?>
<!DOCTYPE fontconfig SYSTEM 'fonts.dtd'>
<fontconfig>

	<!-- Choose an OS Rendering Style.  This will determine B/W, grayscale,
	     or subpixel antialising and slight, full or no hinting and replacements (if set in next option) -->
	<!-- Style should also be set in the infinality-settings.sh file, ususally in /etc/profile.d/ -->

	<!-- Choose one of these options:
		Infinality      - subpixel AA, minimal replacements/tweaks, sans=Arial
		Windows 7       - subpixel AA, sans=Arial
		Windows XP      - subpixel AA, sans=Arial
		Windows 98      - B/W full hinting on TT fonts, grayscale AA for others, sans=Arial
		OSX             - Slight hinting, subpixel AA, sans=Helvetica Neue
		OSX2            - No hinting, subpixel AA, sans=Helvetica Neue
		Linux           - subpixel AA, sans=DejaVu Sans

	=== Recommended Setup ===
	Run ./infctl.sh script located in the current directory to set the style.
	
	# ./infctl.sh setstyle
	
	=== Manual Setup ===
	See the infinality/styles.conf.avail/ directory for all options.  To enable 
	a different style, remove the symlink "conf.d" and link to another style:
	
	# rm conf.d
	# ln -s styles.conf.avail/win7 conf.d
	-->

	<dir prefix="default">../../csgo/panorama/fonts</dir>
	<dir>WINDOWSFONTDIR</dir>
	<dir>~/.fonts</dir>
	<dir>/usr/share/fonts</dir>
	<dir>/usr/local/share/fonts</dir>
	<dir prefix="xdg">fonts</dir>

	<!-- A fontpattern is a font file name, not a font name.  Be aware of filenames across all platforms! -->
	<fontpattern>Arial</fontpattern>
	<fontpattern>.uifont</fontpattern>
	<fontpattern>notosans</fontpattern>
	<fontpattern>notoserif</fontpattern>
	<fontpattern>notomono-regular</fontpattern>
	<fontpattern>FONTNAME</fontpattern>
	<fontpattern>.ttf</fontpattern>
	<fontpattern>FONTFILENAME</fontpattern>
	
	<cachedir>WINDOWSTEMPDIR_FONTCONFIG_CACHE</cachedir>
	<cachedir>~/.fontconfig</cachedir>

	<!-- Uncomment this to reject all bitmap fonts -->
	<!-- Make sure to run this as root if having problems:  fc-cache -f -->
	<!--
	<selectfont>
		<rejectfont>
			<pattern>
				<patelt name="scalable" >
					<bool>false</bool>
				</patelt>
			</pattern>
		</rejectfont>
	</selectfont>
	-->

	<!-- THESE RULES RELATE TO THE OLD MONODIGIT FONTS, TO BE REMOVED ONCE ALL REFERENCES TO THEM HAVE GONE. -->
	<!-- The Stratum2 Monodigit fonts just supply the monospaced digits -->
	<!-- All other characters should come from ordinary Stratum2 -->
	<match>
		<test name="family">
			<string>Stratum2 Bold Monodigit</string>
		</test>
		<edit name="family" mode="append" binding="strong">
			<string>Stratum2</string>
		</edit>
		<edit name="style" mode="assign" binding="strong">
			<string>Bold</string>
		</edit>
	</match>

	<match>
		<test name="family">
			<string>Stratum2 Regular Monodigit</string>
		</test>
		<edit name="family" mode="append" binding="strong">
			<string>Stratum2</string>
		</edit>
		<edit name="weight" mode="assign" binding="strong">
			<string>Regular</string>
		</edit>
	</match>

	<!-- Stratum2 only contains a subset of the Vietnamese alphabet. -->
	<!-- So when language is set to Vietnamese, replace Stratum with Noto. -->
	<!-- Exceptions are Mono and TF fonts. -->
	<!-- Ensure we pick an Italic/Bold version of Noto where appropriate. -->
	<!-- Adjust size due to the Ascent value for Noto being significantly larger than Stratum. -->
	<!-- Adjust size even smaller for condensed fonts.-->
	<match>
		<test name="lang">
			<string>vi-vn</string>
		</test>
		<test name="family" compare="contains">
			<string>Stratum2</string>
		</test>
		<test qual="all" name="family" compare="not_contains">
			<string>TF</string>
		</test>
		<test qual="all" name="family" compare="not_contains">
			<string>Mono</string>
		</test>
		<test qual="all" name="family" compare="not_contains">
			<string>ForceStratum2</string>
		</test>
		<edit name="weight" mode="assign">
			<if>
				<contains>
					<name>family</name>
					<string>Stratum2 Black</string>
				</contains>
				<int>210</int>
				<name>weight</name>
			</if>
		</edit>
		<edit name="slant" mode="assign">
			<if>
				<contains>
					<name>family</name>
					<string>Italic</string>
				</contains>
				<int>100</int>
				<name>slant</name>
			</if>
		</edit>
		<edit name="pixelsize" mode="assign">
			<if>
				<or>
					<contains>
						<name>family</name>
						<string>Condensed</string>
					</contains>
					<less_eq>
						<name>width</name>
						<int>75</int>
					</less_eq>
				</or>
				<times>
					<name>pixelsize</name>
					<double>0.7</double>
				</times>
				<times>
					<name>pixelsize</name>
					<double>0.9</double>
				</times>
			</if>
		</edit>
		<edit name="family" mode="assign" binding="same">
			<string>notosans</string>
		</edit>
	</match>

	<!-- More Vietnamese... -->
	<!-- In some cases (hud health, ammo, money) we want to force Stratum to be used. -->
	<match>
		<test name="lang">
			<string>vi-vn</string>
		</test>
		<test name="family">
			<string>ForceStratum2</string>
		</test>
		<edit name="family" mode="assign" binding="same">
			<string>Stratum2</string>
		</edit>
	</match>

	<!-- Fallback font sizes. -->
	<!-- If we request Stratum, but end up with Arial, reduce the pixelsize because Arial glyphs are larger than Stratum. -->
	<match target="font">
		<test name="family" target="pattern" compare="contains">
			<string>Stratum2</string>
		</test>
		<test name="family" target="font" compare="contains">
			<string>Arial</string>
		</test>
		<edit name="pixelsize" mode="assign">
			<times>
				<name>pixelsize</name>
				<double>0.9</double>
			</times>
		</edit>
	</match>

	<!-- If we request Stratum, but end up with Noto, reduce the pixelsize. -->
	<!-- This fixes alignment issues due to the Ascent value for Noto being significantly larger than Stratum. -->
	<match target="font">
		<test name="family" target="pattern" compare="contains">
			<string>Stratum2</string>
		</test>
		<test name="family" target="font" compare="contains">
			<string>Noto</string>
		</test>
		<edit name="pixelsize" mode="assign">
			<times>
				<name>pixelsize</name>
				<double>0.9</double>
			</times>
		</edit>
	</match>

 	<!-- Stratum contains a set of arrow symbols in place of certain greek/mathematical characters - presumably for some historical reason, possibly used by VGUI somewhere?. -->
 	<!-- For panorama these Stratum characters should be ignored and picked up from a fallback font instead. -->
	<!-- Update for new source2 versions of Stratum, exclude all four of the greek characters which are included in the new Stratum fonts (sometimes as arrows, sometimes not). Best to fallback in all cases to Arial. -->
	<match target="scan">
		<test name="family">
			<string>Stratum2</string> <!-- This matches all the source2 Stratum fonts except the mono versions -->
		</test>
		<edit name="charset" mode="assign">
			<minus>
				<name>charset</name>
				<charset>
					<int>0x0394</int> <!-- greek delta -->
					<int>0x03A9</int> <!-- greek omega -->
					<int>0x03BC</int> <!-- greek mu -->
					<int>0x03C0</int> <!-- greek pi -->
					<int>0x2202</int> <!-- partial diff -->
					<int>0x2206</int> <!-- delta -->
					<int>0x220F</int> <!-- product -->
					<int>0x2211</int> <!-- sum -->
					<int>0x221A</int> <!-- square root -->
					<int>0x221E</int> <!-- infinity -->
					<int>0x222B</int> <!-- integral -->
					<int>0x2248</int> <!-- approxequal -->
					<int>0x2260</int> <!-- notequal -->
					<int>0x2264</int> <!-- lessequal -->
					<int>0x2265</int> <!-- greaterequal -->
					<int>0x25CA</int> <!-- lozenge -->
				</charset>
			</minus>
		</edit>
	</match>

	<!-- Ban Type-1 fonts because they render poorly --> 
	<!-- Comment this out to allow all Type 1 fonts -->
	<selectfont> 
		<rejectfont> 
			<pattern> 
				<patelt name="fontformat" > 
					<string>Type 1</string> 
				</patelt> 
			</pattern> 
		</rejectfont> 
	</selectfont> 

	<!-- Globally use embedded bitmaps in fonts like Calibri? -->
	<match target="font" >
		<edit name="embeddedbitmap" mode="assign">
			<bool>false</bool>
		</edit>
	</match>

	<!-- Substitute truetype fonts in place of bitmap ones? -->
	<match target="pattern" >
		<edit name="prefer_outline" mode="assign">
			<bool>true</bool>
		</edit>
	</match>

	<!-- Do font substitutions for the set style? -->
	<!-- NOTE: Custom substitutions in 42-repl-global.conf will still be done -->
	<!-- NOTE: Corrective substitutions will still be done -->
	<match target="pattern" >
		<edit name="do_substitutions" mode="assign">
			<bool>true</bool>
		</edit>
	</match>

	<!-- Make (some) monospace/coding TTF fonts render as bitmaps? -->
	<!-- courier new, andale mono, monaco, etc. -->
	<match target="pattern" >
		<edit name="bitmap_monospace" mode="assign">
			<bool>false</bool>
		</edit>
	</match>

	<!-- Force autohint always -->
	<!-- Useful for debugging and for free software purists -->
	<match target="font">
		<edit name="force_autohint" mode="assign">
			<bool>false</bool>
		</edit>
	</match>

	<!-- Set DPI.  dpi should be set in ~/.Xresources to 96 -->
	<!-- Setting to 72 here makes the px to pt conversions work better (Chrome) -->
	<!-- Some may need to set this to 96 though -->
	<match target="pattern">
		<edit name="dpi" mode="assign">
			<double>96</double>
		</edit>
	</match>
	
	<!-- Use Qt subpixel positioning on autohinted fonts? -->
	<!-- This only applies to Qt and autohinted fonts. Qt determines subpixel positioning based on hintslight vs. hintfull, -->
	<!--   however infinality patches force slight hinting inside freetype, so this essentially just fakes out Qt. -->
	<!-- Should only be set to true if you are not doing any stem alignment or fitting in environment variables -->
	<match target="pattern" >
		<edit name="qt_use_subpixel_positioning" mode="assign">
			<bool>false</bool>
		</edit>
	</match>

	<!-- Run infctl.sh or change the symlink in current directory instead of modifying this -->
	<include>../../../core/panorama/fonts/conf.d</include>
	
	<!-- Custom fonts -->
	<!-- Edit every occurency with your font name (NOT the font file name) -->
	
	<match>
		<test name="family">
			<string>Stratum2</string>
		</test>
		<edit name="family" mode="append" binding="strong">
			<string>FONTNAME</string>
		</edit>
		<edit name="pixelsize" mode="assign">
			<times>
				<name>pixelsize</name>
				<double>1</double>
			</times>
		</edit>
	</match>
	
	<match>
		<test name="family">
			<string>Stratum2 Bold</string>
		</test>
		<edit name="family" mode="append" binding="strong">
			<string>FONTNAME</string>
		</edit>
		<edit name="pixelsize" mode="assign">
			<times>
				<name>pixelsize</name>
				<double>1</double>
			</times>
		</edit>
	</match>
	
	<match>
		<test name="family">
			<string>Arial</string>
		</test>
		<edit name="family" mode="append" binding="strong">
			<string>FONTNAME</string>
		</edit>
		<edit name="pixelsize" mode="assign">
			<times>
				<name>pixelsize</name>
				<double>1</double>
			</times>
		</edit>
	</match>
	
	<match>
		<test name="family">
			<string>Times New Roman</string>
		</test>
		<edit name="family" mode="append" binding="strong">
			<string>FONTNAME</string>
		</edit>
		<edit name="pixelsize" mode="assign">
			<times>
				<name>pixelsize</name>
				<double>1</double>
			</times>
		</edit>
	</match>
	
	<match>
		<test name="family">
			<string>Courier New</string>
		</test>
		<edit name="family" mode="append" binding="strong">
			<string>FONTNAME</string>
		</edit>
		<edit name="pixelsize" mode="assign">
			<times>
				<name>pixelsize</name>
				<double>1</double>
			</times>
		</edit>
	</match>

	<!-- And here's the thing... -->
	<!-- CSGO devs decided to fallback to "notosans" on characters not supplied with "Stratum2" - the font we're trying to replace -->
	<!-- "notosans" or "Noto" is used i.e. on Vietnamese characters - but also on some labels that should be using "Stratum2" or even Arial -->
	<!-- I can't do much about it right now. If you're Vietnamese or something, just delete this <match> closure. -->
	<!-- Some labels (i.e. icon tooltips in menu) won't be using your custom font -->
	<match>
		<test name="family">
			<string>notosans</string>
		</test>
		<edit name="family" mode="append" binding="strong">
			<string>FONTNAME</string>
		</edit>
		<edit name="pixelsize" mode="assign">
			<times>
				<name>pixelsize</name>
				<double>1</double>
			</times>
		</edit>
	</match>
	
	<match>
		<test name="family">
			<string>notoserif</string>
		</test>
		<edit name="family" mode="append" binding="strong">
			<string>FONTNAME</string>
		</edit>
		<edit name="pixelsize" mode="assign">
			<times>
				<name>pixelsize</name>
				<double>1</double>
			</times>
		</edit>
	</match>
	
	<match>
		<test name="family">
			<string>notomono-regular</string>
		</test>
		<edit name="family" mode="append" binding="strong">
			<string>FONTNAME</string>
		</edit>
		<edit name="pixelsize" mode="assign">
			<times>
				<name>pixelsize</name>
				<double>1</double>
			</times>
		</edit>
	</match>

	<match>
		<test name="family">
			<string>noto</string>
		</test>
		<edit name="family" mode="append" binding="strong">
			<string>FONTNAME</string>
		</edit>
		<edit name="pixelsize" mode="assign">
			<times>
				<name>pixelsize</name>
				<double>1</double>
			</times>
		</edit>
	</match>

</fontconfig>
'''

class CustomMessageBox(QMainWindow):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 200)
        
        # Центральный виджет с диагональным фоном
        central_widget = DiagonalStripe()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Контент
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Сообщение
        msg_label = QLabel(message)
        msg_label.setFont(QFont("Segoe UI", 12))
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("color: #000000;")
        content_layout.addWidget(msg_label)
        
        # Кнопка OK
        ok_btn = StyledButton("ПОН")
        ok_btn.setStyleSheet("width: 100px; height: 30px; font-size: 24px; background-color: #FF6B00")
        ok_btn.clicked.connect(self.close)
        content_layout.addWidget(ok_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(content)
        

class DiagonalStripe(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QColor("#FFFFFF"))

        width = self.width()
        height = self.height()
        stripe_width = width * 0.35

        path = QPainterPath()
        path.moveTo(width - stripe_width, 0)
        path.lineTo(width, 0)
        path.lineTo(width, height)
        path.lineTo(width - stripe_width - height * 0.4, height)
        path.closeSubpath()

        gradient = QLinearGradient(width - stripe_width, 0, width, 0)
        gradient.setColorAt(0, QColor("#FF8C00"))
        gradient.setColorAt(1, QColor("#FF6B00"))
        
        shadow_path = QPainterPath()
        shadow_offset = 10
        shadow_path.moveTo(width - stripe_width + shadow_offset, 0)
        shadow_path.lineTo(width + shadow_offset, 0)
        shadow_path.lineTo(width + shadow_offset, height)
        shadow_path.lineTo(width - stripe_width + shadow_offset - height * 0.4, height)
        shadow_path.closeSubpath()
        
        painter.setOpacity(0.2)
        painter.fillPath(shadow_path, QColor("#000000"))
        
        painter.setOpacity(1.0)
        painter.fillPath(path, QBrush(gradient))

class StyledButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 10))
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: #FF8C00;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6B00;
            }
            QPushButton:pressed {
                background-color: #FF5500;
                padding: 9px 16px 7px 16px;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
            }
        """)

class SteamSearchThread(QThread):
    finished = pyqtSignal(str)

    def run(self):
        possible_paths = [
            "C:\\Program Files (x86)\\Steam\\steamapps\\common",
            "C:\\Program Files\\Steam\\steamapps\\common"
        ]
        
        for drive in range(ord('C'), ord('Z') + 1):
            drive_letter = chr(drive)
            possible_paths.append(f"{drive_letter}:\\SteamLibrary\\steamapps\\common")
            
        found_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csgo_path = os.path.join(path, "Counter-Strike Global Offensive")
                if os.path.exists(csgo_path):
                    found_path = csgo_path
                    break
                    
        self.finished.emit(found_path if found_path else "")

class LoadingScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel("CS2 Font Changer")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #000000;")
        layout.addWidget(title)
        
        # Loading text
        self.loading_label = QLabel("Поиск CS2...")
        self.loading_label.setFont(QFont("Segoe UI", 12))
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet("color: #000000;")
        layout.addWidget(self.loading_label)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(0)
        self.progress.setFixedWidth(300)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #FF8C00;
                border-radius: 5px;
                text-align: center;
                height: 25px;
                color: #000000;
            }
            QProgressBar::chunk {
                background-color: #FF8C00;
            }
        """)
        layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_font = None
        self.steam_path = None
        self.setWindowTitle("CS2 Font Changer")
        self.setFixedSize(800, 600)
        self.setup_ui()
        self.start_search()

    def show_message(self, title, message):
        msg_box = CustomMessageBox(title, message, self)
        msg_box.setWindowModality(Qt.WindowModality.ApplicationModal)
        msg_box.show()
        
    def setup_ui(self):
        self.central_widget = DiagonalStripe()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        
        content_widget = QWidget()
        
        shadow = QGraphicsDropShadowEffect(content_widget)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 80))
        content_widget.setGraphicsEffect(shadow)
        
        content_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0);
                border-radius: 15px;
            }
        """)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(content_widget)

        # Loading screen
        self.loading_screen = LoadingScreen()
        content_layout.addWidget(self.loading_screen)
        
        # Main interface 
        self.main_interface = QWidget()
        self.main_interface.hide()
        main_layout = QVBoxLayout(self.main_interface)
        content_layout.addWidget(self.main_interface)
        
        # Title
        title = QLabel("CS2")
        title.setFont(QFont("Segoe UI", 90, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #000000; padding-bottom: 0px;")
        under_title = QLabel("Font Changer")
        under_title.setFont(QFont("Segoe UI", 30, QFont.Weight.Bold))
        under_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        under_title.setStyleSheet("color: #000000; padding-top: 0px;")
        main_layout.addWidget(title)
        main_layout.addWidget(under_title)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setFont(QFont("Segoe UI", 11))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: #000000;")
        main_layout.addWidget(self.status_label)
        
        # Buttons
        self.select_path_btn = StyledButton("Указать путь к CS2")
        self.select_path_btn.clicked.connect(self.select_steam_path)
        main_layout.addWidget(self.select_path_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.font_btn = StyledButton("Выбрать .ttf/.otf файл")
        self.font_btn.clicked.connect(self.select_font)
        self.font_btn.setEnabled(False)
        main_layout.addWidget(self.font_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.font_label = QLabel("Шрифт не выбран")
        self.font_label.setFont(QFont("Segoe UI", 11))
        self.font_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.font_label.setStyleSheet("color: #000000;")
        
        
        self.apply_btn = StyledButton("Применить шрифт")
        self.apply_btn.clicked.connect(self.apply_font)
        self.apply_btn.setEnabled(False)
        main_layout.addWidget(self.apply_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.font_label)

    def start_search(self):
        self.search_thread = SteamSearchThread()
        self.search_thread.finished.connect(self.on_search_complete)
        self.search_thread.start()

    def on_search_complete(self, path):
        self.loading_screen.hide()
        self.main_interface.show()
        
        if path:
            self.steam_path = path
            self.status_label.setText(f"CS2 найден: {path}")
            self.select_path_btn.hide()
            self.font_btn.setEnabled(True)
        else:
            self.status_label.setText("CS2 не найден")

    def select_steam_path(self):
        path = QFileDialog.getExistingDirectory(self, "Выберите папку с CS2")
        if path:
            if self.validate_csgo_path(path):
                self.steam_path = path
                self.status_label.setText(f"CS2 найден: {path}")
                self.select_path_btn.hide()
                self.font_btn.setEnabled(True)
            else:
                self.show_message("Ошибка", "В данной папке нет CS2")

    def validate_csgo_path(self, path):
        required_paths = [
            os.path.join(path, "game", "csgo", "panorama", "fonts"),
            os.path.join(path, "game", "core", "panorama", "fonts", "conf.d")
        ]
        return all(os.path.exists(p) for p in required_paths)

    def select_font(self):
        font_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите шрифт", "", "Font files (*.ttf *.otf)")
        if font_path:
            self.selected_font = font_path
            self.font_label.setText(f"Выбран шрифт: {os.path.basename(font_path)}")
            self.apply_btn.setEnabled(True)

    def apply_font(self):
        try:
            font_file = os.path.basename(self.selected_font)
            font_name = self.get_font_name(self.selected_font)
            font_file_without_ext = os.path.splitext(font_file)[0]
            
            panorama_path = os.path.join(
                self.steam_path, "game", "csgo", "panorama",
                "fonts", "fonts.conf"
            )
            core_path = os.path.join(
                self.steam_path, "game", "core", "panorama",
                "fonts", "conf.d", "42-repl-global.conf"
            )
            
            self.create_config_file(panorama_path, FONTS_CONF_TEMPLATE, font_name, font_file_without_ext)
            self.create_config_file(core_path, GLOBAL_CONF_TEMPLATE, font_name, font_file_without_ext)
            
            fonts_dir = os.path.join(self.steam_path, "game", "csgo",
                                "panorama", "fonts")
            target_font_path = os.path.join(fonts_dir, font_file)
            
            if os.path.exists(target_font_path):
                try:
                    os.remove(target_font_path)
                except Exception as e:
                    raise Exception(f"Не удалось удалить существующий файл шрифта: {str(e)}")
                    
            shutil.copy2(self.selected_font, fonts_dir)
            
            self.show_message("Успех", "Шрифт успешно изменен!")
            
        except Exception as e:
            self.show_message("Ошибка", f"Вы не можете использовать шрифт из этой папки\nПопробуйте переместить его в другую папку")
            print(e)


    def create_config_file(self, target_path, template, font_name, font_file):
        if os.path.exists(target_path):
            backup_path = target_path + ".backup"
            try:
                shutil.copy2(target_path, backup_path)
            except Exception as e:
                print(f"Не удалось создать резервную копию: {e}")
        
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        try:
            config_content = template\
                .replace('FONTNAME', font_name)\
                .replace('FONTFILENAME', font_file)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(config_content)
        except Exception as e:
            raise Exception(f"Ошибка при создании конфигурационного файла: {e}")
        
    def get_font_name(self, font_path):
        try:
            from fontTools.ttLib import TTFont
            font = TTFont(font_path)
            
            for record in font['name'].names:
                if record.nameID == 4:  
                    if record.isUnicode():
                        return record.string.decode('utf-16-be')
                    else:
                        return record.string.decode('latin-1')
                        
            return os.path.splitext(os.path.basename(font_path))[0]
            
        except Exception as e:
            print(f"Warning: Could not extract font name: {e}")
            return os.path.splitext(os.path.basename(font_path))[0]

def main():
    app = QApplication(sys.argv)
    
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
