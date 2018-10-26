# From https://stackoverflow.com/questions/14004835/nodelay-causes-python-curses-program-to-exit

import curses, time

def main(sc):
    sc.nodelay(1)

    for angry in range(20):
        sc.addstr(angry, 1, "hi")
        sc.refresh()

        if sc.getch() == ord('q'):
            break

        time.sleep(1)

if __name__=='__main__':
    curses.wrapper(main)