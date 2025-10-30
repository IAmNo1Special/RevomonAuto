import logging
import subprocess
import sys
import time
from datetime import datetime

from revomonauto.controllers.revo_controller import RevoAppController

# Set up logging
log_file = f"controller_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)

# Suppress PIL and adb_shell debug logs
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("adb_shell").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def show_overlay(message: str, duration: float = 3.0, font_size: int = 48) -> None:
    """Display an always-on-top overlay with big white text for a short duration.

    Uses a separate Python process to avoid Tkinter threading issues.

    Args:
        message: Text to display.
        duration: Seconds to show the overlay.
        font_size: Font size for the text.
    """
    try:
        script = (
            "import tkinter as tk\n"
            "from tkinter import font as tkfont\n"
            "msg = " + repr(message) + "\n"
            "duration = " + str(float(duration)) + "\n"
            "font_size = " + str(int(font_size)) + "\n"
            "root = tk.Tk()\n"
            "root.overrideredirect(True)\n"
            "root.attributes('-topmost', True)\n"
            "\n"
            "try:\n"
            "    root.attributes('-alpha', 0.9)\n"
            "except Exception:\n"
            "    pass\n"
            "\n"
            "root.configure(bg='black')\n"
            "f = tkfont.Font(family='Segoe UI', size=font_size, weight='bold')\n"
            "label = tk.Label(root, text=msg, font=f, fg='white', bg='black')\n"
            "label.pack(padx=40, pady=20)\n"
            "root.update_idletasks()\n"
            "w = root.winfo_width(); h = root.winfo_height()\n"
            "sw = root.winfo_screenwidth(); sh = root.winfo_screenheight()\n"
            "x = int(sw/2 - w/2); y = int(sh/4 - h/2)\n"
            "root.geometry(f'+{x}+{y}')\n"
            "root.after(int(duration*1000), root.destroy)\n"
            "root.mainloop()\n"
        )
        subprocess.Popen([sys.executable, "-c", script])
    except Exception:
        # Fail silently if GUI is unavailable
        pass


if __name__ == "__main__":
    try:

        controller = RevoAppController()

        show_overlay("Opening Revomon app...")
        controller.open_revomon_app()

        show_overlay("Starting game...")
        controller.start_game()

        show_overlay("Logging in...")
        controller.log_in()

        show_overlay("Opening main menu...")
        controller.open_main_menu()

        time.sleep(1.0)

        show_overlay("Closing main menu...")
        controller.close_main_menu()

        show_overlay("Entering PVP queue...")
        controller.enter_pvp_queue()

        time.sleep(1.0)

        show_overlay("Exiting PVP queue...")
        controller.exit_pvp_queue()

        show_overlay("Opening wardrobe...")
        controller.open_wardrobe()

        time.sleep(1.0)

        show_overlay("Closing wardrobe")
        controller.close_wardrobe()

        show_overlay("Opening menu bag...")
        controller.open_menu_bag()

        time.sleep(1.0)

        show_overlay("Closing menu bag...")
        controller.close_menu_bag()

        show_overlay("Opening friends list...")
        controller.open_friends_list()

        time.sleep(1.0)

        show_overlay("Closing friends list...")
        controller.close_friends_list()

        show_overlay("Opening settings...")
        controller.open_settings()

        time.sleep(1.0)

        show_overlay("Closing settings...")
        controller.close_settings()

        show_overlay("Opening revodex...")
        controller.open_revodex()

        time.sleep(1.0)

        show_overlay("Closing revodex...")
        controller.close_revodex()

        show_overlay("Opening market...")
        controller.open_market()

        time.sleep(1.0)

        show_overlay("Closing market...")
        controller.close_market()

        show_overlay("Opening discussion...")
        controller.open_discussion()

        time.sleep(1.0)

        show_overlay("Closing discussion...")
        controller.close_discussion()

        show_overlay("Opening clan...")
        controller.open_clan()

        time.sleep(1.0)

        show_overlay("Closing clan...")
        controller.close_clan()

        show_overlay("Closing main menu...")
        controller.close_main_menu()

        show_overlay("Opening TV...")
        controller.open_tv()

        show_overlay("Switching TV slots...")
        controller.select_tv_slot(1)

        time.sleep(1.0)

        controller.select_tv_slot(2)

        time.sleep(1.0)

        controller.select_tv_slot(3)

        time.sleep(1.0)

        show_overlay("Searching for Gorlit...")
        controller.tv_search_for_revomon("Gorlit")

        time.sleep(1.0)

        show_overlay("Closing TV...")
        controller.close_tv()

        input("Press Enter once you are in a battle to continue...")

        if controller.is_in_battle_scene():
            show_overlay("Opening attacks menu...")
            controller.open_attacks_menu()

            time.sleep(1.0)

            show_overlay("choosing random attack...")
            controller.choose_move(choose_random=True)

            show_overlay("Closing attacks menu...")
            controller.close_attacks_menu()


            show_overlay("Opening battle bag...")
            controller.open_battle_bag()

            time.sleep(1.0)

            show_overlay("Closing battle bag...")
            controller.close_battle_bag()

            show_overlay("Running from battle...")
            controller.run_from_battle()

        show_overlay("Quting game...")
        controller.quit_game()

        # show_overlay("Closing app...")
        # print(controller.close_app(app=controller))

        # show_overlay("Killing Bluestacks...")
        # print(controller.kill_bluestacks())

        show_overlay("Controller Test: PASSED!")

    except Exception as e:

        show_overlay(f"Controller Test: FAILED!\nError: {e}")
        exit(1)

    finally:

        logger.info(f"ACTIONS -----> {controller.actions}")
