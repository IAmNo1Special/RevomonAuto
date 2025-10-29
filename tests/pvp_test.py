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

        while True:
            if controller.is_in_battle_scene():
                
                logger.info("Opening attacks menu...")
                controller.open_attacks_menu()
                
                logger.info("choosing random attack...")
                controller.choose_move(choose_random=True)


                
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
