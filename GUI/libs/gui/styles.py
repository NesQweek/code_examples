btn_style_unactive = """QPushButton {
	background-color: rgb(59,59,59);
	color: rgb(180,180,180);
	border-style: solid;
	padding: 25px 3px 25px 3px;
}
QPushButton::hover {
	background-color: rgb(69,69,69);
	color: rgb(200,200,200);
	padding: 25px 3px 25px 3px;
}"""


btn_style_active = """QPushButton {
	background-color: rgb(59,59,59);
	color: rgb(180,180,180);
	border-style: solid;
	padding: 25px 3px 15px 3px;
	border-bottom: 10px solid rgba(255,255,255,30)}"""


combobox = """QComboBox {
    border-radius: 3px;
    border: 2px solid gray;
    color: white }

QComboBox:!editable, QComboBox::drop-down:editable {
background-color: qlineargradient(spread:reflect, x1:0, y1:0.523, x2:1, y2:0.528, stop:0 rgba(150, 150, 150, 20), stop:0.545455 rgba(200, 200, 200, 60), stop:1 rgba(150, 150, 150, 60))}

QComboBox QAbstractItemView {
color: rgb(210, 210, 210);
background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(230, 230, 223, 40), stop:1 rgba(200, 200, 200, 40));
selection-background-color:   qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(200, 200, 200, 40));
selection-color: rgb(240, 240, 249)}

QComboBox::drop-down {
subcontrol-origin: padding;
subcontrol-position: top right;
width: 15px;
border-left-width: 1px;
border-left-color: darkgray;
border-left-style: solid; /* just a single line */
border-top-right-radius: 3px; /* same radius as the QComboBox */
border-bottom-right-radius: 3px}

QComboBox::down-arrow {
image: url(:/buttons/icons/arrow_down.png);
width: 10}

QComboBox::down-arrow:on { /* shift the arrow when popup is open */
top: 1px;
left: 1px}"""

