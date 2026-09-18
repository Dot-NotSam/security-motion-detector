import tkinter as tk
from gui.app import SecurityDashboard


def main():
    root = tk.Tk()
    app = SecurityDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
