"""PySide6 desktop shell. Loads the host, wires the main window."""
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from vectorforge.core.host import VectorForgeHost
from vectorforge.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    host = VectorForgeHost.autoload()
    window = MainWindow(host=host)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())