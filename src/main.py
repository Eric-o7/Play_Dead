from graphics import root

def main():
    root.mainloop()

def reset_game():
    import os, sys
    os.execl(sys.executable, *([sys.executable]+sys.argv))    

if __name__ == "__main__":        
    main()
    
    
#todo
# make sure the prompt "Which enemy would you like to target accurately displays all enemies"
# fix bug where the last enemy available attacks twice and prompts player twice