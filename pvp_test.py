import logging
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

if __name__ == "__main__":
    try:

        controller = RevoAppController()

        logger.info("Opening Revomon app...")
        controller.open_revomon_app()

        logger.info("Starting game...")
        controller.start_game()

        logger.info("Logging in...")
        controller.log_in()

        while input("Press Enter once your in a battle...") == "":
            while controller.is_in_battle_scene():
                logger.info("Extracting battle info...")
                controller.extract_battle_info()
                logger.info("Opening attacks menu...")
                controller.open_attacks_menu()
                if controller.is_attacks_menu_scene():
                    controller.extract_battle_moves()
                    logger.info("choosing random attack...")
                    controller.choose_move(choose_random=True)
                    time.sleep(3.0)

        logger.info("Quitting game...")
        controller.quit_game()

        logger.info("Closing app...")
        print(controller.close_app(app=controller))

        logger.info("Killing Bluestacks...")
        print(controller.kill_bluestacks())

        logger.info("Controller Test: PASSED!")
        logger.info(f"ACTIONS -----> {controller.actions}")

    except Exception as e:
        logger.error(f"Controller Test: FAILED!!!\nError: {e}")
