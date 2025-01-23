from graphics import root

def main():
    root.mainloop()

def reset_game():
    import os, sys
    os.execl(sys.executable, *([sys.executable]+sys.argv))    

if __name__ == "__main__":        
    main()
    