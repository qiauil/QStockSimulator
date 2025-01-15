from qfluentwidgets import HeaderCardWidget


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widget=HeaderCardWidget(title="Header Card Widget")
    widget.show()
    sys.exit(app.exec())